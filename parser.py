from Token import Token
from tokenTypes import tokenTypes

class parseError(Exception):
    pass

class parser:
    def __init__(self, tokens):
        self.finalTokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.isEnd():
            statements.append(self.declaration())
        return statements
    def declaration(self):
        try:
            if self.match(tokenTypes.CLASS):
                return self.classDeclaration()
            if self.match(tokenTypes.FUN):
                return self.function("function")
            if self.match(tokenTypes.VAR):
                return self.varDeclaration()
            return self.statement()
        except parseError:
            return None

    def peek(self):
        return self.tokens[self.current]

    def isEnd(self):
        return self.peek().type == tokenTypes.EOF

    #def expr(self):
    #    return equality()
    
    