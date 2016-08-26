"Utils module"

def isFn(fn):
    """
        Is argument a function

        @public
        @param {*} fn
        @return {bool}
    """
    return hasattr(fn, '__call__')

def execValue(val, args=None):
    """
        Returns value if it's not a function, else returns value called with arguments (None by default)

        @public
        @param {*|function}     val
        @param {*}              [args]
        @returns {*}
    """
    return val(*args) if isFn(val) else val

def flatten(lst):
    """
        Flattens list recursively

        @public
        @param {list} lst
        @return {list}
    """
    if lst == []:
        return lst
    if isinstance(lst[0], list):
        return flatten(lst[0]) + flatten(lst[1:])
    return lst[:1] + flatten(lst[1:])
