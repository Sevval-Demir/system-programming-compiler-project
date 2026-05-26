from lexer.token import Token, TokenType

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.position = 0
        self.line = 1

        self.keywords = {
            "int",
            "float",
            "if",
            "else",
            "while",
            "print"
        }

        self.errors = []

    def get_current_char(self):
        """Mevcut karakteri döndürür. Kaynak kod bittiyse None döner."""
        if self.position >= len(self.source_code):
            return None
        return self.source_code[self.position]

    def advance(self):
        """Bir karakter ileri gider."""
        self.position += 1

    def peek(self):
        """Bir sonraki karaktere bakar ama ilerlemez."""
        peek_pos = self.position + 1
        if peek_pos >= len(self.source_code):
            return None
        return self.source_code[peek_pos]

    def skip_whitespace_and_comments(self):
        """Boşlukları, yeni satırları ve yorumları atlar."""
        while True:
            current = self.get_current_char()
            if current is None:
                break

            if current == '\n':
                self.line += 1
                self.advance()
            elif current.isspace():
                self.advance()
            # Tek satırlı yorumlar -> //
            elif current == '/' and self.peek() == '/':
                while self.get_current_char() is not None and self.get_current_char() != '\n':
                    self.advance()
            else:
                break

    def read_number(self):
        """Integer veya float literal okur."""
        result = ""
        is_float = False

        while True:
            current = self.get_current_char()
            if current and current.isdigit():
                result += current
                self.advance()
            elif current == '.' and not is_float:
                is_float = True
                result += current
                self.advance()

                # DÜZELTİLDİ: Noktadan sonra sayı gelmiyorsa (Örn: 15.) bozuk karakteri tüketip çıkıyoruz
                if not (self.get_current_char() and self.get_current_char().isdigit()):
                    error_msg = f"Line {self.line}: Malformed float literal '{result}'"
                    self.errors.append(error_msg)
                    return Token(TokenType.ERROR, result, self.line)
            else:
                break

        # Fazladan nokta kontrolü (Örn: 12.3.4)
        if self.get_current_char() == '.':
            while self.get_current_char() is not None and (self.get_current_char().isdigit() or self.get_current_char() == '.'):
                result += self.get_current_char()
                self.advance()

            error_msg = f"Line {self.line}: Malformed number '{result}'"
            self.errors.append(error_msg)
            return Token(TokenType.ERROR, result, self.line)

        if is_float:
            return Token(TokenType.FLOAT_LITERAL, result, self.line)
        return Token(TokenType.INTEGER_LITERAL, result, self.line)

    def read_identifier_or_keyword(self):
        """Identifier veya keyword okur."""
        result = ""
        while True:
            current = self.get_current_char()
            if current and (current.isalnum() or current == '_'):
                result += current
                self.advance()
            else:
                break

        if result in self.keywords:
            return Token(TokenType.KEYWORD, result, self.line)
        return Token(TokenType.IDENTIFIER, result, self.line)

    def read_string(self):
        """String literal okur."""
        start_line = self.line
        self.advance()  # Açılış tırnağını geç
        result = ""

        while True:
            current = self.get_current_char()

            if current is None:
                error_msg = f"Line {start_line}: Unterminated string literal"
                self.errors.append(error_msg)
                return Token(TokenType.ERROR, result, start_line)

            if current == '\n':
                error_msg = f"Line {start_line}: String literal cannot span multiple lines"
                self.errors.append(error_msg)
                return Token(TokenType.ERROR, result, start_line)

            if current == '"':
                self.advance()  # Kapanış tırnağını geç
                break

            result += current
            self.advance()

        return Token(TokenType.STRING_LITERAL, result, start_line)

    def tokenize(self):
        """Tüm kaynak kodu tokenize eder."""
        tokens = []

        while True:
            self.skip_whitespace_and_comments()
            current = self.get_current_char()

            if current is None:
                tokens.append(Token(TokenType.EOF, "EOF", self.line))
                break

            if current.isalpha() or current == '_':
                tokens.append(self.read_identifier_or_keyword())
                continue

            if current.isdigit():
                tokens.append(self.read_number())
                continue

            if current == '"':
                tokens.append(self.read_string())
                continue

            # =========================================================
            # OPERATORS & DELIMITERS (DÜZELTİLDİ: advance/continue dengesi)
            # =========================================================
            if current == '=':
                if self.peek() == '=':
                    self.advance(); self.advance()
                    tokens.append(Token(TokenType.EQ, "==", self.line))
                else:
                    self.advance()
                    tokens.append(Token(TokenType.ASSIGN, "=", self.line))
                continue

            elif current == '!':
                if self.peek() == '=':
                    self.advance(); self.advance()
                    tokens.append(Token(TokenType.NEQ, "!=", self.line))
                else:
                    self.errors.append(f"Line {self.line}: Invalid character '!'")
                    tokens.append(Token(TokenType.ERROR, "!", self.line))
                    self.advance()
                continue

            elif current == '<':
                if self.peek() == '=':
                    self.advance(); self.advance()
                    tokens.append(Token(TokenType.LTE, "<=", self.line))
                else:
                    self.advance()
                    tokens.append(Token(TokenType.LT, "<", self.line))
                continue

            elif current == '>':
                if self.peek() == '=':
                    self.advance(); self.advance()
                    tokens.append(Token(TokenType.GTE, ">=", self.line))
                else:
                    self.advance()
                    tokens.append(Token(TokenType.GT, ">", self.line))
                continue

            elif current == '&':
                if self.peek() == '&':
                    self.advance(); self.advance()
                    tokens.append(Token(TokenType.AND, "&&", self.line))
                else:
                    # DÜZELTİLDİ: Tek başına olan '&' karakteri hatasından sonra imleç tamamen tüketiliyor
                    self.errors.append(f"Line {self.line}: Invalid character '&'")
                    tokens.append(Token(TokenType.ERROR, "&", self.line))
                    self.advance()
                continue

            elif current == '|':
                if self.peek() == '|':
                    self.advance(); self.advance()
                    tokens.append(Token(TokenType.OR, "||", self.line))
                else:
                    # DÜZELTİLDİ: Tek başına olan '|' karakteri hatasından sonra imleç tamamen tüketiliyor
                    self.errors.append(f"Line {self.line}: Invalid character '|'")
                    tokens.append(Token(TokenType.ERROR, "|", self.line))
                    self.advance()
                continue

            elif current == '+':
                self.advance()
                tokens.append(Token(TokenType.PLUS, "+", self.line))
                continue
            elif current == '-':
                self.advance()
                tokens.append(Token(TokenType.MINUS, "-", self.line))
                continue
            elif current == '*':
                self.advance()
                tokens.append(Token(TokenType.MUL, "*", self.line))
                continue
            elif current == '/':
                self.advance()
                tokens.append(Token(TokenType.DIV, "/", self.line))
                continue
            elif current == ';':
                self.advance()
                tokens.append(Token(TokenType.SEMICOLON, ";", self.line))
                continue
            elif current == ',':
                self.advance()
                tokens.append(Token(TokenType.COMMA, ",", self.line))
                continue
            elif current == '(':
                self.advance()
                tokens.append(Token(TokenType.LPAREN, "(", self.line))
                continue
            elif current == ')':
                self.advance()
                tokens.append(Token(TokenType.RPAREN, ")", self.line))
                continue
            elif current == '{':
                self.advance()
                tokens.append(Token(TokenType.LBRACE, "{", self.line))
                continue
            elif current == '}':
                self.advance()
                tokens.append(Token(TokenType.RBRACE, "}", self.line))
                continue
            else:
                error_msg = f"Line {self.line}: Invalid character '{current}'"
                self.errors.append(error_msg)
                tokens.append(Token(TokenType.ERROR, current, self.line))
                self.advance()
                continue

        return tokens, self.errors