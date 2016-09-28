#coding: utf8

"""
	Bobot: Simple Telegram Bot API Wrapper for Python3.5
	https://github.com/zefirka/bobot
"""

# А мир был чудесный, как сопля на стене
# А город был хороший, словно крест на спине
# А день был счастливый-как слепая кишка
# А он увидел Солнце...

from .bobot import init
from .Rule import Rule
from .Parser import Parser
from .Response import Response, Message, Text, Keyboard, Location, File, Photo, Contact, Audio, Voice
