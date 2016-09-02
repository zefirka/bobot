# pylint: disable=wrong-import-position

import sys
import os
import unittest

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from bobot import bobot
from cases.text import simpleText, regexText, arrayText

dev_bot_token = '254968587:AAE1TDdb0f__jl_LDKkpCjtd2eE4UHsTn1Y'

def getBot(rules):
    bot = bobot.init(dev_bot_token)
    bot.setWebhook(None)
    bot.rule(rules)
    return bot

class MyTestCase(unittest.TestCase):
    def testSimpleText(self):
        bot = getBot(simpleText.rules)
        self.assertTrue(simpleText.check(bot))

    def testRegexp(self):
        bot = getBot(regexText.rules)
        self.assertTrue(regexText.check(bot))

    def testArray(self):
        bot = getBot(arrayText.rules)
        self.assertTrue(arrayText.check(bot))

unittest.main()
