# Changelog

### 0.0.11
 - + Added `sendPhoto` to bot's methods
 - + Added `sendKeyboard` to Response descriptions
 - + Added `sendPhoto` to Response descriptions
 - + Improved Response sending formats with varargs as list of arguments
 - + Improved error handling
 - * Fixed `bot.keyboard` method
 - * Fixed infrastructure errors

### 0.0.10
 - + Added regular expressins into rule matchings
 - + Added `transform` in rules
 - + Added `Rule.all` - for checking list of matches by **AND** operator
 - * Changed simple response interpolation `name` -> `username`

### 0.0.9
 - + Added documentation for Rules
 - + Added test server (requires Flask)
 - + Added creating **Response** object via **Rule** class instance
 - * Changed `action` in Rules. Now gets 3 arguments - bot instance, update and parsed body of update
 - * Changed `setWebhook` method. Now it is bot's method not method from `bobot` library
 - * Moved `execRule` method to **Rule** class, not it is public method of Rules
 - * Fixed: behavior of bot when Rule has action but not response


### 0.0.8 
 - + Added `Response` class and subscribing via `bot.on('msg', responseDescribe)`
 - + Added custom body parsing. By default as a simple text (`id => id` function)
 - + Added user registering via rule option `register`
 - + Added multiple message sending with `Response` class API