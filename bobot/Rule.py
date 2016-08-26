"Module containes Rule class"

from bobot.Errors import RuleNameError
from bobot.utils import execValue, isFn
from bobot.Response import Response

def getMatcher(match):
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

    if isFn(match):
        return fn

    if isinstance(match, list):
        return lst

    if isinstance(match, str) or isinstance(match, int) or isinstance(match, float):
        return eq

class Rule(object):
    "Rules class"

    __alowedRules = ['name', 'match', 'response', 'command', 'action', 'parse']

    def __init__(self, d):
        self.match = None

        for key in d:
            if key in self.__alowedRules:
                # if key in ['action', 'parse']:
                #     fn = d[key]
                #     setattr(self, key, lambda: d[key])
                # else:
                    setattr(self, key, d[key])
            else:
                raise RuleNameError('Rule property: "{}" is invalid'.format(key))

        if hasattr(self, 'command'):
            self.addMatching('/' + self.command)

    def execRule(self, bot, update):
        message = update.get('message', {})
        text = message.get('text')
        sender = message.get('from', {})
        senderId = sender.get('id')
        username = sender.get('username', sender.get('first_name'))

        body = text

        if hasattr(self, 'parse'):
            parser = self.parse()
            body = parser(text)

        matcher = getMatcher(self.match)

        if matcher(text):
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
                    response = response.format(text=text, name=username)

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
