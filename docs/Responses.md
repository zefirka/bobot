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

#### As Response instaces

All single Response class instances can be represented as common `Response` class instance declared with some dict. So:
```python
Text('Hello', interpolate=true)

#equals to

Response({
	'text': {
		'text': 'Hello',
		'interpolate': True
	}
})
```

### Common settings
 - `sielent` _(boolean)_ - should disable notifications when message will be revieved
 - `replyId` _(string)_ - reply message id

### Text
Response class to send simple text. 

Usage: `Text(<str:text>, [settings])`

```python
from bobot import Text

bot.on('text', Text('this is anwer'))
```

##### Options
 - `interpolate` _(boolean)_ - should use interpolation
 - `disableWebPreview` _(boolean)_ - should disable web page preview

##### Response Instance

```python
text = Response({
	'text': 'hello'
})

textOptions = Response({
	'text': {
		'text': 'text {username}',
		'interpolate': True # this is part of option
	}
})
```

### Keyboard
Response class to send 
Usage: 
 - `Keyboard(<string: text>, <list: keyboard>, [settings])`
 - `Keyboard(<dict: description>, [settings])`

```python

times = Keyboard('Choose time', [['12:00', '18:00']], resize=True)

days = Keyboard({
	'text': 'Choose day',
	'keyboard': [  ['Monday', 'Sunday']]
}, autohide=True)
```

##### Options
 - `autohide` _(boolean)_ - should hide keyboard after user's answer
 - `resize` _(boolean)_ - should resize keyboard markup


### Location

Usage: `Location(<float:lat>, <float:lon>)`

```python
from bobot import Location

lat = 43.3041
lon = 40.2301
bot.on('place', Location(lat, lon))
```

### Photo

Usage: 
	- `Photo(<string:fileAddress>, [string:caption])`
	- `Photo(<binary:file>, [string:caption])`

```python
from bobot import Photo

bot.on('photo', Photo('./files/image.png', 'This is my caption'))
```
##### Response Instance

```python
photo = Response({
	'photo': {
		'photo': './files/image.png',
		'caption': 'This is my caption'
	}
})
```

### Voice

### Audio

### Document

