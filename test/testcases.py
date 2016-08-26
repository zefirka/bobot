import re

from bobot.Rule import Rule
from bobot.Parser import Parser

parser = Parser()

def gt(x):
	return lambda y: y > x

def lt(x):
	return lambda y: y < x

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
	}),
	Rule({
		'parse': lambda text: text.isdigit() and int(text),
		'match': Rule.all(lt(100), gt(50)),
		'response': '{text} less than 100 and greater than 50'
	}),
	Rule({
		'match': Rule.all(re.compile(r'^666'), re.compile(r'.*hell$')),
		'response': 'DAMN HELL!!!'
	})
]

def assign(bot):
    bot.on('test', 'responses from on method as string')
    bot.on(r'^test?$', 'responses from on method as regexp')
    bot.rule(rules)
    return bot
