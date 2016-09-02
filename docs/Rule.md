# Rule

Documentation for **Rule** class.

## Usage

Rules is a declarative description of behavior of a bot to the user action that matches to the rule. So you can describe that if user action (like a sending a message) matches to the given rule then bot should do some action. On the simples way it looks like:

```python
from bobot import Rule

helloRule = Rule({
	'match': 'hello',
	'response': 'hello bro!'
})

bot.rule(helloRule)
```

At first we importing Rule class from bobot library. After it we creating a simple rule we called `helloRule`. You can read this rule as: if user's text matches (e.g. directly equals) to the string `'hello'` then bot should response to user with text message contains string `'hello bro'`. Pretty simple, ya!?

You can store your rules in some list and assign them to bot with method `.rule` which can get simple `Rule` instance or list of instances. `Rule` class strictly checks given `dict`-description for the correct properties. For a properly understanding rule's API read lower.

## API

Every rule creating with given dict. That dict describes the rule. List of rule properties:
 - `name`: name of rule 
 - `match` (required) : matcher for rule. Look at [matching](#matching)
 - `response`: response of bot when user action matches to the rule
 - `command`: name of command to match
 - `action`: action to perform before the responding
 - `parse`: parser instance for message body parsing

### Matching
#### String

If matcher is string then bobot checks that user message's text is **strictly equals** to the given text. 

```python
{
	'match': 'Hello'
}
```

This rule matches only for string `Hello`

#### Regular expressions

If type of matcher is compiled regular expression via `re.compile(pattern, flags)` then bobot checks that user message's text matches to the given regular expression with **re.match** `bool(regexp.match(text))` method. 

```python
{
	'match': re.compile(r'\d\d$')
}
```

This rule will match for strings: `'hi22', '123', 's00 00'`


#### Functions 

If type of matcher is function then bobot checks that user message's text matches to rule by calling that function with message's text and checking result with `bool`. 

```python
{
	'match': lambda text: text in ['alpha', 'betta']
}
```

This rule matches only strings `'alpha'` and `'betta'`.

#### List of matchers

If type of `match` is list, then bobot checks all inner matchers of list and matches to the first truthy condition. **Note**: list of matchers implements **OR** matching not AND.

```python
{
	'match': ['exclude', lambda text: text.isdigit() and int(text) > 100]
}
```

This rule matches all strings that `.isdigit()`, and more than `100` or string `'eclude'`.

#### Rule.all

There is a litlle helpre in Rule class called `.all` which can help create matcher that will be satisfied if **EVERY** given matcher will be satisfied.

```python
{
	'match': Rule.all(re.compile(r'^666'), re.compile(r'.*hell$'))
}
```

This rule will match to text that satisfied regular expressions `r'^666'` **AND** `r'.*hell$'`, as example `'666 damn hell'`

#### Commands

Bot has commands. If you want to rule matching to some command just use property `command` which means that rule matches to the given matcher OR to the `/command`. See:

```python
{
	'match': re.compile(r'^(H|h)ello'),
	'command': 'hi'
}
```

This rule matches to the regexp `r'^(H|h)ello'` and string `'/hi'`

### Responding

Rules allows to describe how bot should response to user if user action matches to the rule.

```python
{
	'match': lambda: True,
	'response': 'Some random text'
}
```

This syntax means that on every user message bot will answer with text: `'Some random text'`. If value of response is type of string then there will be automaticaly interpolated message data as: `response.format(text=text, username=username)`, where text - is original text message and username is sender's username (or first name if username is undefined). 

You can describe more complex responses via [**Response** module](https://github.com/zefirka/bobot/tree/master/docs/Response.md). If value of `response` property in rule is dict or list then there will be created Response class instances based on that values.

### Actions

Actions are just functions which get 3 arguments:
```python
def action(bot, update, body):
	senderId = upd.get('message').get('from').get('id')
	bot.send(senderId, str(body))
```

Where `bot` is bot's instance, `update` is a Telegram Update object, and `body` is a parsed message body

#### Usage:

```python
def twice(bot, update, body):
	senderId = upd.get('message').get('from').get('id')
	bot.send(senderId, str(int(body) * 2))

rule = Rule({
	match: re.compile(r'^\d+$'),
	action: twice
})
```

```
Bot <- '44'
Bot -> '88'
```

#### Parsing and transformation
TODO

