# Response classes

Documentation for **Response** class.

Response classes are special classes provided by **bobot** to make response creation simple. You can create abstract object of response for some message and use it in your code. Also there is a common class called **Response** which provide API to create any type of response by describing options of that response.

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

##
 Common settings
 - `sielent` _(boolean)_ - should disable notifications when message will be revieved
 - `replyId` _(string)_ - reply message id

## Text
Response class to send simple text. 

Usage:
	
	- Text(<str:text>, [settings])

Example:

```python
from bobot import Text

bot.on('text', Text('this is anwer'))

# when bot get message 'text' it answers with text message 'this is answer'
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

## Keyboard
Response class to send keyboards.

Usage: 

	- Keyboard(<string: text>, <list: keyboard>, [settings])
	- Keyboard(<dict: description>, [settings])

Example:

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

##### Response Instance

```python
keyboard = Response({
	'keyboard': {
		'keyboard': [ ['Red pill',  'Blue pill'] ],
		'text': 'Choose'
	}
})
```

## Location
Class to send location with latitute and lontitude.

Usage: 

	- Location(<float:lat>, <float:lon>)

Example: 

```python
from bobot import Location

lat = 43.3041
lon = 40.2301
bot.on('place', Location(lat, lon))
```

## Document
Common class to send file to user.

Usage: 

	- Document(<string:fileAddress>, [string:caption])
	- Document(<binary:file>, [string:caption])

Example: 

```python
from bobot import Docuemnt

bot.on('give me text', Docuemnt('./docs/file.txt', 'Get this text'))

```

##### Response Instance

```python
doc = Response({
	'document': {
		'document': './docs/file.txt',
		'caption': 'Get this text'
	}
})
```

## Photo
Class to send photo.

Usage:

	- Photo(<string:fileAddress>, [string:caption])
	- Photo(<binary:file>, [string:caption])

Example:

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

## Voice
Class to send voice message to user.

Usage: 

	- Voice(<string:fileAddress>, [string:caption])
	- Voice(<binary:file>, [string:caption])

Example:

```python
from bobot import Photo

bot.on('voice', Voice('./files/voice.ogg', 'This is my voice'))
```
##### Response Instance

```python
voice = Response({
	'voice': {
		'voice': './files/image.png',
		'caption': 'This is my caption'
	}
})
```

#### Options for voice
 - `duration` _(int)_ - duration of the voice message in seconds

## Video
Class to send to user video file.

Usage:

    - Video(<string:fileAddress>, [string:caption])
	- Video(<binary:file>, [string:caption])

Example: 

```python
from bobot import Video

myVideo = Video('./videos/video.mp4', 'This is a caption for my video', duration=10, sielent=True)

bot.on('video', myVideo)
```

##### Response Instance

```python
voice = Response({
	'video': {
		'video': './videos/video.mp4',
		'caption': 'This is my caption'
	}
})
```


#### Options for video
 - `duration` _(int)_ - duration of the video message in seconds
 - `width` _(int)_ - video width
 - `height` _(int)_ - video height


