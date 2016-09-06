"Testcases for text messages"


from .. import Case
from bobot.Rule import Rule
from bobot.Response import Text

responseAsTextDict = Case.Case([
    Rule({
        'match': 'text',
        'response': {
            'text': 'Waiting for text'
        }
    })
], [
    {
        'expected': [Case.Expectation('Waiting for text').value()],
        'message': Case.Message('text').value()
    }
])

responseAsTextDictOptions = Case.Case([
    Rule({
        'match': 'text',
        'response': {
            'text': {
                'text': 'Waiting for {text}',
                'interpolate': True
            }
        }
    })
], [
    {
        'expected': [Case.Expectation('Waiting for text').value()],
        'message': Case.Message('text').value()
    }
])

responseAsTextObject = Case.Case([
    Rule({
        'match': 'text',
        'response': Text('Waiting for text')
    })
], [
    {
        'expected': [Case.Expectation('Waiting for text').value()],
        'message': Case.Message('text').value()
    }
])

responseAsTextObjectOptions = Case.Case([
    Rule({
        'match': 'text',
        'response': Text('Waiting for {text}', interpolate=True)
    })
], [
    {
        'expected': [Case.Expectation('Waiting for text').value()],
        'message': Case.Message('text').value()
    }
])
