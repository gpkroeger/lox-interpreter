import sys
from pathlib import Path
from Lox import lox
from TokenTypes import tokType
from Token import Token

def runningFile(filename):
    NLox = lox()
    #directory = Path("tests/" + filename)
    NLox.runFile(filename.cget("text"))
