# pylint: skip-file

import sys
import os
import unittest

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from bobot import bobot
from cases.text import simpleText, regexText, arrayTextOr, arrayTextAnd

from cases.response.string import *
from cases.response.text import *
from cases.response.photo import *
from cases.after import afterTests, testResultOkCalls
from cases.commands import *
from cases.rule.check import checkTrue, checkFalse, checkUpdateName
from cases.rule.all import checkAll, checkOr, checkXor

from constants import DEV_BOT_TOKEN

def getBot(rules):
    bot = bobot.init(DEV_BOT_TOKEN, 'TestBot')
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

class RuleAfterTestCases(unittest.TestCase):
    def testAfterCalls(self):
        bot = getBot(afterTests.rules)
        afterTests.checkAfter(bot)
        self.assertNotEqual(afterTests.before, afterTests.after)
        self.assertEqual(afterTests.awaits, afterTests.after)

    def testResultOkCalls(self):
        bot = getBot(testResultOkCalls.rules)
        testResultOkCalls.checkAfter(bot)
        self.assertNotEqual(testResultOkCalls.before, testResultOkCalls.after)
        self.assertEqual(testResultOkCalls.awaits, testResultOkCalls.after)

class RuleCommandTestCases(unittest.TestCase):
    def testCommandWithSlash(self):
        bot = getBot(commandWithSlash.rules)
        self.assertTrue(commandWithSlash.check(bot))
    
    def testCommandWithSlashAndUserName(self):
        bot = getBot(commandWithSlashAndUserName.rules)
        self.assertTrue(commandWithSlashAndUserName.check(bot))
    
    def testCommandStandaloneWithSlash(self):
        bot = getBot(commandStandaloneWithSlash.rules)
        self.assertTrue(commandStandaloneWithSlash.check(bot))
    
    def testCommandStandaloneWithSlashAndUserName(self):
        bot = getBot(commandStandaloneWithSlashAndUserName.rules)
        self.assertTrue(commandStandaloneWithSlashAndUserName.check(bot))

class TextResponseTestCases(unittest.TestCase):
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

    def testResponseInterpolateBody(self):
        bot = getBot(responseInterpolateBody.rules)
        self.assertTrue(responseInterpolateBody.check(bot))
  
class PhotoResponseTestCases(unittest.TestCase):
    def testResponsePhotoWithoutCaption(self):
        bot = getBot(responsePhotoWithoutCaption.rules)
        self.assertTrue(responsePhotoWithoutCaption.check(bot))

    def testResponsePhotoWithCaption(self):
        bot = getBot(responsePhotoWithCaption.rules)
        self.assertTrue(responsePhotoWithCaption.check(bot))

    def testResponsePhotoErrorFileNotFound(self):
        bot = getBot(responsePhotoErrorFileNotFound.rules)
        self.assertTrue(responsePhotoErrorFileNotFound.handlerError(bot, FileNotFoundError))

    def testResponsePhotoWithoutCaptionAsPhoto(self):
        bot = getBot(responsePhotoWithoutCaptionAsPhoto.rules)
        self.assertTrue(responsePhotoWithoutCaptionAsPhoto.check(bot))

    def testResponsePhotoWithCaptionAsPhoto(self):
        bot = getBot(responsePhotoWithCaptionAsPhoto.rules)
        self.assertTrue(responsePhotoWithCaptionAsPhoto.check(bot))

    def testResponsePhotoErrorFileNotFoundAsPhoto(self):
        bot = getBot(responsePhotoErrorFileNotFoundAsPhoto.rules)
        self.assertTrue(responsePhotoErrorFileNotFoundAsPhoto.handlerError(bot, FileNotFoundError))

class BotTestCases(unittest.TestCase):
    def testToken(self):
        bot = bobot.init('a')
        self.assertEqual('a', bot.getToken())

    def testDifferentInstances(self):
        bot1 = bobot.init('a')
        bot2 = bobot.init('b')
        self.assertTrue(bot1.getToken() != bot2.getToken())

class RuleCheckTestCases(unittest.TestCase):
    def testCheckTrue(self):
        bot = getBot(checkTrue.rules)
        self.assertTrue(checkTrue.check(bot))

    def testCheckFalse(self):
        bot = getBot(checkFalse.rules)
        self.assertFalse(checkFalse.check(bot))

    def testCheckUpdateName(self):
        bot = getBot(checkUpdateName.rules)
        self.assertTrue(checkUpdateName.check(bot))

class RuleOrXorAllTestCases(unittest.TestCase):
    def testCheckOr(self):
        bot = getBot(checkOr.rules)
        self.assertTrue(checkOr.check(bot))

    def testCheckXor(self):
        bot = getBot(checkXor.rules)
        self.assertTrue(checkXor.check(bot))

    def testCheckAll(self):
        bot = getBot(checkAll.rules)
        self.assertTrue(checkAll.check(bot))

unittest.main()
