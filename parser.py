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
            if self.match(tokenTypes.CLASS):
                return self.declareClass()
            if self.match(tokenTypes.FUN):
                return self.function("function")
            if self.match(tokenTypes.VAR):
                return self.declareVariable()

            return self.statement()
        except parseError:
            self.synchronize()
            return None

    def declareClass(self):
        name = self.consume(tokenTypes.IDENTIFIER, "Expect class name.")
        sClass = None
        if self.match(tokenTypes.LESS):
            self.consume(tokenTypes.IDENTIFIER, "Expect superclass name")
            sClass = Variable(self.previous())
        self.consume(tokenTypes.LEFT_BRACE, "Expect '{' before class body.")
        methods = []
        while not self.check(tokenTypes.RIGHT_BRACE) and not self.is_at_end():
            methods.append(self.function("method"))
        self.consume(tokenTypes.RIGHT_BRACE, "Expect '}' after class body.")
        return Class(name, sClass, methods)

    def declareVariable(self):
        name = self.consume(tokenTypes.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(tokenTypes.EQUAL):
            initializer = self.expression()
        self.consume(tokenTypes.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def function(self, kind):
        name = self.consume(tokenTypes.IDENTIFIER, f"Expect {kind} name.")
        self.consume(tokenTypes.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []
        if not self.check(tokenTypes.RIGHT_PAREN):
            parameters.append(self.consume(tokenTypes.IDENTIFIER, "Expect parameter name."))

            while self.match(tokenTypes.COMMA):
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")
                parameters.append(
                    self.consume(tokenTypes.IDENTIFIER, "Expect parameter name.")
                )
        self.consume(tokenTypes.RIGHT_PAREN, f"Expect ')' after {kind} parameters.")
        self.consume(tokenTypes.LEFT_BRACE, "Expect '{' before the " f"{kind} body.")
        body = self.block()
        return Function(name, parameters, body)

    def parameters(self):
        return []

    def statement(self):
        if self.match(tokenTypes.RETURN):
            return self.returnStatement()
        if self.match(tokenTypes.PRINT):
            return self.printStatement()
        if self.match(tokenTypes.IF):
            return self.ifStatement()
        if self.match(tokenTypes.WHILE):
            return self.whileStatement()
        if self.match(tokenTypes.FOR):
            return self.forStatement()
        if self.match(tokenTypes.LEFT_BRACE):
            return Block(self.block())

        return self.expressionStatement()

    def returnStatement(self):
        keyword = self.previous()
        value = None
        if not self.check(tokenTypes.SEMICOLON):
            value = self.expression()
        self.consume(tokenTypes.SEMICOLON, "Expect ';' after return value.")
        return Return(keyword, value)

    def ifStatement(self):
        self.consume(tokenTypes.LEFT_PAREN, "Expect '(' after 'if'")
        condition = self.expression()
        self.consume(tokenTypes.RIGHT_PAREN, "Expect ')' after if condition.")
        then_branch = self.statement()
        else_branch = None
        if self.match(tokenTypes.ELSE):
            else_branch = self.statement()
        return If(condition, then_branch, else_branch)

    def printStatement(self):
        expr = self.expression()
        self.consume(tokenTypes.SEMICOLON, "Expect ';' after value.")
        return Print(expr)

    def whileStatement(self):
        self.consume(tokenTypes.LEFT_PAREN, "Expect '(' after 'while'")
        condition = self.expression()
        self.consume(tokenTypes.RIGHT_PAREN, "Expect ')' after while condition.")

        return While(condition, self.statement())

    def forStatement(self):
        self.consume(tokenTypes.LEFT_PAREN, "Expect '(' after 'for'")
        if self.match(tokenTypes.SEMICOLON):
            initializer = None
        elif self.match(tokenTypes.VAR):
            initializer = self.declareVariable()
        else:
            initializer = self.expressionStatement()

        if self.check(tokenTypes.SEMICOLON):
            condition = None
        else:
            condition = self.expression()
        self.consume(tokenTypes.SEMICOLON, "Expect ';' after for condition.")

        if self.check(tokenTypes.RIGHT_PAREN):
            increment = None
        else:
            increment = self.expression()
        self.consume(tokenTypes.RIGHT_PAREN, "Expect ')' after for clauses.")
        body = self.statement()
        initializer_list: List[Stmt] = [] if initializer is None else [initializer]
        condition_expr = Literal(True) if condition is None else condition
        increment_list: List[Stmt] = ([] if increment is None else [Expression(increment)])
        return Block( initializer_list + [While(condition_expr, Block([body] + increment_list))])

    def expression(self):
        return self.assignment()

    def block(self):
        statements = []
        while not self.check(tokenTypes.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(tokenTypes.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def expressionStatement(self):
        expr = self.expression()
        self.consume(tokenTypes.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)
    
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

    def primary(self) -> Expr:
        if self.match(tokenTypes.FALSE):
            return Literal(False)
        elif self.match(tokenTypes.TRUE):
            return Literal(True)
        elif self.match(tokenTypes.NIL):
            return Literal(None)
        elif self.match(tokenTypes.NUMBER, tokenTypes.STRING):
            return Literal(self.previous().literal)
        elif self.match(tokenTypes.THIS):
            return This(self.previous())
        elif self.match(tokenTypes.SUPER):
            keyword = self.previous()
            self.consume(tokenTypes.DOT, "Expect '.' after 'super'")
            method = self.consume(tokenTypes.IDENTIFIER, "Expect superclass method name")
            return Super(keyword, method)
        elif self.match(tokenTypes.IDENTIFIER):
            return Variable(self.previous())
        elif self.match(tokenTypes.LEFT_PAREN):
            expr = self.expression()
            self.consume(tokenTypes.RIGHT_PAREN, "Expect ')' after expression")
            return Grouping(expr)
        else:
            raise self.error(self.peek(), "Expect expression")

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().ttype == tokenTypes.SEMICOLON:
                return
            if self.peek().ttype in {
                tokenTypes.CLASS,
                tokenTypes.FUN,
                tokenTypes.VAR,
                tokenTypes.FOR,
                tokenTypes.IF,
                tokenTypes.WHILE,
                tokenTypes.PRINT,
                tokenTypes.RETURN,
            }:
                return
            self.advance()
    
    