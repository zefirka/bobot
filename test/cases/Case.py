import json

BOT_ID = 254968587
DEV_ID = 172862922

__results = {
    'message_id': 'id',
    'date': 'date',
    'caption': 'caption'
}

def clearPhoto(_id):
    def clearFn(photo):
        photo.update({
            'file_id': _id
        })
        return photo
    return clearFn

def clear(response, **opts):
    for opt in __results:
        response['result'][opt] = opts.get(__results[opt], None)

    if response['result'].get('photo'):
        response['result']['photo'] = list(map(clearPhoto(opts.get('photoId')), response['result']['photo']))
    return response

class Case:
    def __init__(self, rules, cases):
        self.rules = rules
        self.cases = cases

    def check(self, bot):
        for case in self.cases:

            msg = case['message'][0]
            expecteds, results = (case['expected'], bot.process(msg))

            if len(results) != len(expecteds):
                return False

            i = 0
            while i < len(results):
                resultItem = results[i]
                response = resultItem if isinstance(resultItem, dict) else json.loads(resultItem)
                expectedItem = expecteds[i]

                expectedValue = expectedItem[0]
                expectedOptions = expectedItem[1]

                expected = expectedValue

                i += 1

                print(response)
                print('response ------->')
                print(expected)
                print('expected ------->')

                if response.get('result') and expected.get('result'):
                    response = clear(response, **expectedOptions)
                    expected = clear(expected, **expectedOptions)

                    if not response == expected:
                        return False
        return True

    def handlerError(self, bot, errorClass):
        #pylint: disable=broad-except
        try:
            self.check(bot)
        except Exception as err:
            if isinstance(err, errorClass):
                return True
            return False

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

def coreOkPhoto(pid):
    core = coreOk()
    core['result'].update({
        'photo': [
            {
                'height': 84,
                'file_size': 2139,
                'width': 90,
                'file_id': pid
            },
            {
                'height': 298,
                'file_size': 21120,
                'width': 320,
                'file_id': pid
            },
            {
                'height': 416,
                'file_size': 35367,
                'width': 446,
                'file_id': pid
            }
        ]
    })
    return core

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

        if opts.get('muted'):
            core['message']['disable_notification'] = True

        self.options = opts
        self.message = core

    def value(self):
        # pylint: disable=no-value-for-parameter
        return self.transform(self.message), self.options


class Expectation(Message):
    transform = id2

    def __init__(self, text, core=coreOk, **opts):
        core = core()
        core['result']['text'] = text

        if opts.get('date'):
            core['result']['date'] = opts.get('date')

        if opts.get('muted'):
            core['result']['disable_notification'] = opts.get('muted')

        self.options = opts
        self.message = core

class Photo(Expectation):
    def __init__(self, _id, core=coreOkPhoto, **opts):
        core = core(_id)

        if opts.get('date'):
            core['result']['date'] = opts.get('date')

        if opts.get('muted'):
            core['result']['disable_notification'] = opts.get('muted')

        self.options = opts
        self.message = core

