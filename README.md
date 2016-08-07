# bobot

Simple Telegram Bot API wrapper for Python 

## Usage


#### Initialize bot
```python
import bobot

# setup telegram api webhook
bobot.setWebhook(webHookUrl)

# Create bot and use it
bot = bobot.init(TOKEN)
```

#### Subscribe on messages

```python
# by value of message text
bot.on('hello', {
	'sendMessage': 'hello' # set up action and response
})

# create message handlers
def sayHello(update):
	message = update.get('message')
	name = message.get('from').get('first_name')
	text = message.get('text')
	return '{0}, dear {1}'.format(text, name)

# create rule to handle update
rule = Rule({
	'match': ['hello', 'aloha'],
	'response': sayHello
})

# and assign that rule to bot
bot.rule(rule)
```



