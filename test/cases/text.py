"Testcases for text messages"

import re

from . import Case
from bobot.Rule import Rule

simpleText = Case.Case([
    Rule({
        'match': 'test',
        'response': 'test-yourself'
    }),
    Rule({
        'match': 'tost',
        'response': 'tost-yourself'
    }),
], [
    {
        'expected': [Case.Expectation('test-yourself').value()],
        'message': Case.Message('test').value()
    },
    {
        'expected': [Case.Expectation('tost-yourself').value()],
        'message': Case.Message('tost').value()
    }
])

regexText = Case.Case([
    Rule({
        'match': re.compile('test'),
        'response': 'inside had test'
    }),
    Rule({
        'match': re.compile('^test'),
        'response': 'starts with test'
    })
], [
    {
        'expected': [
            Case.Expectation('inside had test').value(),
            Case.Expectation('starts with test').value()
        ],
        'message': Case.Message('test dudu').value()
    }
])

arrayText = Case.Case([
    Rule({
        'match': ['alpha', 'betta'],
        'response': 'alpha or betta'
    }),
    Rule({
        'match': ['alpha', 'gamma'],
        'response': 'alpha or gamma'
    })
], [
    {
        'expected': [Case.Expectation('alpha or betta').value()],
        'message': Case.Message('betta').value()
    },
    {
        'expected': [Case.Expectation('alpha or gamma').value()],
        'message': Case.Message('gamma').value()
    },
    {
        'expected': [
            Case.Expectation('alpha or betta').value(),
            Case.Expectation('alpha or gamma').value()
        ],
        'message': Case.Message('alpha').value()
    }

])