import fLoxInterpreter
import time
from fLoxAst import *
import Environment


class LoxCallable(ABC):
    def call(self,interpreter,arguments):
        pass

    def arity(self):
        pass

class ClockCallable(LoxCallable):
    def call(self, interpreter, arguments):
        return float(time.time()) 

    def arity(self):
        return 0

    def __str__(self)->str:
        return "<native fn>"

class LoxFunction(LoxCallable):
    def __init__(self,declaration:Function,closure,isInitializer):
        
        super().__init__()
        self.declaration=declaration 
        self.closure=closure 
        self.isInit=isInitializer

    def call(self,interpreter,arguments:list):
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

    def arity(self):
        return len(self.declaration.params)

    def __str__(self)->str:
        return "<fn {}>".format(self.declaration.name.lexeme)

    def bind(self,instance):
        env=Environment.environment(self.closure)
        env.define("this",instance)
        return LoxFunction(self.declaration,env,self.isInit)

        