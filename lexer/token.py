from enum import Enum, auto


class TokenType(Enum):
    # Veri Tipleri ve Anahtar Kelimeler (Keywords) [cite: 20, 21, 24, 25, 26]
    KEYWORD = auto()  # int, float, if, else, while, print [cite: 21, 24, 25, 26]
    IDENTIFIER = auto()  # x, y, result vb. [cite: 32, 33]

    # Literals (Sabit Değerler) [cite: 27]
    INTEGER_LITERAL = auto()  # 10, 5 [cite: 27]
    FLOAT_LITERAL = auto()  # 3.14 [cite: 27]
    STRING_LITERAL = auto()  # "Result is large" [cite: 27]

    # Operatörler [cite: 23]
    ASSIGN = auto()  # = [cite: 22]
    PLUS = auto()  # + [cite: 23]
    MINUS = auto()  # - [cite: 23]
    MUL = auto()  # * [cite: 23]
    DIV = auto()  # / [cite: 23]

    # Karşılaştırma ve Mantıksal Operatörler [cite: 23]
    EQ = auto()  # == [cite: 23]
    NEQ = auto()  # != [cite: 23]
    LT = auto()  # < [cite: 23]
    GT = auto()  # > [cite: 23]
    LTE = auto()  # <= [cite: 23]
    GTE = auto()  # >= [cite: 23]
    AND = auto()  # && [cite: 23]
    OR = auto()  # || [cite: 23]

    # Ayırıcılar (Delimiters) [cite: 32]
    SEMICOLON = auto()  # ;
    COMMA = auto()  # ,
    LPAREN = auto()  # (
    RPAREN = auto()  # )
    LBRACE = auto()  # {
    RBRACE = auto()  # }

    # Özel Durum Tokenları [cite: 35]
    EOF = auto()  # End Of File (Dosyanın bittiğini parser'a haber vermek için)
    ERROR = auto()  # Sözcük hatası durumları için [cite: 35]


class Token:
    def __init__(self, type_: TokenType, value: str, line: int):
        self.type = type_  # Token tipi (Örn: TokenType.KEYWORD)
        self.value = value  # Koddan kırpılan string değer (Örn: "int")
        self.line = line  # Hata raporlaması için hangi satırda olduğu [cite: 35]

    def __repr__(self):
        # Arayüzde ve terminalde düzgün hizalı görebilmek için formatlı gösterim
        return f"Line {self.line:02d} -> {self.type.name:<16} : '{self.value}'"