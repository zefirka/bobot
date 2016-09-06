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

### Text
```python
from bobot import Text

resp = Text('text')
```
### Keyboard