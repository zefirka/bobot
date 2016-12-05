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

def getFile(f):
    """
        Returns opened file

        @public
        @param {str} f
        @return file
    """
    return open(f, 'rb')

def instanceof(obj, instances):
    "Checks does object instance of some of given instances"
    lst = filter(lambda instance: isinstance(obj, instance), instances)
    return bool(len(list(lst)))

def omit(obj, keys):
    """
        Remove keys from dict by names
        @param {dict} obj
        @param {list[str]} keys
        @return {dict}

    """
    obj = obj.copy()
    for key in keys:
        if obj.get(key):
            del obj[key]
    return obj

def pickCompat(obj, keys):
    """
        Forming dict from given one and list of keys
        @param {dict} obj
        @param {list[str]} keys
        @return {dict}
    """
    result = {}
    for key in keys:
        result[key] = obj.get(key)
    return result
