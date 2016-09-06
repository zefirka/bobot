"""
    User responses module.
    Contains:
        Message
        Text
        Keyboard
        Location
        File
        Photo
        Contact
"""

from bobot.utils.utils import instanceof
from bobot.Errors import ResponseFormatError

class Message:
    "Main Message class container"

    method = 'sendMessage'

    def __init__(self, **options):
        self.options = options

    def getData(self, data):
        # pylint: disable=unused-argument
        "Return data to send with method"

        return []

    def getOptions(self):
        "Return options dict"

        options = self.options.get('options', {})
        options.update({
            'disable_notifications': self.options.get('sielent', False)
        })

        return options

    def run(self, bot, update):
        "Apply update to response body"

        message = update.get('message', {})
        text = message.get('text')
        sender = message.get('from', {})
        senderId = sender.get('id')

        data = {
            'text': text,
            'username': sender.get('username'),
            'first_name': sender.get('first_name'),
            'second_name': sender.get('second_name')
        }

        methodArgs = self.getData(data)

        if not instanceof(methodArgs, [dict, tuple]):
            methodArgs = [methodArgs]

        sendArguments = [senderId] + list(methodArgs)

        options = self.getOptions()
        options = {'options': options}
        getattr(bot, self.method)(*sendArguments, **options)

class Text(Message):
    "Text response container"
    # pylint: disable=missing-docstring

    method = 'sendMessage'

    def __init__(self, text, **options):
        super().__init__(**options)
        self.text = text

    def getData(self, data):
        text = self.text

        if self.options.get('interpolate'):
            text = self.text.format(
                text=data.get('text'),
                first_name=data.get('first_name'),
                username=data.get('username'),
                second_name=data.get('second_name'))

        return text

    def getOptions(self):
        options = super().getOptions()

        additional = {
            'disable_web_page_preview': self.options.get('disableWebPreview', False),
            'reply_to_message_id': self.options.get('replyId', None)
        }

        options.update(additional)

        if self.options.get('format'):
            options.update({'parse_mode': self.options.get('format')})

        if self.options.get('markup'):
            options.update({'reply_markup': self.options.get('markup')})

        return options

class Keyboard(Text):
    "Keyboard response container"
    method = 'sendKeyboard'
    # pylint: disable=missing-docstring

    def __init__(self, text, keyboard=None, **options):
        super().__init__(text, **options)
        self.text = text if keyboard else text.get('text')
        self.keyboard = keyboard if keyboard else text.get('keyboard', [])

        if isinstance(self.keyboard, list):
            self.keyboard = {
                'keyboard': self.keyboard
            }

        if options.get('autohide') != None:
            self.keyboard['one_time_keyboard'] = options.get('autohide')

        if options.get('resize') != None:
            self.keyboard['resize_keyboard'] = options.get('resize')

    def getData(self, data):
        return super().getData(data), self.keyboard

class Location(Message):
    "Location response container"
    # pylint: disable=missing-docstring
    method = 'sendLocation'

    def __init__(self, lat, lon, **options):
        super().__init__(**options)
        self.lat = lat
        self.lon = lon

    def getData(self, data):
        return self.lat, self.lon

class Sticker(Message):
    "Sticker response container"
    # pylint: disable=missing-docstring
    def __init__(self, sticker, **options):
        super().__init__(**options)
        self.sticker = sticker

    def getData(self, data):
        return self.sticker


class File(Message):
    "File response container"
    # pylint: disable=missing-docstring

    method = 'sendDocument'

    def __init__(self, file, caption=None, **options):
        super().__init__(**options)
        self.file = file
        self.caption = caption

    def getData(self, data):
        return self.file, self.caption


class Photo(File):
    "Photo response container"
    method = 'sendPhoto'

class Contact(Message):
    "Contact response container"
    # pylint: disable=missing-docstring
    method = 'sendContact'

    def __init__(self, phone, first, last='', **options):
        super().__init__(**options)
        self.phone = phone
        self.first = first
        self.last = last

    def getData(self, data):
        return self.phone, self.first, self.last

def getAction(actionType, data):
    "Calculates action by actionType in response description"
    # pylint: disable=missing-docstring,unnecessary-lambda,redefined-variable-type
    response = None

    if actionType == 'text':
        if isinstance(data, dict):
            text = data.get('text', '')
            del data['text']
            response = Text(text, **data)
        else:
            text = data
            response = Text(text)
    elif actionType == 'location':
        if isinstance(data, dict):
            lat = data.get('lat')
            lon = data.get('lon')
            del data['lat']
            del data['lon']
            response = Location(lat, lon, **data)
        elif isinstance(data, list):
            response = Location(data[0], data[1])
        else:
            raise ResponseFormatError('Invalid syntax at Location response')

    def action(response):
        return lambda bot, update: response.run(bot, update)

    return action(response)

class Response():
    "Response class"

    __map = {
        'text': Text,
        'keyboard': Keyboard,
        'location': Location,
        'photo': Photo
    }

    def __init__(self, responses):
        self.body = responses
        self.actions = []

        if not isinstance(responses, list):
            responses = [responses]

        for response in responses:
            self.addAction(response)

    def addAction(self, response):
        "Adds action to actions list"
        for responseKey in response:

            respBody = response[responseKey]

            if responseKey in self.__map:
                self.actions.append(getAction(responseKey, respBody))
            else:
                raise ResponseFormatError('Invalid response action: "{}"'.format(responseKey))


    def run(self, bot, update):
        "Runs response actions"

        for action in self.actions:
            action(bot, update)
