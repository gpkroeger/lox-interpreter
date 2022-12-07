import sys
from pathlib import Path
from fLox import floxx
from fLoxTokenTypes import tokType
from fLoxToken import Token

if __name__ == "__main__":
    arguments = sys.argv
    floxx = floxx()
    if len(arguments) > 2:
        print("Usage: py main.py <name of lox file>")
        exit(0)
    elif len(arguments) == 2:
        directory = Path("tests/" + arguments[1])
        floxx.runFile(directory)
    elif len(arguments) == 1:
        floxx.runScript()