import sys
from pathlib import Path
from fLox import floxx
from fLoxTokenTypes import tokType
from fLoxToken import Token

def runningFile(filename):
    fLox = floxx()
    #directory = Path("tests/" + filename)
    fLox.runFile(filename.cget("text"))
