import Callable
from Ast import *

class FLOXclass(Callable.LoxCallable):
    def __init__(self, name , superclass, methods):
        self.name=name
        self.methods=methods
        self.superclass=superclass

    def __str__(self):
        return self.name 

    def call(self, interpreter, arguments):
        instance=FLOXInstance(self)
        initializer=self.findMethod('init')

        if initializer is not None: 
            initializer.bind(instance).call(interpreter,arguments) #init
        return instance

    def findMethod(self,name):
        methods=self.methods.get(name)
        supermethods=None
        if self.superclass is not None:
            supermethods=self.superclass.findMethod(name)
        if methods!=None:
            return methods
        return supermethods

    def arity(self):
        initializer=self.findMethod('init')

        if initializer is None:
            return 0
        else:
            return initializer.arity() #init


class FLOXInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

    def __str__(self):
        return self.klass.name + " instance"  #Testing

    def get(self, name):
        if self.fields.get(name.lexeme) is not None:
            return self.fields[name.lexeme]
        method=self.klass.findMethod(name.lexeme)
        
        if method is not None:
            return method.bind(self)
        raise RunTimeError(name,"Undefined property:{}".format(name.lexeme))

    def set(self,name,value):
        self.fields[name.lexeme]=value





