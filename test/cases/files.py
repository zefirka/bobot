from bobot.Rule import Rule

def getFile(f):
    return open(f, 'rb')

def sendPhoto(bot, upd, body):
    id = upd.get('message').get('from').get('id')
    bot.sendPhoto(id, getFile('./test/files/image.png'))

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
