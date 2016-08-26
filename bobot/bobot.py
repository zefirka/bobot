"""
    Main bot module
    Includes class Bot
"""

import json
import re

from bobot.Rule import Rule
from bobot.Response import Response

from bobot.utils import isFn, execValue
from bobot.req import get

__token = None
__api = 'https://api.telegram.org/bot{token}/{method}'

class Bot(object):
    """
        Main Bot class
    """

    __info = None

    def __getMatcher(self, match):
        def fn(text):
            "Mathing by function"
            return match(text)

        def lst(text):
            "Mathing by list of mathers"
            for submatch in match:
                submatcher = self.__getMatcher(submatch)

                if submatcher(text):
                    return True
            return False

        def eq(text):
            "Mathing by equality"
            return text == match

        if isFn(match):
            return fn

        if isinstance(match, list):
            return lst

        if isinstance(match, str) or isinstance(match, int) or isinstance(match, float):
            return eq


    def __execRule(self, rule, update):
        message = update.get('message', {})
        text = message.get('text')
        sender = message.get('from', {})
        senderId = sender.get('id')
        username = sender.get('username', sender.get('first_name'))

        body = text

        if hasattr(rule, 'parse'):
            body = rule.parse(text)

        matcher = self.__getMatcher(rule.match)

        if matcher(text):
            if hasattr(rule, 'register') and not self.clients.get(senderId):
                self.clients[senderId] = self.register(sender, rule.register)

            if hasattr(rule, 'action'):
                rule.action(self, update, body)

            if hasattr(rule, 'response'):
                if isinstance(rule.response, Response):
                    return rule.response.run(update, self)
                else:
                    response = execValue(rule.response, [body, self])
                    response = response.format(text=text, name=username)

                    self.send(senderId, response)

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
        info = json.loads(info)
        self.__info = info
        return info.get('result')

    def send(self, chatId, message):
        """
            Sends message to user
            @public
            @param {str} chatId
            @param  {str} message
            @return {json}
        """

        return call('sendMessage', {
            'chat_id': chatId,
            'text': message
        })

    def keyboard(self, chatId, text, keyboard):
        "Sends keyboard to user"

        return call('sendMessage', {
            'chat_id': chatId,
            'text': text,
            'reply_markup': {
                'keyboard': json.dumps(keyboard.get('keyboard')),
                'resize_keyboard': keyboard.get('resize'),
                'one_time_keyboard': keyboard.get('autohide')
            }
        })

    def process(self, update):
        """
            Process update by bot's rules
            @public
            @param {dict} update
        """

        if not len(self.rules):
            return None

        for rule in self.rules:
            self.__execRule(rule, update)

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

        # Changelog
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

def call(method, data={}):
    "Calls telegram API"
    url = __api.format(token=__token, method=method)
    return get(url, data)
