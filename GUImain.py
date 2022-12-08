import sys
from pathlib import Path
from Lox import lox
from TokenTypes import tokType
from Token import Token

def runningFile(filename):
    fLox = lox()
    #directory = Path("tests/" + filename)
    fLox.runFile(filename.cget("text"))
