from enum import Enum, auto

class TokenType(Enum):
    # Veri Tipleri ve Anahtar Kelimeler (Keywords)
    KEYWORD = auto()  # int, float, if, else, while, print
    IDENTIFIER = auto()  # x, y, result vb.

    # Literals (Sabit Değerler)
    INTEGER_LITERAL = auto()  # 10, 5
    FLOAT_LITERAL = auto()  # 3.14
    STRING_LITERAL = auto()  # "Result is large"

    # Operatörler
    ASSIGN = auto()  # =
    PLUS = auto()  # +
    MINUS = auto()  # -
    MAIN_MUL = auto()  # * (Dahili Python adıyla çakışmaması için isim)
    MUL = auto()
    DIV = auto()  # /

    # Karşılaştırma ve Mantıksal Operatörler
    EQ = auto()  # ==
    NEQ = auto()  # !=
    LT = auto()  # <
    GT = auto()  # >
    LTE = auto()  # <=
    GTE = auto()  # >=
    AND = auto()  # &&
    OR = auto()  # ||

    # Ayırıcılar (Delimiters)
    ID_COMMA = auto()
    SEMICOLON = auto()  # ;
    COMMA = auto()  # ,
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACE = auto()  # {
    RBRACE = auto()  # }

    # Özel Durum Tokenları
    EOF = auto()  # End Of File
    ERROR = auto()  # Sözcük hatası durumları için

class Token:
    def __init__(self, type_: TokenType, value: str, line: int):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Line {self.line:02d} -> {self.type.name:<16} : '{self.value}'"