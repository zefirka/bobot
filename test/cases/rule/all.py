"Testcases for Rule.all property"

from .. import Case
from bobot.Rule import Rule

first = lambda t: t.isdigit()
second = lambda t: int(t) > 100

checkOr = Case.Case([
    Rule({
        'match': [first, second],
        'response': 'checkOr'
    })
], [
    {
        'expected': [
            Case.Expectation('checkOr').value()
        ],
        'message': Case.Message('50').value()
    }
])

checkAll = Case.Case([Rule({
    'match': Rule.all(first, second),
    'response': 'checkAll'
})], [
    {
        'expected': [],
        'message': Case.Message('50').value()
    },
    {
        'expected': [Case.Expectation('checkAll').value()],
        'message': Case.Message('122').value()
    }
])

checkXor = Case.Case([Rule({
    'match': Rule.xor(first, second),
    'response': 'checkXor'
})], [
    {
        'expected': [Case.Expectation('checkXor').value()],
        'message': Case.Message('50').value()
    },
    {
        'expected': [],
        'message': Case.Message('101').value()
    }
])
