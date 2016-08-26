from bobot.Rule import Rule

rules = [
	Rule({
		'match': ['alpha', 'betta'],
		'response': 'hoho'
	}),
	Rule({
		'match': 'action',
		'action': lambda bot, upd, body: bot.send(upd.get('message').get('from').get('id'), 'ACTION COMPLETED BROO')
	})
]

def assign(bot):
    bot.on('test', 'responses from on method as string')
    bot.on(r'^test?$', 'responses from on method as regexp')
    bot.rule(rules)
    return bot
