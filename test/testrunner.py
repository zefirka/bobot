# pylint: skip-file

import sys
import os
import unittest

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from bobot import bobot
from cases.text import simpleText, regexText, arrayTextOr, arrayTextAnd
from cases.response.string import responseAsText, responseInterpolateText, responseInterpolateUserName, responseInterpolateDate
from cases.response.text import responseAsTextDict, responseAsTextDictOptions, responseAsTextObject, responseAsTextObjectOptions
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

class ResponseTestCases(unittest.TestCase):
    def testResponseAsText(self):
        bot = getBot(responseAsText.rules)
        self.assertTrue(responseAsText.check(bot))

    def testResponseInterpolateText(self):
        bot = getBot(responseInterpolateText.rules)
        self.assertTrue(responseInterpolateText.check(bot))

    def testResponseInterpolateUserName(self):
        bot = getBot(responseInterpolateUserName.rules)
        self.assertTrue(responseInterpolateUserName.check(bot))

    def testResponseInterpolateDate(self):
        bot = getBot(responseInterpolateDate.rules)
        self.assertTrue(responseInterpolateDate.check(bot))

    def testResponseAsTextDict(self):
        bot = getBot(responseAsTextDict.rules)
        self.assertTrue(responseAsTextDict.check(bot))

    def testResponseAsTextDictOptions(self):
        bot = getBot(responseAsTextDictOptions.rules)
        self.assertTrue(responseAsTextDictOptions.check(bot))

    def testResponseAsTextObject(self):
        bot = getBot(responseAsTextObject.rules)
        self.assertTrue(responseAsTextObject.check(bot))

    def testResponseAsTextObjectOptions(self):
        bot = getBot(responseAsTextObjectOptions.rules)
        self.assertTrue(responseAsTextObjectOptions.check(bot))
        
class BotTestCases(unittest.TestCase):
    def testToken(self):
        bot = bobot.init('a')
        self.assertEqual('a', bot.getToken())

    def testDifferentInstances(self):
        bot1 = bobot.init('a')
        bot2 = bobot.init('b')
        self.assertTrue(bot1.getToken() != bot2.getToken())

unittest.main()
