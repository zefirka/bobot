# Response

Documentation for **Response** class.

## Usage

Reponses are special class to describe response actions. 

```python
from bobot import Response

hello = Response({
	'sendMessages': {
		'text': ['Hello', 'my', '**dear**', 'friend!'],
		'options': {
			'reply_markup': 'markdown'
		}
	}
})

bot.on('Hello', hello)
```

