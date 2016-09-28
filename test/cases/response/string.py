"Testcases for text messages"

from .. import Case
from bobot.Rule import Rule

responseAsText = Case.Case([
    Rule({
        'match': 'a',
        'response': 'simple text'
    })
], [
    {
        'expected': [Case.Expectation('simple text').value()],
        'message': Case.Message('a').value()
    }
])

responseInterpolateText = Case.Case([Rule({
    'match': 'i',
    'response': 'interpolate text: {text}'
})], [{
    'expected': [Case.Expectation('interpolate text: i').value()],
    'message': Case.Message('i').value()
}])

responseInterpolateUserName = Case.Case([Rule({
    'match': 'i',
    'response': 'interpolate text: {username}'
})], [{
    'expected': [Case.Expectation('interpolate text: devbot').value()],
    'message': Case.Message('i').value()
}])

responseInterpolateDate = Case.Case([Rule({
    'match': 'i',
    'response': 'interpolate text: {date}'
})], [{
    'expected': [Case.Expectation('interpolate text: 666_666', date='666_666').value()],
    'message': Case.Message('i', date='666_666').value()
}])

responseInterpolateBody = Case.Case([Rule({
    'match': 'i',
    'response': 'interpolate text: {body}'
})], [{
    'expected': [Case.Expectation('interpolate text: i').value()],
    'message': Case.Message('i').value()
}])

