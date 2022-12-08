from Ast import *
import Lox

class Parser:
    def __init__(self, tokens, *args, **kwargs):
        self.tokens=tokens
        self.current=0 

    def isAtEnd(self):
        return self.peek().type is tokType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current-1]

    def advance(self):
        if not self.isAtEnd():
            self.current+=1
        return self.previous()

    def check(self,type:tokType):
        if self.isAtEnd():
            return False
        return self.peek().type==type

    
    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True 
        return False

    def consume(self,type, message):
        if self.check(type):
            return self.advance()
        next=self.peek()
        raise self.error(next,message)

    def error(self,token,message):
        Lox.lox.tokenError(token,message)
        return ParseError()

    
    def expression(self):
        return self.assignment()

    def assignment(self):
        expr=self.logic_OR()

        if self.match(tokType.EQUAL):
            equals=self.previous()
            value=self.assignment()
            if type(expr) is Variable:
                name=expr.name
                return Assign(name,value)

            elif isinstance(expr,Get):
                return Set(expr.obj,expr.name,value)

            else:
                self.error(equals,"Invalid assignment target.")
        return expr

    def logic_OR(self):
        expr=self.logic_AND()
        while self.match(tokType.OR):
            operator=self.previous()
            right=self.logic_AND()
            expr=Logical(expr,operator,right)
        return expr

    
    def logic_AND(self):
        expr=self.equality()
        while self.match(tokType.AND):
            operator=self.previous()
            right=self.equality()
            expr=Logical(expr,operator,right)
        return expr


    def equality(self):
        
        expr=self.comparison()
        while self.match(tokType.BANG_EQUAL,tokType.EQUAL_EQUAL):
            operator=self.previous()
            right=self.comparison()
            expr=Binary(expr,operator,right)
        return expr

    def comparison(self):
        expr=self.term()
        while self.match(tokType.GREATER,tokType.GREATER_EQUAL,tokType.LESS,tokType.LESS_EQUAL):
            operator=self.previous()
            right=self.term()
            expr=Binary(expr,operator,right)
        return expr

    def term(self):
        expr=self.factor()
        while self.match(tokType.MINUS,tokType.PLUS):
            operator=self.previous()
            right=self.factor()
            expr=Binary(expr,operator,right)
        return expr

    def factor(self):
        expr=self.unary()
        while self.match(tokType.SLASH,tokType.STAR):
            operator=self.previous()
            right=self.unary()
            expr=Binary(expr,operator,right)
        return expr 

    def unary(self):
        if self.match(tokType.BANG,tokType.MINUS):
            operator=self.previous()
            right=self.unary()
            return Unary(operator,right)
        else:
            return self.call()

    def call(self):
        expr=self.primary()
        while True:
            if self.match(tokType.LEFT_PAREN):
                expr=self.finishCall(expr)
            elif self.match(tokType.DOT):
                name=self.consume(tokType.IDENTIFIER,"Expected property name after '.'")
                expr=Get(expr,name)
            else:
                break
        return expr

    def finishCall(self,callee):
        arguments=[]
        if not self.check(tokType.RIGHT_PAREN):
            while True:
                if len(arguments)>=255:
                    self.error(self.peek(),"Can't handle more than 255 arguments. Reduce arguments.")
                arguments.append(self.expression())
                if not self.match(tokType.COMMA):
                    break
        paren=self.consume(tokType.RIGHT_PAREN,"Expected ')' after arguments.")
        return Call(callee,paren,arguments)

    

    def primary(self):
        if self.match(tokType.FALSE):
            return Literal(False)
        elif self.match(tokType.TRUE):
            return Literal(True)
        elif self.match(tokType.NIL):
            return Literal(None)
        elif self.match(tokType.NUMBER,tokType.STRING):
            return Literal(self.previous().literal)
        elif self.match(tokType.SUPER):
            keyword=self.previous()
            self.consume(tokType.DOT,"Expect '.' after 'super'")
            method=self.consume(tokType.IDENTIFIER,"Expect superclass method name")
            return Super(keyword,method)
        elif self.match(tokType.THIS):
            return This(self.previous())
        elif self.match(tokType.IDENTIFIER):
            return Variable(self.previous())
        elif self.match(tokType.LEFT_PAREN):
            expr=self.expression() 
            self.consume(tokType.RIGHT_PAREN,'Expect ) after expression.')
            return Grouping(expr)
        
        
        raise self.error(self.peek(),"Expect expression.")

    
    
    def synchornize(self):
        self.advance() 
        while not self.isAtEnd():
            if self.previous().type==tokType.SEMICOLON:
                return
            typeToStart=[tokType.CLASS,tokType.FUN,tokType.VAR,tokType.FOR,tokType.IF,tokType.WHILE,tokType.PRINT,tokType.RETURN]
            if self.peek().type in typeToStart:
                
                return
            self.advance()

    def parse(self):
        statments=[] 
        while not self.isAtEnd():
            statments.append(self.declaration())
        return statments

    
    def statment(self):
        if self.match(tokType.PRINT):
            return self.printStatment()
        if self.match(tokType.RETURN):
            return self.returnStatment()
        if self.match(tokType.WHILE):
            return self.whileStatment()
        if self.match(tokType.LEFT_BRACE):
            return Block(self.block())
        if self.match(tokType.FOR):
            return self.forStatment()
        if self.match(tokType.IF):
            return self.ifStatment()
        return self.expressionStatment()

    def declaration(self):
        try:
            if self.match(tokType.FUN):
                return self.function("function")
            elif self.match(tokType.CLASS):
                return self.classDeclaration()
            elif self.match(tokType.VAR):
                return self.varDeclaration()
            else:
                return self.statment()
        except ParseError as e:
            self.synchornize()

    def printStatment(self):
        value=self.expression()
        self.consume(tokType.SEMICOLON,"Expect ';' after value")
        return Print(value)
        

    def expressionStatment(self):
        expr=self.expression()
        self.consume(tokType.SEMICOLON,"Expect ';' after value")
        return Expression(expr)

    def varDeclaration(self):
        name=self.consume(tokType.IDENTIFIER,"Expect variable name")
        initializer=None
        if self.match(tokType.EQUAL):
            initializer=self.expression() 
        self.consume(tokType.SEMICOLON,"Expect ';' after variable declatation")
        return Var(name,initializer)

    def block(self):
        statments=[]
        while not self.isAtEnd() and not self.check(tokType.RIGHT_BRACE):
            statments.append(self.declaration())
        self.consume(tokType.RIGHT_BRACE,"Expect '}' after block.")
        return statments

    def ifStatment(self):
        self.consume(tokType.LEFT_PAREN,"Expect '(' after 'if'.")
        condition=self.expression()
        self.consume(tokType.RIGHT_PAREN,"Expect ')' after if condition")
        thenBranch=self.statment()
        elseBranch=None
        if self.match(tokType.ELSE):
            elseBranch=self.statment()
        return If(condition,thenBranch,elseBranch)

    def whileStatment(self):
        self.consume(tokType.LEFT_PAREN,"Expect '(' after 'while'.")
        condition=self.expression()
        self.consume(tokType.RIGHT_PAREN,"Expect ')' after while condition")
        body=self.statment()
        return While(condition,body)

    def forStatment(self):
        self.consume(tokType.LEFT_PAREN,"Expect '(' after 'for'.")
        initializer=None
        condition=None
        increment=None
        if self.match(tokType.SEMICOLON): 
            initializer=None
        elif self.match(tokType.VAR):
            initializer=self.varDeclaration()
        else:
            initializer=self.expressionStatment()
        if not self.check(tokType.SEMICOLON):
            condition=self.expression()
        self.consume(tokType.SEMICOLON,"Expect ; after loop condition")
        
        if not self.check(tokType.RIGHT_PAREN):
            increment=self.expression()
        self.consume(tokType.RIGHT_PAREN,"Expect ) after for clauses")
        
        body=self.statment()
        if increment is not None :
            body=Block([body,Expression(increment)])
        if condition is None:
            condition=Literal(True)
        body=While(condition,body)
        if initializer is not None:
            body=Block([initializer,body])
        return body 

    
    def function(self,kind):
        name=self.consume(tokType.IDENTIFIER,"Expect {} name".format(kind))
        self.consume(tokType.LEFT_PAREN,"Expect '(' after {} name".format(kind))
        parameters=[]
        if not self.check(tokType.RIGHT_PAREN):
            while True:
                if len(parameters)>=255:
                    self.error(self.peek(),"Can not have too many params")
                parameters.append(self.consume(tokType.IDENTIFIER,"Expect patameter name"))
                if not self.match(tokType.COMMA):
                    break
        self.consume(tokType.RIGHT_PAREN,"Expect ')' after params.")
        self.consume(tokType.LEFT_BRACE,"Expect fun blocks")
        body=self.block()
        return Function(name,parameters,body)

    def returnStatment(self):
        keyword=self.previous()
        value=None
        if not self.check(tokType.SEMICOLON):
            value=self.expression()
        self.consume(tokType.SEMICOLON,"Expect ';' after rtn value")
        return Return(keyword,value)

    def classDeclaration(self):
        name=self.consume(tokType.IDENTIFIER,"Expect Class Name")
        superclass=None
        if self.match(tokType.LESS):
            self.consume(tokType.IDENTIFIER,"Expect Super name")
            superclass=Variable(self.previous())
        self.consume(tokType.LEFT_BRACE,"Expect { before class body")
        methods=[]
        while not self.check(tokType.RIGHT_BRACE) and not self.isAtEnd():
            methods.append(self.function("method"))
        self.consume(tokType.RIGHT_BRACE,"Expect } after class body")
        return Class(name,superclass,methods)
