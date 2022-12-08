import time
from Ast import *

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




        