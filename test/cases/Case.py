import json

BOT_ID = 254968587
DEV_ID = 172862922

class Case:
    def __init__(self, rules, cases):
        self.rules = rules
        self.cases = cases

    def check(self, bot):
        for case in self.cases:
            expecteds, results = (case['expected'], bot.process(case['message']))

            if len(results) != len(expecteds):
                return False

            i = 0
            while i < len(results):
                response = json.loads(results[i])
                expected = json.loads(expecteds[i])

                i += 1

                if response['result'] and expected['result']:
                    response['result']['message_id'] = None
                    expected['result']['message_id'] = None
                    response['result']['date'] = None
                    expected['result']['date'] = None

                    if not response == expected:
                        return False
        return True

def coreOk():
    return {
        'ok': True,
        'result': {
            'message_id': None,
            'from': {
                'id': BOT_ID,
                'first_name': 'mcs-python-bot',
                'username': 'mcspythonbot'
            },
            'chat': {
                'id': DEV_ID,
                'first_name': 'T',
                'last_name': 'M',
                'username': 'zeffirsky',
                'type': 'private'
            },
            'date': None,
        }
    }

def coreMessage():
    return {
        'message': {
            'from': {
                'id': '{}'.format(DEV_ID),
                'first_name': 'dev',
                'second_name': 'bot',
                'username': 'devbot'
            },
            'date': None
        }
    }

id2 = lambda _, x: x
dumps = lambda _, x: json.dumps(x)

class Message:
    transform = id2

    def __init__(self, text, core=coreMessage, **opts):
        core = core()

        core['message']['text'] = text

        if opts.get('date'):
            core['message']['date'] = opts.get('date')
        self.message = core

    def value(self):
        # pylint: disable=no-value-for-parameter
        return self.transform(self.message)


class Expectation(Message):
    transform = dumps

    def __init__(self, text, core=coreOk, **opts):
        core = core()
        core['result']['text'] = text

        if opts.get('date'):
            core['result']['date'] = opts.get('date')

        self.message = core
