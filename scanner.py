import string
#from Lox import Lox
from tokenTypes import tokenTypes, keywords
from Token import Token
from errors import *

class scanner:
    def __init__(self, rawText):
        self.text = rawText
        self.tokens = []
        self.line = 1
        self.start = 0
        self.current = 0
    
    def scanTokens(self):
        while not self.atEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token( tokenTypes.EOF, "", None, self.line ))
        return self.tokens
    
    def atEnd(self):
        return self.current >= len(self.text)

    def scanToken(self):
        c = self.advance()
        #single char tokens
        if c == '(': self.addToken(tokenTypes.LEFT_PAREN)
        elif c == ')': self.addToken(tokenTypes.RIGHT_PAREN)
        elif c == '{': self.addToken(tokenTypes.LEFT_BRACE)
        elif c == '}': self.addToken(tokenTypes.RIGHT_BRACE)
        elif c == ',': self.addToken(tokenTypes.COMMA)
        elif c == '.': self.addToken(tokenTypes.DOT)
        elif c == '-': self.addToken(tokenTypes.MINUS)
        elif c == '+': self.addToken(tokenTypes.PLUS)
        elif c == ';': self.addToken(tokenTypes.SEMICOLON)
        elif c == '*': self.addToken(tokenTypes.STAR)
        #ambigous char tokens
        elif c == '!': self.addToken(tokenTypes.BANG_EQUAL if self.match('=') else tokenTypes.BANG)
        elif c == '=': self.addToken(tokenTypes.EQUAL_EQUAL if self.match('=') else tokenTypes.EQUAL)
        elif c == '<': self.addToken(tokenTypes.LESS_EQUAL if self.match('=') else tokenTypes.LESS)
        elif c == '>': self.addToken(tokenTypes.GREATER_EQUAL if self.match('=') else tokenTypes.GREATER)
        #distinguishes between comments and SLASH
        elif c == '/':
            if self.self.match('/'):
                while self.peek() != '\n' and not self.atEnd(): self.advance()
            else: self.addToken(tokenTypes.SLASH)
        #skip all whitespace
        elif c in (' ', '\r', '\t', '\n'): 
            if c == '\n': self.line+=1
        #literals
        elif c == '"': self.string()
        elif c.isdigit(): self.number()
        elif scanner.isAlnum(c): self.identifier()
        else:
            newError(self.line, "Unexpected character")

    def advance(self):
        res = self.text[self.current]
        self.current += 1
        return res
    
    def addToken(self, type, literal=None):
        res = self.text[self.start:self.current]
        self.tokens.append(Token( type, res, literal, self.line ))

    def match(self, expected):
        if self.atEnd(): return False
        if self.text[self.current] != expected: return False

        self.current+=1
        return True

    def peek(self):
        if self.atEnd(): return '\0'
        return self.text[self.current]
    
    def string(self):
        while self.peek() != '"' and not self.atEnd():
            if self.peek() == '\n': self.line+=1
            self.advance()
        
        if self.atEnd():
            newError(self.line, "Unterminated string.")
            return
        
        self.advance()

        value = self.text[self.start+1:self.current-1].strip()
        self.addToken(tokenTypes.STRING, value)

    def number(self):
        while self.peek().isdigit(): self.advance()
        
        if self.peek() == '.' and self.peekNext().isdigit():
            self.advance()
        
        while self.peek().isdigit(): self.advance()

        self.addToken(tokenTypes.NUMBER, float(self.text[self.start:self.current]))
    
    def peekNext(self):
        if self.current+1 >= len(self.text): return '\0'
        return self.text[self.current+1]

    def identifier(self):
        while scanner.isAlnum(self.peek()): 
            self.advance()

        res = self.text[self.start:self.current]
        type = tokenTypes.IDENTIFIER
        if res.lower().strip() in keywords:
            type = keywords[res.lower().strip()]
        self.addToken(type)
    
    def isAlpha(c):
        return ("a" <= c and c <= "z") or ("A" <= c and c <= "Z") or (c == "_")

    def isAlnum(c):
        return scanner.isAlpha(c) or c.isdigit()