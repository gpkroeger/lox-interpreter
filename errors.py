#Need to setup runtime errors, interpreation errors, and variable errors
#testing
from tokenTypes import tokenTypes
from Token import Token

class Globals:
    iError = False
    iRuntime = False

def error(line, errorMessage):
    report(line, "", errorMessage)

def report(line, where, errorMessage):
    print("[line {line}] Error{where}: {message}")
    Globals.iError  = True

def runtimeError(error):
    print(f"line {error.token.line} Runtime error: {error.message}")
    Globals.iRuntime = True

def newError(token: Token, message):
    if token.tokenTypes == tokenTypes.EOF:
        report(token.lineNum, "at", message)
    else:
        report(token.lineNum, "at {token.lexeme}", message)

class InterpretError(Exception):
    def __init__(self, token, message):
        self.token = token
        self.message = message