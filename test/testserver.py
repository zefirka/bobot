# pylint: disable=wrong-import-position
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from flask import Flask, request
from bobot import bobot
from constants import DEV_BOT_TOKEN
import testcases

mode = sys.argv[-1]

app = Flask('bot-test')


bot = bobot.init(DEV_BOT_TOKEN)
bot.setWebhook(None)
bot = testcases.assign(bot)

@app.route('/')
def hello():
    return 'It is alive!'

@app.route('/about')
def about():
    res = str(bot.about())
    return res

@app.route('/updates')
def updates():
    res = str(bot.getUpdates())
    return res

@app.route('/bot', methods=['GET', 'POST'])
def test():
    body = request.get_json()
    bot.process(body)
    return ''

if __name__ == "__main__":
    app.run(port=8002, debug={mode is 'debug'})
