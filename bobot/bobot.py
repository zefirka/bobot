"""
    Main bot module
    Includes class Bot
"""

import json
import re

from bobot.req import get
from bobot.Rule import Rule

__token = None
__api = 'https://api.telegram.org/bot{token}/{method}'

def isFn(fn):
    "Detect is argument a function"
    return hasattr(fn, '__call__')

def execValue(val, args=None):
    """
        Returns value if it's not a function, else returns value called with arguments (None by default)
        @param {*|function}     val
        @param {*}              [args]
        @returns {*}
    """
    return val(args) if isFn(val) else val

class Bot():
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

        matcher = self.__getMatcher(rule.match)

        if matcher(text):
            if rule.response:
                response = execValue(rule.response, update)
                response = response.format(text=text, name=username)

                self.send(senderId, response)

    def __addRule(self, rule):
        if not isinstance(rule, Rule):
            raise Exception('rule is not Rule instance')

        self.rules.append(rule)
        return self.rules


    def __init__(self):
        self.rules = []

    def about(self):
        "Returns information about bot"

        if self.__info:
            return self.__info

        info = call('getMe')
        info = json.loads(info)
        self.__info = info
        return info.get('result')

    def send(self, chatId, message):
        "Sends message"

        call('sendMessage', {
            'chat_id': chatId,
            'text': message
        })

    def process(self, update):
        "Process update by bot's rules"

        if not len(self.rules):
            return None

        for rule in self.rules:
            self.__execRule(rule, update)

    def rule(self, rules):
        "Assign rule to bot"

        if isinstance(rules, list):
            rules = [rules]

        for rule in rules:
            self.__addRule(rule)

    def on(self, match, response, flags=0):
        "Subscribes to matching"

        self.rule(Rule({
            'name': match,
            'match': lambda text: bool(re.compile(match, flags).match(text)),
            'response': response
        }))

    def getToken(self):
        'Returns token'

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

def setWebhook(url, certificate=None):
    "Setting up Telegram Webhook"
    data = {
        'url': url
    }
    if certificate:
        data['certificate'] = certificate

    return call('setWebhook', data)
