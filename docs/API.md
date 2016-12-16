# API

## Initialization

At first you should get bot instance:

```python
import bobot

bot = bobot.init(TOKEN)

print(bot.about())
```

## Methods

#### init
Creates `Bot` class instance. 

```
bot = bobot.init(<str: token>, [str: username])
```

Where: 
 - `token` - bot's token
 - `username` - bot's username (e.g. @mybot)


#### setWebhook
Sets webhook. 
```python
bot.setWebhook(String: url, [File: certificate])
```
#### about
Return bot authorization info:
```python
bot.about()
```

#### rule
Assign rule or rules to bot:
```python
singleRule = Rule({...})
bot.rule(singleRule)

listOfRules = [Rule({...}), Rule({...})]
bot.rule(listOfRules)
```

#### process
Apply rules to user update from Telegram. Example from Flask:
```python
@app.route('/', methods=['GET', 'POST'])
def index():
    body = request.get_json()
    bot.process(body)
    return ''
```

#### getUpdates
Calls telegram API method `getUpdates` which returns a list of updates. 

```python
bot.getUpdates()
```