#main.py
#this will be the program that is called to start the process of py
#USAGE: python3 main.py (optional filename)
#with no fileName, this will act as a bash script
#with fileName, this will act as an interpreter for the passed .lox file

import sys
import string
from scanner import scanner
from parser import parser
from errors import *

def runFile(fileName):
    inputFile = open(fileName, 'r')
    rawText = inputFile.read()
    run(rawText)

def runPrompt():
    while True:
        line = input("> ")
        if not line or len(line) == 0:
            break
        run(line)
        hadError = False

def run(source):
    Scanner = scanner(source)
    tokens = Scanner.scanTokens()
    Parser = parser(tokens)
    res = parser.parse()

    if res is None or Globals.iError:
        return

if __name__ == "__main__":
    # print(f"Arguments count: {len(sys.argv)}")

    argv = sys.argv
    argc = len(argv)

    if argc == 1:
        runPrompt()
    elif argc == 2:
        runFile(argv[1])
    else:
        print('Error, incorrect number of arguments')
        exit(64)