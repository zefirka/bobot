"""
    User response module
"""

from bobot.utils.utils import flatten
from bobot.Errors import RuleNameError, ResponseFormatError, ResponseMessageError

def createMessage(message, data):
    """
        Creates message from message description object
        and update's data
    """
    options = {}
    text = message

    if isinstance(message, dict):
        text = message.get('text')
        options = message.get('options', {})

        if not text:
            raise ResponseMessageError('Message description should have "text" [String] property', 'text')

        if message.get('interpolate', False):
            text = text.format(
                text=data.get('text'),
                first_name=data.get('first_name'),
                username=data.get('username'),
                second_name=data.get('second_name'))

    return text, options

def processResponseBody(responseBody):
    "Processing response description body to actions lists"

    if isinstance(responseBody, dict):
        return [responseBody]
    elif isinstance(responseBody, list):
        return list(map(processResponseBody, responseBody))
    else:
        raise ResponseFormatError('Wrong response description. Expected dict, got {}'.format(type(responseBody)))

def sendMessage(message=''):
    "Returns message sending function"

    def action(bot, chatId, data):
        "Sends message"
        text, options = createMessage(message, data)
        return bot.send(chatId, text, options)
    return action

def sendMessages(*messages):
    "Returns messages sending function"

    def action(bot, chatId, data):
        "Sends messages"
        for message in messages:
            text, options = createMessage(message, data)
            bot.send(chatId, text, options)
    return action

def sendKeyboard(kb={}):
    "Returns function that sends keyboard to user"
    def action(bot, chatId, data):
        # pylint: disable=unused-argument,missing-docstring
        bot.keyboard(chatId, kb)
    return action

def sendPhoto(photo=None, caption=''):
    "Returns function that sends photo to user"
    if not photo:
        raise ResponseFormatError('Specify photo by URL or File')

    def action(bot, chatId, data):
        # pylint: disable=unused-argument,missing-docstring
        bot.sendPhoto(chatId, photo, caption)

    return action

def sendSticker(stickerId):
    "Returns stickerSender"

    def action(bot, chatId, data):
        # pylint: disable=unused-argument,missing-docstring
        bot.sendSticker(chatId, stickerId)

    return action

class Response():
    "Response class"

    __alowedRules = {
        'sendMessages': sendMessages,
        'sendMessage': sendMessage,
        'sendKeyboard': sendKeyboard,
        'sendSticker': sendSticker,
        'sendPhoto': sendPhoto
    }

    def __addAction(self, actionName, actionArgs):
        if isinstance(actionArgs, list):
            action = self.__alowedRules[actionName](*actionArgs)
        else:
            action = self.__alowedRules[actionName](actionArgs)
        self.actions.append(action)

    def __processResponseDescription(self, response):
        for key in response:
            if key in self.__alowedRules:
                self.__addAction(key, response[key])
            else:
                raise RuleNameError('Response property: "{}" is invalid'.format(key))

    def __init__(self, responseBody):
        self.body = responseBody
        self.actions = []

        responses = flatten(processResponseBody(responseBody))

        for response in responses:
            self.__processResponseDescription(response)

    def run(self, update, bot):
        """
            Runs response actions
        """
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

        for action in self.actions:
            action(bot, senderId, data)
