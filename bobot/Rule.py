"Module containes Rule class"

import re

from bobot.Errors import RuleNameError
from bobot.utils import execValue, isFn, instanceof, someOf
from bobot.Response import Response, Message

def isResponseClass(i):
    """
       Checks is item is response class (one of Response and Message)
       @param {*} i
       @return {bool}
    """
    return instanceof(i, [Response, Message])

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


def formatResponse(response, update, body):
    "Formats given response with update's data"

    message = update.get('message', {})
    text = message.get('text')
    sender = message.get('from', {})
    senderName = sender.get('first_name')
    senderSecondName = sender.get('second_name')
    username = sender.get('username')
    date = message.get('date')

    return response.format(
        text=text,
        username=username,
        body=body,
        name=senderName,
        secondName=senderSecondName,
        date=date
    )

def getResponder(response, bot, update, body):
    """
        Calculates responder for given response by type

        @param {*}    response
        @param {Bot}  bot
        @param {dict} update
        @param {*}    body
        @return {dict}
    """
    isResponseDirect = False

    if isinstance(response, dict):
        isResponseDirect = response.get('direct', False)
        response = Response(response)

    if isResponseClass(response):
        return response.run(bot, update)

    if isinstance(response, list):
        result = []
        for res in response:
            result.append(getResponder(res, bot, update, body))
        return result

    response = execValue(response, [body, bot])
    response = formatResponse(response, update, body)

    message = update.get('message', {})
    userId = message.get('from', {}).get('id')
    chatId = message.get('chat', {}).get('id')
    responseId = userId if isResponseDirect else chatId

    return bot.sendMessage(responseId, response)

class Rule(object):
    "Rules class"

    __alowedRules = [
        'name',
        'match',
        'response',
        'command',
        'action',
        'parse',
        'transform',
        'after',
        'command',
        'check'
    ]

    @staticmethod
    def all(*args):
        "Helper method: return matcher for EVERY argument matcher"

        def matcher(text):
            "Matcher"
            for match in args:
                matcher = getMatcher(match)
                if not matcher(text):
                    return False
            return True
        return matcher

    @staticmethod
    def xor(*args):
        "Helper method: return matcher for ONE OF argument matcher"

        def matcher(text):
            "Matcher"
            matches = len(list(filter(bool, map(lambda arg: getMatcher(arg)(text), args))))
            return matches == 1
        return matcher

    def __init__(self, d):
        self.match = None
        self.command = None

        for key in d:
            if key in self.__alowedRules:
                setattr(self, key, d[key])
            else:
                raise RuleNameError('Rule property: "{}" is invalid'.format(key))

        if not self.match and not self.command:
            raise Exception('Rule have not matcher and command at same time')

    def getCommandMatcher(self, bot):
        """
            Returns matcher for any type of command e.g.
            /commandName
            /commandName@bot_name
        """

        if self.command:
            return getMatcher(re.compile(r'^/{command}(@{name})?$'.format(command=self.command, name=bot.name), re.I))

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

        body = text

        if hasattr(self, 'check'):
            if not self.check(update):
                return None

        if hasattr(self, 'parse'):
            #pylint: disable=broad-except
            try:
                body = self.parse(body)
            except Exception as error:
                print('Parsing Error:')
                print(error)

        matcher = lambda x: False

        if self.match:
            matcher = getMatcher(self.match)

        if self.command:
            matcher = someOf(matcher, self.getCommandMatcher(bot))

        if matcher(body):
            if hasattr(self, 'transform'):
                body = self.transform(body)

            if hasattr(self, 'register') and not bot.clients.get(senderId):
                bot.clients[senderId] = bot.register(sender, self.register)

            if hasattr(self, 'action'):
                self.action(bot, update, body)

            if hasattr(self, 'response'):
                responseResult = getResponder(self.response, bot, update, body)

                if hasattr(self, 'after'):
                    self.after(responseResult, bot, update)

                return responseResult

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
