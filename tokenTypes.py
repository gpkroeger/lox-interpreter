from enum import Enum, auto

class tokenTypes(Enum):
    #single character tokens
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    #either one or two character tokens
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    #literals
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    #keywords
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    #EOF
    EOF = auto()

keywords = {
    "and":tokenTypes.AND,
    "class":tokenTypes.CLASS,
    "else":tokenTypes.ELSE,
    "false":tokenTypes.FALSE,
    "fun":tokenTypes.FUN,
    "for":tokenTypes.FOR,
    "if":tokenTypes.IF,
    "nil":tokenTypes.NIL,
    "or":tokenTypes.OR,
    "print":tokenTypes.PRINT,
    "return":tokenTypes.RETURN,
    "super":tokenTypes.SUPER,
    "this":tokenTypes.THIS,
    "tru":tokenTypes.TRUE,
    "var":tokenTypes.VAR,
    "while":tokenTypes.WHILE
}