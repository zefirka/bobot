"""
    Main bot module
    Includes class Bot
"""

import re
from json import loads, dumps

from bobot.Rule import Rule
from bobot.Response import Response
from bobot.Errors import MessageTextEmptyError
from bobot.utils.req import get, post
from bobot.utils.utils import getFile

__token = None
__api = 'https://api.telegram.org/bot{token}/{method}'

class Bot(object):
    """
        Main Bot class
    """

    __info = None

    def __addRule(self, rule):
        if not isinstance(rule, Rule):
            raise Exception('rule is not Rule instance')

        self.rules.append(rule)
        return self.rules

    #####################################################
    #####################################################

    def __init__(self):
        self.rules = []
        self.clients = {}

    def about(self):
        "Returns information about bot"

        if self.__info:
            return self.__info

        info = call('getMe')
        info = loads(info)
        self.__info = info
        return info.get('result')

    def send(self, chatId, text, options={}):
        """
            Sends text to user
            @public
            @param {str} chatId
            @param  {str} text
            @return {json}
        """

        if not text:
            raise MessageTextEmptyError('Specify message\'s text')

        data = {
            'chat_id': chatId,
            'text': text
        }

        data.update(options)

        return call('sendMessage', data)

    def sendSticker(self, chatId, stickerId):
        """
            Sends photo to user
            @public
            @param {str}        chatId
            @param {str}        strickerId
        """

        data = {
            'chat_id': chatId,
            'sticker': stickerId
        }

        return call('sendSticker', data)

    def sendPhoto(self, chatId, photo, caption=None):
        """
            Sends photo to user
            @public
            @param {str}        chatId
            @param {str|file}   photo
            @param {strp}       [caption]
            @return {tuple}     <photos, result>
        """

        data = {
            'chat_id': chatId,
            'caption': caption
        }

        if isinstance(photo, str):
            photo = getFile(photo)

        file = {'photo': photo}

        res = call('sendPhoto', data, file)
        photos = res.get('result', {}).get('photos', [])

        return photos, res

    def keyboard(self, chatId, text, keyboard=None):
        """
            Sends keyboard to user
            @public
            @param {str} chatId
            @param {str|dict} text - text or keyboard dict
            @param {dict} [keyboard]
        """

        if not keyboard:
            keyboard = text
            text = text.pop('text', '')

        if not text:
            raise MessageTextEmptyError('Specify text message')

        board = dumps(keyboard)

        return call('sendMessage', {
            'chat_id': chatId,
            'text': text,
            'reply_markup': board
        })

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

    def getUpdates(self, limit=None, offset=None):
        "Call getUpdates method"

        return call('getUpdates', {
            'limit': limit,
            'offset': offset
        })

    def register(self, user, registerInfo={'id': 'id'}):
        "Registers client to bot memory"
        result = {}
        for key in registerInfo:
            result[key] = user.get(registerInfo[key])
        return result

    def setWebhook(self, url, certificate=None):
        """
            Setting up Telegram Webhook for given bot
            @public
            @param {str} url
            @param {str} [certificate]
            @return {json}
        """

        data = {
            'url': url
        }

        if certificate:
            data['certificate'] = certificate

        return call('setWebhook', data)

    def getToken(self):
        "Returns token"

        return __token


def init(token):
    'Initialize'

    global __token
    __token = token

    bot = Bot()
    return bot

def call(method, data={}, files=None):
    "Calls telegram API"
    url = __api.format(token=__token, method=method)

    if files:
        return loads(post(url, data, None, files))

    return get(url, data)
