
class Token:
    def __init__(self, tokType, lexeme, literal, lineNum):
        self.tokType = tokType
        self.lexeme = lexeme
        self.literal = literal
        self.lineNum = lineNum
    
    def __str__(self):
        return f'Identifier: {self.tokType} Lexeme: {self.lexeme} Literal Value: {self.literal}'
