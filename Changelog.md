# Changelog

## 0.1.*

### 0.1.5
 - + Added `Rule.xor` helper
 - + Added `check` property into Rule
 - + Improved documentation
 - + Added tests for `check` property and `Rule.xor`
 - * Fixed #8

### 0.1.4
 - + Added `after` rule property
 - + Added `command` rule property
 - + Added test for `after` and `command` properties in Rule

### 0.1.3
 - * Fixed missing Sticker class in exports
 - * Fixed response ID by adding `direct` parameter

### 0.1.2
 - + added `sendChatAction` method
 - * fixed README

### 0.1.1
 - *Fixed `getUpdates` signature

### 0.1.0
 - + Added support for next types: 
  - Locations
  - Contacts
  - Venues
  - Documents
  - Voice
  - Audio
  - Photo
  - Video
  - Sticker

 - + Added specific response classes
 - * Changed one simple format of Response to multiple classes `Text, Location, Keyboard, Photo ...`
 - * Changed format of **Response** descriptions
 - * Renamed `send` -> `sendMessage`
 - * Renamed `keyboard` -> `sendKeyboard`
 - * Fixed error with multiple instaces of bot sharing one token
 - * Improved infrastructure
 - * Write more tests for rules and responses

## 0.0.*

### 0.0.13 (hot-fix)
 - + Added docs for `getUpdates`
 - * Fixed Makefile
 - * Fixed tescases

### 0.0.12
 - + Added tests
 - + Added `sendSticker` Response and method for bot
 - * Changed `sendMessages` format in Response

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
