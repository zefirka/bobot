"Test cases for Rule.after property"

from json import loads
from bobot.Rule import Rule

from . import Case

def simpleAfter(responseResult, bot, update):
    afterTests.bring({
        'value': 'Something'
    })

def simpleAfterOk(responseResult, bot, update):
    if loads(responseResult).get('ok'):
        testResultOkCalls.bring({
            'value': 'Ok'
        })

afterTests = Case.Case([
    Rule({
        'match': 'after',
        'response': 'afterTests',
        'after': simpleAfter
    })
], [
    {
        'expected': [Case.Message('afterTests').value()],
        'message': Case.Message('after').value()
    }
], {
    'before': {
        'value': None
    },
    'awaits': {
        'value': 'Something'
    }
})

testResultOkCalls = Case.Case([
    Rule({
        'match': 'after',
        'response': 'testResultOkCalls',
        'after': simpleAfterOk
    })
], [
    {
        'expected': [Case.Message('testResultOkCalls').value()],
        'message': Case.Message('after').value()
    }
], {
    'before': {
        'value': None
    },
    'awaits': {
        'value': 'Ok'
    }
})
