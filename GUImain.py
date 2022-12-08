import sys
from pathlib import Path
from Lox import floxx
from TokenTypes import tokType
from Token import Token

def runningFile(filename):
    fLox = floxx()
    #directory = Path("tests/" + filename)
    fLox.runFile(filename.cget("text"))
