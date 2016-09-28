"Module contains test cases for test server"

import re

from bobot.Rule import Rule
from bobot.Parser import Parser
from bobot.Response import Voice, Video

from cases.files import rules as filerules

parser = Parser()

def gt(x):
    return lambda y: y > x

def lt(x):
    return lambda y: y < x

actionTest = lambda bot, upd, body: bot.sendMessage(upd.get('message').get('from').get('id'), 'action completed bro')

def kb(bot, upd, body):
    # pylint: disable=unused-argument
    "Send keyboard"

    userId = upd.get('message').get('from').get('id')
    bot.sendKeyboard(userId, 'sosi', {
        'resize_keyboard': True,
        'keyboard': [
            [
                {'text': 'alpha'},
                {'text': 'betta'}
            ]
        ],
        'one_time_keyboard': True
    })

testkb = {
    'resize_keyboard': True,
    'text': 'hallo bro',
    'keyboard': [
        [
            'alpha',
            'betta'
        ]
    ],
    'one_time_keyboard': True
}

rules = [
    Rule({
        'match': ['alpha', 'betta'],
        'response': 'alpha or betta was sent'
    }),
    Rule({
        'match': 'action',
        'action': actionTest
    }),
    Rule({
        'name': 'case',
        'match': 'yo-yo',
        'response': [
            {
                'text': {
                    'text': 'Salam, {username}!',
                    'interpolate': True
                }
            },
            {
                'text': 'kase',
            },
            {
                'keyboard': testkb
            }
        ]
    }),
    Rule({
        'match': lambda text: 'parse' in text,
        'parse': parser.parse,
        'response': '{body}'
    }),
    Rule({
        'match': re.compile(r'^regexp'),
        'response': 'regexp included'
    }),
    Rule({
        'parse': lambda text: text.isdigit() and int(text),
        'match': Rule.all(lt(100), gt(50)),
        'response': '{text} less than 100 and greater than 50'
    }),
    Rule({
        'match': Rule.all(re.compile(r'^666'), re.compile(r'.*hell$')),
        'response': 'DAMN HELL!!!'
    }),
    Rule({
        'match': 'keyboard',
        'action': kb
    }),
    Rule({
        'match': re.compile(r'where\s*am\s*i\??'),
        'response': [{
            'location': [40.781984, 43.886827],
        }, {
            'text': 'Home, sweet home'
        }]
    })
]

def wordsCount(message):
    return len(message.split(' '))


def assign(bot):
    bot.rule(Rule({
        'match': lambda length: length > 2,
        'parse': wordsCount,
        'response': 'Words count was: {body}'
    }))

    bot.on('video', Video('./test/files/video.mp4', 'sosi'))

    bot.on('test', 'responses from on method as string')
    bot.on(r'^test?$', 'responses from on method as regexp')
    bot.on('html', {
        'text': {
            'text': '<pre>И так я \nтоже могу\n:3</pre>',
            'format': 'html'
        }
    })
    bot.on('jazz', {
        'sticker': 'BQADAgADBQADIyIEBsnMqhlT3UvLAg'
    })
    bot.rule(rules)
    bot.rule(filerules)

    voice = Voice('./test/files/voice.opus', 'caption', duration=3)

    bot.on('voice', voice)

    return bot
