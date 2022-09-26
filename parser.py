class parser:
    def __init__(self):
        self.finalTokens = []
        self.current = 0
    
    def parseTokens(self, tokens):
        self.finalTokens = tokens
    
    