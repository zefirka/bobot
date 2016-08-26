import re

from bobot.Rule import Rule
from bobot.Parser import Parser

parser = Parser()

rules = [
	Rule({
		'match': ['alpha', 'betta'],
		'response': 'alpha or betta was sent'
	}),
	Rule({
		'match': 'action',
		'action': lambda bot, upd, body: bot.send(upd.get('message').get('from').get('id'), 'action completed bro')
	}),
	Rule({
		'name': 'case',
		'match': 'yo-yo',
		'response': [
			{
				'sendMessage': {
					'text': 'Salam, {username}!',
					'interpolate': True
				}
			},
			{
				'sendMessages': 'THIS IS SPARTA!!!'.split(' ')
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
	})
]

def assign(bot):
    bot.on('test', 'responses from on method as string')
    bot.on(r'^test?$', 'responses from on method as regexp')
    bot.rule(rules)
    return bot
