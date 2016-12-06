"Test cases for Rule.commands property"

from . import Case
from bobot.Rule import Rule

commandWithSlash = Case.Case([
    Rule({
        'match': 'text',
        'command': 'text',
        'response': 'done text'
    })
], [
    {
        'expected': [Case.Expectation('done text').value()],
        'message': Case.Message('text').value()
    },
    {
        'expected': [Case.Expectation('done text').value()],
        'message': Case.Message('/text').value()
    }
])

commandWithSlashAndUserName = Case.Case([
    Rule({
        'match': 'text',
        'command': 'text',
        'response': 'done text'
    })
], [
    {
        'expected': [Case.Expectation('done text').value()],
        'message': Case.Message('text').value()
    },
    {
        'expected': [Case.Expectation('done text').value()],
        'message': Case.Message('/text@TestBot').value()
    }
])

commandStandaloneWithSlash = Case.Case([
    Rule({
        'command': 'text',
        'response': 'done text'
    })
], [
    {
        'expected': [Case.Expectation('done text').value()],
        'message': Case.Message('/text').value()
    }
])

commandStandaloneWithSlashAndUserName = Case.Case([
    Rule({
        'command': 'text',
        'response': 'done text'
    })
], [
    {
        'expected': [Case.Expectation('done text').value()],
        'message': Case.Message('/text@TestBot').value()
    }
])
