from Token import Token
from tokenTypes import tokenTypes
from typing import List

class parseError(Exception):
    pass

class parser:
    def __init__(self, tokens: List[Token]) ->None:
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
    
    def previous(self):
        return self.tokens[self.current - 1]
    
    def advance(self):
        if not self.isEnd():
            self.current += 1
        return self.previous()

    def check(self, type, tokenType):
        if self.isEnd():
            return False
        else:
            return self.peek().tokType == tokenType

    def isEnd(self):
        return self.peek().tokType == tokenTypes.EOF

    def error(self, type: tokenTypes, message: str):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    #def expr(self):
    #    return equality()
    
    