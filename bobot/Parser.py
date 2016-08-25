"Module contains Parser"

class Parser(object):
    "Parser class"

    def __init__(self, splitter=' '):
        self.splitter = splitter

    def parse(self, text):
        "Parses given text"
        return text.split(self.splitter)
