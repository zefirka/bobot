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

from bobot.utils.utils import instanceof, omit, pickCompat
from bobot.Errors import ResponseFormatError, ResponseMessageError

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

        options = self.options or {}
        options.update({
            'disable_notification': self.options.get('sielent', False),
            'reply_to_message_id': self.options.get('replyId', None),
        })

        if self.options.get('markup'):
            options.update({'reply_markup': self.options.get('markup', None)})

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

        return getattr(bot, self.method)(*sendArguments, **options)

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
        print('options: {}'.format(options))

        additional = {
            'disable_web_page_preview': self.options.get('disableWebPreview', False),
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

    @staticmethod
    def __toKeyboard(row):
        def toButton(btn):
            if isinstance(btn, dict) and btn['text']:
                return btn
            else:
                return {
                    'text': str(btn)
                }
        return list(map(toButton, row))

    def __init__(self, text, keyboard=None, **options):
        #pylint: disable=redefined-variable-type
        super().__init__(text, **options)
        self.text = text if keyboard else text.get('text')
        self.keyboard = keyboard if keyboard else text.get('keyboard', [])

        self.keyboard = list(map(self.__toKeyboard, self.keyboard))

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
    method = 'sendSticker'

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

class Document(File):
    "Document response container"
    method = 'sendDocument'

class Voice(File):
    "Voice response container"
    method = 'sendVoice'

class Audio(File):
    "Audio response container"
    method = 'sendAudio'

class Video(File):
    "Video response container"
    method = 'sendVideo'

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
    # pylint: disable=missing-docstring,unnecessary-lambda,redefined-variable-type,too-many-locals,too-many-branches
    response = None

    if actionType == 'text':
        if isinstance(data, dict):
            text = data.get('text', '')
            data = omit(data, ['text'])
            response = Text(text, **data)
        else:
            text = data
            response = Text(text)
    elif actionType == 'location':
        if isinstance(data, dict):
            lat = data.get('lat')
            lon = data.get('lon')
            options = omit(data, ['lat', 'lon'])
            response = Location(lat, lon, **options)
        elif isinstance(data, list):
            response = Location(data[0], data[1])
        else:
            raise ResponseFormatError('Invalid format at Location response')
    elif actionType == 'keyboard':
        if isinstance(data, dict):
            optionNames = ['autohide', 'resize']
            options = pickCompat(data, optionNames)
            keyboard = omit(data, optionNames)
            response = Keyboard(keyboard, **options)
        else:
            raise ResponseFormatError('Invalid format at Keyboard response')
    elif actionType == 'photo':
        if isinstance(data, dict):
            photo = data.get('photo')
            caption = data.get('caption')
            options = omit(data, ['photo', 'caption'])
            response = Photo(photo, caption, **options)
        else:
            response = Photo(data)
    elif actionType == 'sticker':
        if isinstance(data, dict):
            sticker = data.get('sticker')
            options = omit(data, ['sticker'])
            response = Sticker(sticker, **options)
        else:
            response = Sticker(data)
    elif actionType == 'contact':
        if isinstance(data, dict):
            phone = data.get('phone')
            name = data.get('firstName')
            lastName = data.get('lastName')
            options = omit(data, ['phone', 'firstName', 'lastName'])
            response = Contact(phone, name, lastName, **options)
        else:
            raise ResponseFormatError('Invalid format at Contact response')
    elif actionType == 'voice' or actionType == 'audio':
        if isinstance(data, dict):
            file = data.get(actionType)
            caption = data.get('caption')
            options = omit(data, ['voice', 'caption', 'audio'])
            response = Voice(file, caption, **options) if actionType == 'voice' else Audio(file, caption, **options)
        else:
            typeOfResponse = 'Voice' if actionType == 'voice' else 'Audio'
            raise ResponseFormatError('Invalid format at {} response'.format(typeOfResponse))
    elif actionType == 'video':
        if isinstance(data, dict):
            file = data.get('video')
            caption = data.get('caption')
            options = omit(data, ['caption', 'video'])
            response = Video(file, caption, **options)
        else:
            raise ResponseFormatError('Invalid format at Video response')
    else:
        raise ResponseMessageError('Invalid response type: "{}"'.format(actionType))

    def action(response):
        return lambda bot, update: response.run(bot, update)

    return action(response)

class Response():
    "Response class"

    __map = {
        'text': Text,
        'keyboard': Keyboard,
        'location': Location,
        'photo': Photo,
        'sticker': Sticker,
        'audio': Audio,
        'voice': Voice
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
        if len(response) > 1:
            raise ResponseFormatError('Response can hold only one action')

        responseKey = list(response.keys()).pop()
        respBody = response[responseKey]

        if responseKey in self.__map:
            self.action = getAction(responseKey, respBody)
        else:
            raise ResponseFormatError('Invalid response action: "{}"'.format(responseKey))

    def run(self, bot, update):
        "Runs response actions"
        return self.action(bot, update)
