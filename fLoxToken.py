from fLoxTokenTypes import TokenType

class Token(object):
    def __init__(self,type:TokenType,lexeme:str,literal,line:int):
        self.type=type
        self.lexeme=lexeme
        self.literal=literal
        self.line=line

    def __str__(self)->str:
        return str(self.type)+" "+self.lexeme+" "+str(self.literal)