from Scanner import Scanner
from Token import Token
from TokenTypes import tokType
from Ast import *
from Parser import Parser
from Resolver import Resolver
from interpreter import Interpreter


class lox(object):
    ErrorOccured = False
    def __init__(self):
        super().__init__()
        self.data = None
        self.interpreter = Interpreter()

    def runFile(self,filepath:str):
        with open(filepath, 'r') as file:
            self.data = file.read()
        self.run(self.data)
        if lox.ErrorOccured:
            exit(65)
    
    def runPrompt(self):
        while True:
            print(">", end='')
            line=input()
            self.run(line)
            lox.ErrorOccured=False
             

    def run(self,source:str):
        scanner=Scanner(source)
        tokens=scanner.scanTokens()
        parser=Parser(tokens)
        statments=parser.parse()
        resolver=Resolver(self.interpreter)
        if lox.ErrorOccured:
            return;
        resolver.resolve(statments)
        self.interpreter.interpret(statments)
       
    @staticmethod
    def error(line:int,message:str):
        lox.report(line,"",message)

    @staticmethod
    def tokenError(token:Token,message:str):
        if token.type==tokType.EOF:
            lox.report(token.line,"at end",message)
        else:
            lox.report(token.line,"at '"+token.lexeme+"'",message)

    @staticmethod
    def runtimeError(error:RunTimeError):
        lox.hadError=True
        print(error.message+" [line"+str(error.token.line)+"]")

    @staticmethod
    def report(line:int,where:str,message:str):
        print("line {} error, {}:{}".format(line,where,message))
        lox.hadError=True

