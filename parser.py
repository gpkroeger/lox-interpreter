import Token, tokenTypes, expression, statements

class parser:
    def __init__(self, tokens):
        self.finalTokens = tokens
        self.current = 0

    def peek(self):
        return self.tokens[self.current]

    def isEnd(self):
        return self.peek().type == tokenTypes.EOF
    