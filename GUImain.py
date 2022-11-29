import sys
from pathlib import Path
from fLox import floxx
from fLoxTokenTypes import TokenType
from fLoxToken import Token

def runningFile(filename):
    fLox = floxx()
    #directory = Path("tests/" + filename)
    fLox.runFile(filename.cget("text"))
