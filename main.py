import sys
from fLox import FLOX
from fLoxTokenTypes import TokenType
from fLoxToken import Token

if __name__ == "__main__":
    arguments = sys.argv
    FLOX = FLOX()
    if len(arguments) > 2:
        print("Usage: py main.py <name of lox file>")
        exit(0)
    elif len(arguments) == 2:
        FLOX.runFile(arguments[1])
    elif len(arguments) == 1:
        FLOX.runScript()