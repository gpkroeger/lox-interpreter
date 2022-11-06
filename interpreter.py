from errors import *
from evals import *
from Token import Token
from tokenTypes import tokenTypes

class rException(Exception):
    def __init__(self, val):
        self.val = val

def isNumber(value):
    return isinstance(value, int) or isinstance(value, float)

def isEqual(left, right):
    return left == right

def isOperandNumber(token, operand):
    if isNumber(operand):
        return
    raise InterpretError(token, "Operand must be a number.")

def checkBothOperand(token, left, right):
    if isNumber(left) and isNumber(right):
        return
    raise InterpretError(token, "Operands must be numbers.")

