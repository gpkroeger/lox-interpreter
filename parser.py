from Token import Token
from tokenTypes import tokenTypes

class parser:
    def __init__(self, tokens):
        self.finalTokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current]

    def isEnd(self):
        return self.peek().type == tokenTypes.EOF

    def expr(self):
        return equality()
    
    