"Errors module"

class RuleNameError(Exception):
    "Exception to determine error in name of rule"
    pass

class ParsingError(Exception):
    "Exception to determine error while parsing of message"
    pass

class ResponseFormatError(Exception):
    "Exception to determine error in response format"
    pass

class ResponseMessageError(Exception):
    "Exception to determine error in response message description"
    pass
