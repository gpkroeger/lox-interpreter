from fLoxTokenTypes import tokType

class Token(object):
    def __init__(self,type:tokType,lexeme:str,literal,line:int):
        self.type=type
        self.lexeme=lexeme
        self.literal=literal
        self.line=line

    def __str__(self)->str:
        return str(self.type)+" "+self.lexeme+" "+str(self.literal)