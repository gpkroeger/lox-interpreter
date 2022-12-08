import sys
from pathlib import Path
from Lox import lox
from TokenTypes import tokType
from Token import Token

if __name__ == "__main__":
    arguments = sys.argv
    lox = lox()
    if len(arguments) > 2:
        print("Usage: py main.py <name of lox file>")
        exit(0)
    elif len(arguments) == 2:
        directory = Path("tests/" + arguments[1])
        lox.runFile(directory)
    elif len(arguments) == 1:
        lox.runScript()