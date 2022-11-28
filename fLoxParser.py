from fLoxAst import *
import fLox

class Parser:
    def __init__(self, tokens, *args, **kwargs):
        self.tokens=tokens
        self.current=0 

    def isAtEnd(self)->bool:
        return self.peek().type is TokenType.EOF

    def peek(self)->Token:
        return self.tokens[self.current]

    def previous(self)->Token:
        return self.tokens[self.current-1]

    def advance(self)->Token:
        if not self.isAtEnd():
            self.current+=1
        return self.previous()

    def check(self,type:TokenType)->bool:
        if self.isAtEnd():
            return False
        return self.peek().type==type

    
    def match(self, *types)->bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True 
        return False

    def consume(self,type:TokenType, message:str):
        if self.check(type):
            return self.advance()
        next=self.peek()
        raise self.error(next,message)

    def error(self,token,message):
        fLox.FLOX.tokenError(token,message)
        return ParseError()

    
    def expression(self)->Expr:
        return self.assignment()

    def assignment(self)->Expr:
        expr=self.logic_OR()

        if self.match(TokenType.EQUAL):
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

    def logic_OR(self)->Expr:
        expr=self.logic_AND()
        while self.match(TokenType.OR):
            operator=self.previous()
            right=self.logic_AND()
            expr=Logical(expr,operator,right)
        return expr

    
    def logic_AND(self)->Expr:
        expr=self.equality()
        while self.match(TokenType.AND):
            operator=self.previous()
            right=self.equality()
            expr=Logical(expr,operator,right)
        return expr


    def equality(self)->Expr:
        
        expr=self.comparison()
        while self.match(TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL):
            operator=self.previous()
            right=self.comparison()
            expr=Binary(expr,operator,right)
        return expr

    def comparison(self)->Expr:
        expr=self.term()
        while self.match(TokenType.GREATER,TokenType.GREATER_EQUAL,TokenType.LESS,TokenType.LESS_EQUAL):
            operator=self.previous()
            right=self.term()
            expr=Binary(expr,operator,right)
        return expr

    def term(self)->Expr:
        expr=self.factor()
        while self.match(TokenType.MINUS,TokenType.PLUS):
            operator=self.previous()
            right=self.factor()
            expr=Binary(expr,operator,right)
        return expr

    def factor(self)->Expr:
        expr=self.unary()
        while self.match(TokenType.SLASH,TokenType.STAR):
            operator=self.previous()
            right=self.unary()
            expr=Binary(expr,operator,right)
        return expr 

    def unary(self)->Expr:
        if self.match(TokenType.BANG,TokenType.MINUS):
            operator=self.previous()
            right=self.unary()
            return Unary(operator,right)
        else:
            return self.call()

    def call(self)->Expr:
        expr=self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr=self.finishCall(expr)
            elif self.match(TokenType.DOT):
                name=self.consume(TokenType.IDENTIFIER,"Expected property name after '.'")
                expr=Get(expr,name)
            else:
                break
        return expr

    def finishCall(self,callee:Expr)->Expr:
        arguments=[]
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments)>=255:
                    self.error(self.peek(),"Can't handle more than 255 arguments. Reduce arguments.")
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        paren=self.consume(TokenType.RIGHT_PAREN,"Expected ')' after arguments.")
        return Call(callee,paren,arguments)

    

    def primary(self)->Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        elif self.match(TokenType.TRUE):
            return Literal(True)
        elif self.match(TokenType.NIL):
            return Literal(None)
        elif self.match(TokenType.NUMBER,TokenType.STRING):
            return Literal(self.previous().literal)
        elif self.match(TokenType.SUPER):
            keyword=self.previous()
            self.consume(TokenType.DOT,"Expect '.' after 'super'")
            method=self.consume(TokenType.IDENTIFIER,"Expect superclass method name")
            return Super(keyword,method)
        elif self.match(TokenType.THIS):
            return This(self.previous())
        elif self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        elif self.match(TokenType.LEFT_PAREN):
            expr=self.expression() 
            self.consume(TokenType.RIGHT_PAREN,'Expect ) after expression.')
            return Grouping(expr)
        
        
        raise self.error(self.peek(),"Expect expression.")

    
    
    def synchornize(self):
        self.advance() 
        while not self.isAtEnd():
            if self.previous().type==TokenType.SEMICOLON:
                return
            typeToStart=[TokenType.CLASS,TokenType.FUN,TokenType.VAR,TokenType.FOR,TokenType.IF,TokenType.WHILE,TokenType.PRINT,TokenType.RETURN]
            if self.peek().type in typeToStart:
                
                return
            self.advance()

    def parse(self):
        statments=[] 
        while not self.isAtEnd():
            statments.append(self.declaration())
        return statments

    
    def statment(self)->Stmt:
        if self.match(TokenType.PRINT):
            return self.printStatment()
        if self.match(TokenType.RETURN):
            return self.returnStatment()
        if self.match(TokenType.WHILE):
            return self.whileStatment()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        if self.match(TokenType.FOR):
            return self.forStatment()
        if self.match(TokenType.IF):
            return self.ifStatment()
        return self.expressionStatment()

    def declaration(self)->Stmt:
        try:
            if self.match(TokenType.FUN):
                return self.function("function")
            elif self.match(TokenType.CLASS):
                return self.classDeclaration()
            elif self.match(TokenType.VAR):
                return self.varDeclaration()
            else:
                return self.statment()
        except ParseError as e:
            self.synchornize()

    def printStatment(self)->Stmt:
        value=self.expression()
        self.consume(TokenType.SEMICOLON,"Expect ';' after value")
        return Print(value)
        

    def expressionStatment(self)->Stmt:
        expr=self.expression()
        self.consume(TokenType.SEMICOLON,"Expect ';' after value")
        return Expression(expr)

    def varDeclaration(self)->Stmt:
        name=self.consume(TokenType.IDENTIFIER,"Expect variable name")
        initializer=None
        if self.match(TokenType.EQUAL):
            initializer=self.expression() 
        self.consume(TokenType.SEMICOLON,"Expect ';' after variable declatation")
        return Var(name,initializer)

    def block(self)->list:
        statments=[]
        while not self.isAtEnd() and not self.check(TokenType.RIGHT_BRACE):
            statments.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE,"Expect '}' after block.")
        return statments

    def ifStatment(self)->Stmt:
        self.consume(TokenType.LEFT_PAREN,"Expect '(' after 'if'.")
        condition=self.expression()
        self.consume(TokenType.RIGHT_PAREN,"Expect ')' after if condition")
        thenBranch=self.statment()
        elseBranch=None
        if self.match(TokenType.ELSE):
            elseBranch=self.statment()
        return If(condition,thenBranch,elseBranch)

    def whileStatment(self)->Stmt:
        self.consume(TokenType.LEFT_PAREN,"Expect '(' after 'while'.")
        condition=self.expression()
        self.consume(TokenType.RIGHT_PAREN,"Expect ')' after while condition")
        body=self.statment()
        return While(condition,body)

    def forStatment(self)->Stmt:
        self.consume(TokenType.LEFT_PAREN,"Expect '(' after 'for'.")
        initializer=None
        condition=None
        increment=None
        if self.match(TokenType.SEMICOLON): 
            initializer=None
        elif self.match(TokenType.VAR):
            initializer=self.varDeclaration()
        else:
            initializer=self.expressionStatment()
        if not self.check(TokenType.SEMICOLON):
            condition=self.expression()
        self.consume(TokenType.SEMICOLON,"Expect ; after loop condition")
        
        if not self.check(TokenType.RIGHT_PAREN):
            increment=self.expression()
        self.consume(TokenType.RIGHT_PAREN,"Expect ) after for clauses")
        
        body=self.statment()
        if increment is not None :
            body=Block([body,Expression(increment)])
        if condition is None:
            condition=Literal(True)
        body=While(condition,body)
        if initializer is not None:
            body=Block([initializer,body])
        return body 

    
    def function(self,kind:str)->Stmt:
        name=self.consume(TokenType.IDENTIFIER,"Expect {} name".format(kind))
        self.consume(TokenType.LEFT_PAREN,"Expect '(' after {} name".format(kind))
        parameters=[]
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters)>=255:
                    self.error(self.peek(),"Can not have too many params")
                parameters.append(self.consume(TokenType.IDENTIFIER,"Expect patameter name"))
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RIGHT_PAREN,"Expect ')' after params.")
        self.consume(TokenType.LEFT_BRACE,"Expect fun blocks")
        body=self.block()
        return Function(name,parameters,body)

    def returnStatment(self)->Stmt:
        keyword=self.previous()
        value=None
        if not self.check(TokenType.SEMICOLON):
            value=self.expression()
        self.consume(TokenType.SEMICOLON,"Expect ';' after rtn value")
        return Return(keyword,value)

    def classDeclaration(self)->Stmt:
        name=self.consume(TokenType.IDENTIFIER,"Expect Class Name")
        superclass=None
        if self.match(TokenType.LESS):
            self.consume(TokenType.IDENTIFIER,"Expect Super name")
            superclass=Variable(self.previous())
        self.consume(TokenType.LEFT_BRACE,"Expect { before class body")
        methods=[]
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            methods.append(self.function("method"))
        self.consume(TokenType.RIGHT_BRACE,"Expect } after class body")
        return Class(name,superclass,methods)

























