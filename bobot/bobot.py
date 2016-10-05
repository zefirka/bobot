"""
    Main bot module
    Includes class Bot
"""

import re
from json import loads, dumps

from bobot.Rule import Rule
from bobot.Response import Response
from bobot.Errors import MessageError
from bobot.utils.req import get, post
from bobot.utils.utils import getFile

__api = 'https://api.telegram.org/bot{token}/{method}'

def init(token):
    'Initialize'

    bot = Bot(token)
    return bot

def call(token, method, data={}, files=None):
    "Calls telegram API"
    url = __api.format(token=token, method=method)

    if files:
        response = loads(post(url, data, None, files))
    else:
        response = get(url, data)

    return response

def caller(method, **kwargs):
    "Telegram API calling decorator"

    method = kwargs.get('method', method)

    def sendFunciton(token, *args):
        "Calling function"
        return call(token, method, *args)

    def callerDecorator(dataFunction):
        "Caller decorator"

        def callerFunction(self, chatId=None, *args, **options):
            "API Caller"
            argumentsOrder = kwargs.get('arguments')
            requiredArguments = kwargs.get('required')

            if argumentsOrder and requiredArguments:
                for index, argument in enumerate(argumentsOrder):
                    if requiredArguments.get(argument) and not args[index]:
                        raise requiredArguments.get(argument)

            if kwargs.get('static', False) is True:
                callArgs = dataFunction(chatId, *args)
            else:
                callArgs = dataFunction(*args)

            if isinstance(callArgs, dict):
                callArgs = [callArgs]

            if kwargs.get('static', False) is not True:
                callArgs[0]['chat_id'] = chatId

            if options.get('options', False):
                callArgs[0].update(options.get('options'))

            return sendFunciton(self.getToken(), *callArgs)

        return callerFunction

    return callerDecorator

class Bot(object):
    # pylint: disable=no-self-argument
    """
        Bot class
    """
    def __addRule(self, rule):
        if not isinstance(rule, Rule):
            raise Exception('rule is not Rule instance')

        self.rules.append(rule)
        return self.rules

    #####################################################
    #####################################################

    def __init__(self, token):
        self.__info = None
        self.__token = token
        self.rules = []
        self.clients = {}

    def about(self):
        "Returns information about bot"

        if self.__info:
            return self.__info

        info = call(self.__token, 'getMe')
        info = loads(info)
        self.__info = info
        return info.get('result')

    @caller('sendMessage',
            arguments=['text'],
            required={
                'text': MessageError('Specify message\'s text')
            })
    def sendMessage(text):
        "Sends text to user"

        data = {
            'text': text
        }

        return data

    @caller('sendSticker',
            arguments=['sticker'],
            required={
                'sticker': MessageError('Specify StickerID')
            })
    def sendSticker(stickerId):
        "Sends stricker to user"

        data = {
            'sticker': stickerId
        }

        return data

    @caller('sendPhoto')
    def sendPhoto(photo, caption=None):
        "Sends photo to user"

        data = {}
        if caption:
            data['caption'] = caption

        if isinstance(photo, str):
            photo = getFile(photo)

        file = {'photo': photo}

        return data, file

    @caller('sendDocument')
    def sendDocument(doc, caption=None):
        "Sends document"

        data = {}
        if caption:
            data['caption'] = caption

        if isinstance(doc, str):
            doc = getFile(doc)

        file = {'document': doc}

        return data, file

    @caller('sendAudio')
    def sendAudio(audio, caption=None):
        "Sends audio"

        data = {}
        if caption:
            data['caption'] = caption

        if isinstance(audio, str):
            audio = getFile(audio)

        file = {'audio': audio}

        return data, file

    @caller('sendVoice')
    def sendVoice(voice, caption=None):
        "Sends voice"

        data = {}
        if caption:
            data['caption'] = caption

        if isinstance(voice, str):
            voice = getFile(voice)

        file = {'voice': voice}

        return data, file

    @caller('sendVideo')
    def sendVideo(video, caption=None):
        "Sends video"

        data = {}
        if caption:
            data['caption'] = caption

        if isinstance(video, str):
            video = getFile(video)

        file = {'video': video}

        return data, file

    @caller('sendLocation')
    def sendLocation(lat, lon):
        "Sends location"

        return {
            'latitude': lat,
            'longitude': lon
        }

    @caller('sendContact')
    def sendContact(phone, name, secondName=None):
        "Send contact to user"
        return {
            'phone_number': phone,
            'first_name': name,
            'secon_name': secondName
        }

    @caller('sendMessage')
    def sendKeyboard(text, keyboard=None):
        "Sends keyboard to user"

        if not keyboard:
            keyboard = text
            text = text.pop('text', '')

        if not text:
            raise MessageError('Specify text message')

        board = dumps(keyboard)

        return {
            'text': text,
            'reply_markup': board
        }

    def process(self, update):
        """
            Process update by bot's rules
            @public
            @param {dict} update
        """
        result = []

        if not len(self.rules):
            return None

        for rule in self.rules:
            result.append(rule.execRule(self, update))

        return list(filter(bool, result))

    def rule(self, rules):
        """
            Assign rules to bot
            @public
            @param {list[Rule]|Rule} rules
        """

        if not isinstance(rules, list):
            rules = [rules]

        for rule in rules:
            self.__addRule(rule)

    def on(self, match, response, flags=0):
        "Subscribes to matching"

        if isinstance(response, dict) or isinstance(response, list):
            response = Response(response)

        self.rule(Rule({
            'name': match,
            'match': lambda text: bool(re.compile(match, flags).match(text)),
            'response': response
        }))

    @caller('getUpdates', static=True)
    def getUpdates(limit=None, offset=None):
        "Call getUpdates method"
        return {
            'limit': limit,
            'offset': offset
        }

    def register(self, user, registerInfo={'id': 'id'}):
        "Registers client to bot memory"

        result = {}
        for key in registerInfo:
            result[key] = user.get(registerInfo[key])
        return result

    @caller('setWebhook', static=True)
    def setWebhook(url, certificate=None):
        "Setting up Telegram Webhook for given bot"

        data = {
            'url': url
        }

        if certificate:
            data['certificate'] = certificate

        return data

    def getToken(self):
        "Returns token"

        return self.__token
