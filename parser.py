from lib2to3.pgen2 import token
from Token import Token
from tokenTypes import tokenTypes
from typing import List
from .evals import *

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
            #if self.match(tokenTypes.CLASS):
            #    return self.classDeclaration() 
            if self.match(tokenTypes.FUN):
                return self.function("function")
            if self.match(tokenTypes.VAR):
                return self.varDeclaration()
            return self.statement()
        except parseError:
            return None
    
    def expression(self):
        return self.assignment()
    
    def assignment(self):
        expr = self.logicalOR()
        if self.match(tokenTypes.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                return Assign(expr.name, value)
            elif isinstance(expr, Get):
                return Set(expr.object, expr.name, value)
            raise self.error(equals, "Invalid assignment")
        return expr

    def logicalOR(self):
        expr = self.logicalAND()
        while self.match(tokenTypes.OR):
            expr = Logical(expr, self.previous(), self.logicalAND())
        return expr
    
    def logicalAND(self):
        expr = self.equality()
        while self.match(tokenTypes.AND):
            expr = Logical(expr, self.previous(), self.equality())
        return expr

    def equality(self):
        left = self.comparison()
        while self.match(tokenTypes.BANG_EQUAL, tokenTypes.EQUAL_EQUAL):
            left = Binary(left, self.previous(), self.comparison())
        return left

    def comparison(self):
        left = self.term()
        while self.match(tokenTypes.GREATER, tokenTypes.GREATER_EQUAL, tokenTypes.LESS, tokenTypes.LESS_EQUAL):
            left = Binary(left, self.previous(), self.term())
        return left
    def term(self):
        left = self.factor()
        while self.match(tokenTypes.MINUS, tokenTypes.PLUS):
            left = Binary(left, self.previous, self.factor())
        return left
    
    def factor(self):
        left = self.unary()
        while self.match(tokenTypes.SLASH, tokenTypes.STAR):
            left = Binary(left, self.previous(), self.unary())
        return left

    def unary(self):
        if self.match(tokenTypes.MINUS, tokenTypes.BANG):
            return Unary(self.previous(), self.unary())
        else:
            return self.call()
    
    def call(self):
        expr = self.primary()
        while True:
            if self.match(tokenTypes.LEFT_PAREN):
                expr = self.finishCall(expr)
            if self.match(tokenTypes.DOT):
                name = self.consume(tokenTypes.IDENTIFIER, "Expected function name after .")
                expr = Get(expr, name)
            else:
                break
        return expr
        
    def finishCall(self, expr):
        args = []
        if not self.check(tokenTypes.RIGHT_PAREN):
            args.append(self.expression())
            while self.match(tokenTypes.COMMA):
                if len(args) >= 255:
                    self.error(self.peek(), "Max of 255 Arguments")
                args.append(self.expression())
        paren = self.consume(tokenTypes.RIGHT_PAREN, "Expected a ')'.")
        return Call(expr, paren, args)
    
    def consume(self, toktype: tokenTypes, msg: str):
        if self.check(toktype):
            return self.advance()
        raise self.error(self.peek(), msg)
    
    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

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

    
    