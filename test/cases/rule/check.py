"Testcases for Rule.check property"

from .. import Case
from bobot.Rule import Rule

checkTrue = Case.Case([
    Rule({
        'check': lambda x: True,
        'match': 'checkTrue',
        'response': 'checkTrue'
    })
], [
    {
        'expected': [Case.Expectation('checkTrue').value()],
        'message': Case.Message('checkTrue').value()
    }
])

checkFalse = Case.Case([Rule({
    'check': lambda x: False,
    'match': '3140981',
    'response': '3140981'
})], [{
    'expected': [None],
    'message': Case.Message('3140981').value()
}])

def isTeste(upd):
    return upd.get('message').get('from').get('username') == 'devbot',

checkUpdateName = Case.Case([Rule({
    'check': isTeste,
    'match': 'zefirka',
    'response': 'zefirka'
})], [{
    'expected': [Case.Expectation('zefirka').value()],
    'message': Case.Message('zefirka').value()
}])
