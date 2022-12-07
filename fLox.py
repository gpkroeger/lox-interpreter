from fLoxScanner import Scanner
from fLoxToken import Token
from fLoxTokenTypes import tokType
from fLoxAst import *
from fLoxParser import Parser
from fLoxResolver import Resolver
from fLoxInterpreter import Interpreter


class floxx(object):
    ErrorOccured = False
    def __init__(self):
        super().__init__()
        self.data = None
        self.interpreter = Interpreter()

    def runFile(self,filepath:str):
        with open(filepath, 'r') as file:
            self.data = file.read()
        self.run(self.data)
        if floxx.ErrorOccured:
            exit(65)
    
    def runPrompt(self):
        while True:
            print(">", end='')
            line=input()
            self.run(line)
            floxx.ErrorOccured=False
             

    def run(self,source:str):
        scanner=Scanner(source)
        tokens=scanner.scanTokens()
        parser=Parser(tokens)
        statments=parser.parse()
        resolver=Resolver(self.interpreter)
        if floxx.ErrorOccured:
            return;
        resolver.resolve(statments)
        self.interpreter.interpret(statments)
       
        
        
        
   
    @staticmethod
    def error(line:int,message:str):
        floxx.report(line,"",message)

    @staticmethod
    def tokenError(token:Token,message:str):
        if token.type==tokType.EOF:
            floxx.report(token.line,"at end",message)
        else:
            floxx.report(token.line,"at '"+token.lexeme+"'",message)

    @staticmethod
    def runtimeError(error:RunTimeError):
        floxx.hadError=True
        print(error.message+" [line"+str(error.token.line)+"]")

    @staticmethod
    def report(line:int,where:str,message:str):
        print("line {} error, {}:{}".format(line,where,message))
        floxx.hadError=True

