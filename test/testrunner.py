# pylint: disable=wrong-import-position

import sys
import os
import unittest

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from bobot import bobot
from cases.text import simpleText, regexText, arrayTextOr, arrayTextAnd
from constants import DEV_BOT_TOKEN

def getBot(rules):
    bot = bobot.init(DEV_BOT_TOKEN)
    bot.setWebhook(None)
    bot.rule(rules)
    return bot

class RuleTestCases(unittest.TestCase):
    def testSimpleText(self):
        bot = getBot(simpleText.rules)
        self.assertTrue(simpleText.check(bot))

    def testRegexp(self):
        bot = getBot(regexText.rules)
        self.assertTrue(regexText.check(bot))

    def testArrayOr(self):
        bot = getBot(arrayTextOr.rules)
        self.assertTrue(arrayTextOr.check(bot))

    def testArrayAnd(self):
        bot = getBot(arrayTextAnd.rules)
        self.assertTrue(arrayTextAnd.check(bot))

unittest.main()
