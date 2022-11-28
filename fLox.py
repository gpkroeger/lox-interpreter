from fLoxScanner import Scanner
from fLoxToken import Token
from fLoxTokenTypes import TokenType
from fLoxAst import *
from fLoxParser import Parser
from fLoxResolver import Resolver
from fLoxInterpreter import Interpreter


class FLOX(object):
    ErrorOccured = False
    def __init__(self):
        super().__init__()
        self.data = None
        self.interpreter = Interpreter()

    def runFile(self,filepath:str):
        with open(filepath, 'r') as file:
            self.data = file.read()
        self.run(self.data)
        if FLOX.ErrorOccured:
            exit(65)
    
    def runPrompt(self):
        while True:
            print(">", end='')
            line=input()
            
            if(len(line)==0):
                print("Leaving REPL Mode...")
                break
            self.run(line)
            FLOX.ErrorOccured=False
             

    def run(self,source:str):
        scanner=Scanner(source)
        tokens=scanner.scanTokens()
        parser=Parser(tokens)
        statments=parser.parse()
        resolver=Resolver(self.interpreter)
        if FLOX.ErrorOccured:
            return;
        resolver.resolve(statments)
        self.interpreter.interpret(statments)
       
        
        
        
   
    @staticmethod
    def error(line:int,message:str):
        FLOX.report(line,"",message)

    @staticmethod
    def tokenError(token:Token,message:str):
        if token.type==TokenType.EOF:
            FLOX.report(token.line,"at end",message)
        else:
            FLOX.report(token.line,"at '"+token.lexeme+"'",message)

    @staticmethod
    def runtimeError(error:RunTimeError):
        FLOX.hadError=True
        print(error.message+" [line"+str(error.token.line)+"]")

    @staticmethod
    def report(line:int,where:str,message:str):
        print("line {} error, {}:{}".format(line,where,message))
        FLOX.hadError=True
