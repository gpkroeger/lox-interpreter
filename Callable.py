import interpreter
import time
from Ast import *
import Environment


class LoxCallable(ABC):
    def call(self, interpreter, arguments):
        pass

    def arity(self):
        pass

class ClockCallable(LoxCallable):

    def __str__(self)->str:
        return "<native fn>"

    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return float(time.time()) 


class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure, isInitializer):
        self.declaration=declaration 
        self.closure=closure 
        self.isInit=isInitializer

    def __str__(self)->str:
        return "<fn " + self.declaration.name.lexeme + ">"

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        env=Environment.environment(self.closure)
        
        for i in range(len(self.declaration.params)):
            env.define(self.declaration.params[i].lexeme,arguments[i])
        
        try:
            interpreter.executeBlock(self.declaration.body,env)
            if self.isInit:
                return self.closure.getAt(0,"this")
            return None

        except ReturnException as e:
            if self.isInit:
                return self.closure.getAt(0,"this")
            return e.value

    def bind(self,instance):
        env=Environment.environment(self.closure)
        env.define("this",instance)
        return LoxFunction(self.declaration,env,self.isInit)

        