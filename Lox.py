#main.py
#this will be the program that is called to start the process of py
#USAGE: python3 main.py (optional filename)
#with no fileName, this will act as a bash script
#with fileName, this will act as an interpreter for the passed .lox file

import sys
import string
from scanner import scanner
from parser import parser

class Lox:
    hadError = False

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
        # scanny = scanner(source)
        # for token in scanny.scanTokens():
        #     print(token)
        #indicate an error and exit gracefully
        if hadError:
            exit(65)

    def error(line, msg):
        report(line, "", message)
    
    def report(msg, where):
        print('[line ', line, '] Error', where, ":", message)
        hadError = True

if __name__ == "__main__":
    # print(f"Arguments count: {len(sys.argv)}")

    argv = sys.argv
    argc = len(argv)

    if argc == 1:
        Lox.runPrompt()
    elif argc == 2:
        Lox.runFile(argv[1])
    else:
        print('Error, incorrect number of arguments')
        exit(64)