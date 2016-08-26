# Changelog

### 0.0.9
 - + Added documentation for Rules
 - + Added test server (requires Flask)
 - * Changed `action` in Rules. Now gets 3 arguments - bot instance, update and parsed body of update
 - * Changed `setWebhook` method. Now it is bot's method not method from `bobot` library
 - * Fixed: behavior of bot when Rule has action but not response


### 0.0.8 
 - + Added `Response` class and subscribing via `bot.on('msg', responseDescribe)`
 - + Added custom body parsing. By default as a simple text (`id => id` function)
 - + Added user registering via rule option `register`
 - + Added multiple message sending with `Response` class API