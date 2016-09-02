"Test cases for files"

from bobot.Rule import Rule

def getFile(f):
    "Opens file"
    return open(f, 'rb')

def sendPhoto(bot, upd, body):
    # pylint: disable=unused-argument
    "Sends photo to user"
    userId = upd.get('message').get('from').get('id')
    bot.sendPhoto(userId, getFile('./test/files/image.png'))

rules = [
    Rule({
        'match': ['image', 'img'],
        'action': sendPhoto
    }),
    Rule({
        'match': 'full_image',
        'response': {
            'sendPhoto': ['./test/files/image.png', 'SIX SIX SIX']
        }
    })
]
