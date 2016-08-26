# bobot

Simple Telegram Bot API wrapper for Python 

## Usage

#### Initialize bot
```python
import bobot

# Create instance of bot
bot = bobot.init(TOKEN)

# setup telegram api webhook
bot.setWebhook(webHookUrl)
```

#### Subscribe on messages

```python
# by value of message text
bot.on('hello', 'hello yourself bro!') # set up request and response

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

## Documentation

### [Rules](https://github.com/zefirka/bobot/tree/master/docs/Rule.md)
