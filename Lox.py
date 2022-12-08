from Scanner import Scanner
from Token import Token
from TokenTypes import tokType
from Ast import *
from Parser import Parser
from Resolver import Resolver
from interpreter import Interpreter


class lox(object):

    hasErrorOccured = False

    def __init__(self):
        super().__init__()
        self.data = None
        self.interpreter = Interpreter()

    def runFile(self,filepath):
        with open(filepath, 'r') as file:
            self.data = file.read()
        self.run(self.data)
        if lox.hasErrorOccured:
            exit(65)
    
    def runPrompt(self):
        while True:
            print(">", end='')
            line=input()
            self.run(line)
            lox.hasErrorOccured=False
             
    def run(self, source):
        scanner=Scanner(source)
        tokens=scanner.scanTokens()
        parser=Parser(tokens)
        statments=parser.parse()
        resolver=Resolver(self.interpreter)
        if lox.hasErrorOccured:
            return;
        resolver.resolve(statments)
        self.interpreter.interpret(statments)
       
    @staticmethod
    def error(line, msg):
        lox.report(line,"",msg)

    @staticmethod
    def tokenError(token, msg):
        if token.type==tokType.EOF:
            lox.report(token.line,"at end",msg)
        else:
            lox.report(token.line,"at '"+token.lexeme+"'",msg)

    @staticmethod
    def runtimeError(error):
        lox.hadError=True
        print(error.message+" [line"+str(error.token.line)+"]")

    @staticmethod
    def report(line, where, msg):
        print("line {} error, {}:{}".format(line,where,msg))
        lox.hadError=True
