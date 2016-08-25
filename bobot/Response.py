"""
    User response module
"""

from bobot.utils import flatten
from bobot.Errors import RuleNameError, ResponseFormatError, ResponseMessageError

def createMessage(message, data):
    """
        Creates message from message description object
        and update's data
    """
    text = message

    if isinstance(message, dict):
        text = message.get('text')

        if not text:
            raise ResponseMessageError('Message description should have "text" [String] property', 'text')

        if message.get('interpolate', False):
            text = text.format(
                text=data.get('text'),
                first_name=data.get('first_name'),
                username=data.get('username'),
                second_name=data.get('second_name'))

    return text

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
        return bot.send(chatId, createMessage(message, data))
    return action

def sendMessages(messages=['']):
    "Returns messages sending function"

    def action(bot, chatId, data):
        "Sends messages"
        for message in messages:
            bot.send(chatId, createMessage(message, data))
    return action

class Response():
    "Response class"

    __alowedRules = {
        'sendMessages': sendMessages,
        'sendMessage': sendMessage
    }

    def __addAction(self, actionName, actionArgs):
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
