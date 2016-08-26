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
 - `match` (required) : matcher for rule. Look at [matching](#Matching)
 - `response`: response of bot when user action matches to the rule
 - `command`: name of command to match
 - `action`: action to perform before the responding
 - `parse`: parser instance for message body parsing

### Matching

#### Commands


### Responsing

### Actions
#### Register
#### Parsing

