from lexer.token import TokenType
from parser.ast_nodes import (
    ProgramNode, DeclarationNode, AssignmentNode, BinOpNode,
    UnaryOpNode, LiteralNode, VariableNode, IfNode, WhileNode, PrintNode
)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.errors = []  # Sözdizim (Syntax) hatalarını burada toplayacağız

    def get_current_token(self):
        # Güvenli erişim: Token listesinin dışına taşmayı engeller
        if self.position >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.position]

    def consume(self, token_type, error_message):
        """Beklenen token tipini kontrol eder, doğruysa ilerler, yanlışsa hata kaydeder."""
        current = self.get_current_token()
        if current.type == token_type:
            self.position += 1
            return current
        else:
            self.errors.append(f"Line {current.line}: Syntax Error - {error_message}. Found '{current.value}'")
            if current.type != TokenType.EOF:
                self.position += 1
            return current

    def parse(self):
        """Derlemeyi başlatan ana fonksiyon."""
        statements = []
        while self.get_current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return ProgramNode(statements), self.errors

    def parse_statement(self):
        """BNF: <Statement> ::= <DeclarationStmt> | <AssignmentStmt> | <IfStmt> ..."""
        current_token = self.get_current_token()

        if current_token.type == TokenType.KEYWORD:
            if current_token.value in ("int", "float"):
                return self.parse_declaration_stmt()
            elif current_token.value == "if":
                return self.parse_if_stmt()
            elif current_token.value == "while":
                return self.parse_while_stmt()
            elif current_token.value == "print":
                return self.parse_print_stmt()

        elif current_token.type == TokenType.IDENTIFIER:
            return self.parse_assignment_stmt()

        else:
            self.errors.append(
                f"Line {current_token.line}: Syntax Error - Unexpected statement start '{current_token.value}'")
            self.position += 1
            return None

    def parse_declaration_stmt(self):
        """BNF: <DeclarationStmt> ::= <Type> IDENTIFIER ";" """
        type_token = self.get_current_token()
        self.position += 1

        var_token = self.consume(TokenType.IDENTIFIER, "Expected variable name after type")
        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")

        return DeclarationNode(type_token.value, var_token.value, type_token.line)

    def parse_assignment_stmt(self):
        """BNF: <AssignmentStmt> ::= IDENTIFIER "=" <Expression> ";" """
        var_token = self.get_current_token()
        self.position += 1

        self.consume(TokenType.ASSIGN, "Expected '=' after variable name")
        expr = self.parse_expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' at the end of assignment")

        return AssignmentNode(var_token.value, expr, var_token.line)

    def parse_if_stmt(self):
        """BNF: <IfStmt> ::= "if" "(" <Condition> ")" "{" <StatementList> "}" <ElsePart> """
        self.position += 1
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self.parse_condition()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")

        self.consume(TokenType.LBRACE, "Expected '{' to start 'if' block")
        then_statements = []
        while self.get_current_token().type != TokenType.RBRACE and self.get_current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt: then_statements.append(stmt)
        self.consume(TokenType.RBRACE, "Expected '}' to close 'if' block")

        else_statements = None
        if self.get_current_token().type == TokenType.KEYWORD and self.get_current_token().value == "else":
            self.position += 1
            self.consume(TokenType.LBRACE, "Expected '{' to start 'else' block")
            else_statements = []
            while self.get_current_token().type != TokenType.RBRACE and self.get_current_token().type != TokenType.EOF:
                stmt = self.parse_statement()
                if stmt: else_statements.append(stmt)
            self.consume(TokenType.RBRACE, "Expected '}' to close 'else' block")

        return IfNode(condition, then_statements, else_statements)

    def parse_while_stmt(self):
        """BNF: <WhileStmt> ::= "while" "(" <Condition> ")" "{" <StatementList> "}" """
        self.position += 1
        self.consume(TokenType.LPAREN, "Expected '(' after 'while'")
        condition = self.parse_condition()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")

        self.consume(TokenType.LBRACE, "Expected '{' to start 'while' block")
        body_statements = []
        while self.get_current_token().type != TokenType.RBRACE and self.get_current_token().type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt: body_statements.append(stmt)
        self.consume(TokenType.RBRACE, "Expected '}' to close 'while' block")

        return WhileNode(condition, body_statements)

    def parse_print_stmt(self):
        """BNF: <PrintStmt> ::= "print" "(" <PrintArgument> ")" ";" """
        print_token = self.get_current_token()
        self.position += 1
        self.consume(TokenType.LPAREN, "Expected '(' after 'print'")

        if self.get_current_token().type == TokenType.STRING_LITERAL:
            argument = LiteralNode(self.get_current_token())
            self.position += 1
        else:
            argument = self.parse_expression()

        self.consume(TokenType.RPAREN, "Expected ')' after print argument")
        self.consume(TokenType.SEMICOLON, "Expected ';' after print statement")

        return PrintNode(argument, print_token.line)

    def parse_condition(self):
        """BNF: <Condition> ::= <SimpleCondition> ( <LogicalOp> <SimpleCondition> )* """
        left = self.parse_simple_condition()

        while self.get_current_token().type in (TokenType.AND, TokenType.OR):
            op_token = self.get_current_token()
            self.position += 1
            right = self.parse_simple_condition()
            left = BinOpNode(left, op_token, right)

        return left

    def parse_simple_condition(self):
        """BNF: <SimpleCondition> ::= <Expression> <RelOp> <Expression> """
        left = self.parse_expression()
        rel_ops = (TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE)

        if self.get_current_token().type in rel_ops:
            op_token = self.get_current_token()
            self.position += 1
            right = self.parse_expression()
            return BinOpNode(left, op_token, right)
        else:
            # DÜZELTİLDİ: Koşul operatörü eksikse imleç güvenli ilerletilir, kilitlenme önlenir
            self.errors.append(f"Line {self.get_current_token().line}: Syntax Error - Expected comparison operator")
            if self.get_current_token().type != TokenType.EOF:
                self.position += 1
            return left

    def parse_expression(self):
        """BNF: <Expression> ::= <Term> ( ( "+" | "-" ) <Term> )* """
        left = self.parse_term()

        while self.get_current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.get_current_token()
            self.position += 1
            right = self.parse_term()
            left = BinOpNode(left, op_token, right)

        return left

    def parse_term(self):
        """BNF: <Term> ::= <Factor> ( ( "*" | "/" ) <Factor> )* """
        left = self.parse_factor()

        while self.get_current_token().type in (TokenType.MUL, TokenType.DIV):
            op_token = self.get_current_token()
            self.position += 1
            right = self.parse_factor()
            left = BinOpNode(left, op_token, right)

        return left

    def parse_factor(self):
        """BNF: <Factor> ::= IDENTIFIER | INTEGER_LITERAL | FLOAT_LITERAL | "(" <Expression> ")" | "-" <Factor> """
        token = self.get_current_token()

        if token.type in (TokenType.INTEGER_LITERAL, TokenType.FLOAT_LITERAL):
            self.position += 1
            return LiteralNode(token)

        elif token.type == TokenType.IDENTIFIER:
            self.position += 1
            return VariableNode(token)

        elif token.type == TokenType.MINUS:
            self.position += 1
            factor = self.parse_factor()
            return UnaryOpNode(token, factor)

        elif token.type == TokenType.LPAREN:
            self.position += 1
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN, "Expected ')' to match opening parenthesis")
            return expr

        else:
            self.errors.append(f"Line {token.line}: Syntax Error - Expected number, variable or '('")
            if token.type != TokenType.EOF:
                self.position += 1
            return None