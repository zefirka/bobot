"Module containes Rule class"

import re

from bobot.Errors import RuleNameError
from bobot.utils.utils import execValue, isFn
from bobot.Response import Response

__retype = type(re.compile('re'))

def getMatcher(match):
    "Return matcher by `match` value of Rule"

    def fn(text):
        "Mathing by function"
        return match(text)

    def lst(text):
        "Mathing by list of mathers"
        for submatch in match:
            submatcher = getMatcher(submatch)

            if submatcher(text):
                return True
        return False

    def eq(text):
        "Mathing by equality"
        return text == match

    def rematch(text):
        "Mathing as regex"
        return bool(match.match(text))

    if isFn(match):
        return fn

    if isinstance(match, list):
        return lst

    if isinstance(match, str) or isinstance(match, int) or isinstance(match, float):
        return eq

    if isinstance(match, __retype):
        return rematch


class Rule(object):
    "Rules class"

    __alowedRules = ['name', 'match', 'response', 'command', 'action', 'parse', 'transform']

    @staticmethod
    def all(*args):
        "Helper method"

        def matcher(text):
            "Matcher"
            for match in args:
                matcher = getMatcher(match)
                if not matcher(text):
                    return False
            return True
        return matcher

    def __init__(self, d):
        self.match = None

        for key in d:
            if key in self.__alowedRules:
                setattr(self, key, d[key])
            else:
                raise RuleNameError('Rule property: "{}" is invalid'.format(key))

        if hasattr(self, 'command'):
            self.addMatching('/' + self.command)

    def execRule(self, bot, update):
        """
            Executes rule

            @public
            @param {Bot} bot
            @param {dict} update
        """
        message = update.get('message', {})
        text = message.get('text')
        sender = message.get('from', {})
        senderId = sender.get('id')
        username = sender.get('username', sender.get('first_name'))

        body = text

        if hasattr(self, 'parse'):
            body = self.parse(body)

        matcher = getMatcher(self.match)

        if matcher(body):
            if hasattr(self, 'transform'):
                body = self.transform(body)

            if hasattr(self, 'register') and not bot.clients.get(senderId):
                bot.clients[senderId] = bot.register(sender, self.register)

            if hasattr(self, 'action'):
                self.action(bot, update, body)

            if hasattr(self, 'response'):
                if isinstance(self.response, Response):
                    return self.response.run(update, bot)
                elif isinstance(self.response, dict) or isinstance(self.response, list):
                    response = Response(self.response)
                    return response.run(update, bot)
                else:
                    response = execValue(self.response, [body, bot])
                    response = response.format(text=text, username=username, body=body)

                    bot.send(senderId, response)

    def on(self, text, action):
        "Create rule assigned on text"
        if not isinstance(self.match, dict):
            self.match = {
                'value': self.match
            }
            self.match.setdefault('callbacks', {})
            self.match['callbacks'][text] = action

    def addMatching(self, matching):
        "Add new matching"

        if isinstance(self.match, list):
            self.match.append(matching)
        else:
            self.match = [self.match, matching]
