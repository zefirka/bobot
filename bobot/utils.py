"Utils module"

def isFn(fn):
    "Detect is argument a function"
    return hasattr(fn, '__call__')

def execValue(val, args=None):
    """
        Returns value if it's not a function, else returns value called with arguments (None by default)
        @param {*|function}     val
        @param {*}              [args]
        @returns {*}
    """
    return val(*args) if isFn(val) else val


def flatten(lst):
    "Flattens list recursively"
    if lst == []:
        return lst
    if isinstance(lst[0], list):
        return flatten(lst[0]) + flatten(lst[1:])
    return lst[:1] + flatten(lst[1:])
