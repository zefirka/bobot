# Response classes

Documentation for **Response** class.

## Usage

Reponses are special classes to describe response actions. There are some specific classes to response with a given type of message like a simple text, keyboard, sticker or photo and common `Response` class which allows to you describe response as you want.

```python
from bobot import Text, Keyboard, Response

bot.on('Hello', Text('Hello **friend**!', format='markdown'))

bot.on('key', Keyboard([[{'text': 'A'}, {'text': 'B'}]]), autohide=True)

bot.on('hi', Response({
	'text': 'Hello'
}))
```

### Common settings
 - `sielent` _(boolean)_ - should disable notifications when message will be revieved
 - `replyId` _(string)_ - reply message id

### Text
Response class to send simple text.

```python
from bobot import Text

resp = Text('text')
```

#### Options
 - `interpolate` _(boolean)_ - should use interpolation

### Keyboard
 - `autohide` _(boolean)_ 