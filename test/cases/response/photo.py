"Testcases for photo messages"


from .. import Case
from bobot.Rule import Rule
from bobot.Response import Photo

responsePhotoWithoutCaption = Case.Case([
    Rule({
        'match': 'p',
        'response': {
            'photo': {
                'photo': './test/files/image.png'
            }
        }
    })
], [
    {
        'expected': [Case.Photo('./test/files/image.png', photoId='test').value()],
        'message': Case.Message('p', photoId='test').value()
    }
])

responsePhotoWithCaption = Case.Case([
    Rule({
        'match': 'p',
        'response': {
            'photo': {
                'photo': './test/files/image.png',
                'caption': 'Hello'
            }
        }
    })
], [
    {
        'expected': [Case.Photo('./test/files/image.png', caption='Hello', photoId='test').value()],
        'message': Case.Message('p', photoId='test', caption='Hello').value()
    }
])

responsePhotoErrorFileNotFound = Case.Case([
    Rule({
        'match': 'p',
        'response': {
            'photo': {
                'photo': 'no name '
            }
        }
    })
], [
    {
        'expected': [Case.Photo('./test/files/image.png', caption='Hello', photoId='test').value()],
        'message': Case.Message('p', photoId='test', caption='Hello').value()
    }
])

responsePhotoWithoutCaptionAsPhoto = Case.Case([
    Rule({
        'match': 'p',
        'response': Photo('./test/files/image.png')
    })
], [
    {
        'expected': [Case.Photo('./test/files/image.png', photoId='test').value()],
        'message': Case.Message('p', photoId='test').value()
    }
])

responsePhotoWithCaptionAsPhoto = Case.Case([
    Rule({
        'match': 'p',
        'response': Photo('./test/files/image.png', 'Hello')
    })
], [
    {
        'expected': [Case.Photo('./test/files/image.png', caption='Hello', photoId='test').value()],
        'message': Case.Message('p', photoId='test', caption='Hello').value()
    }
])

responsePhotoErrorFileNotFoundAsPhoto = Case.Case([
    Rule({
        'match': 'p',
        'response': Photo('no name')
    })
], [
    {
        'expected': [Case.Photo('./test/files/image.png', caption='Hello', photoId='test').value()],
        'message': Case.Message('p', photoId='test', caption='Hello').value()
    }
])

