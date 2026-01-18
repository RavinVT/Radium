from enum import Enum, auto

class TokenType(Enum):
    FUN = auto()
    VAL = auto()
    VAR = auto()
    IDENT = auto()
    INT = auto()
    STRING = auto()

    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COLON = auto()
    EQUAL = auto()
    COMMA = auto()

    EOF = auto()

    CLASS = auto()
    DOT = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()


class Token:
    def __init__(self, _type: TokenType, value=None, line=0, col=0):
        self.type = _type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"{self.type.name}({self.value})"
