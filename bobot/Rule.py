"Module containes Rule class"

from bobot.Errors import RuleNameError

class Rule(object):
    "Rules class"

    __alowedRules = ['name', 'match', 'response', 'command', 'action', 'parse']

    def __init__(self, d):
        self.match = None

        for key in d:
            if key in self.__alowedRules:
                setattr(self, key, d[key])
            else:
                raise RuleNameError('Rule property: "{}" is invalid'.format(key))

        if hasattr(self, 'command'):
            self.addMatching('/' + self.command)

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
