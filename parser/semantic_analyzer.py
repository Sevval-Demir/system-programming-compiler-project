from parser.ast_nodes import (
    ProgramNode, DeclarationNode, AssignmentNode, BinOpNode,
    UnaryOpNode, LiteralNode, VariableNode, IfNode, WhileNode, PrintNode
)
from lexer.token import TokenType


class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.errors = []  # Anlamsal hataları burada toplayacağız

    def analyze(self, root_node):
        """Ağacı yukarıdan aşağıya dolaşarak analiz işlemini başlatır."""
        self.visit(root_node)
        return self.errors

    def visit(self, node):
        """Düğümün tipine göre ilgili dinamik fonksiyonu tetikler."""
        if node is None:
            return None

        # Dinamik fonksiyon çağrısı (Örn: ProgramNode geldiyse visit_ProgramNode tetiklenir)
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_ProgramNode(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_DeclarationNode(self, node):
        """Hata 1: Duplicate Declaration Kontrolü"""
        # Sembol tablosuna eklemeyi deniyoruz
        success = self.symbol_table.insert(node.var_name, node.data_type)
        if not success:
            self.errors.append(
                f"Line {node.line}: Semantic Error - Duplicate declaration. "
                f"Variable '{node.var_name}' is already declared."
            )

    def visit_AssignmentNode(self, node):
        """Hata 2 & 3: Undeclared Variable ve Type Mismatch Kontrolü"""
        # 1. Atama yapılacak değişken sembol tablosunda var mı?
        var_symbol = self.symbol_table.lookup(node.var_name)
        if var_symbol is None:
            self.errors.append(
                f"Line {node.line}: Semantic Error - Undeclared variable. "
                f"Variable '{node.var_name}' must be declared before assignment."
            )
            return

        # 2. Atanan ifadenin (sağ tarafın) tipini çözümlüyoruz
        expr_type = self.visit(node.expr)

        # 3. Tip uyumluluğunu denetle (int değişkene float atanmasını engelle)
        if var_symbol.type == "int" and expr_type == "float":
            self.errors.append(
                f"Line {node.line}: Semantic Error - Type mismatch. "
                f"Cannot assign float value to int variable '{node.var_name}'."
            )

    def visit_BinOpNode(self, node):
        """Matematiksel ve mantıksal işlemlerin tip çözümlemesi."""
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        # Eğer taraflardan biri float ise, işlemin sonucu da float olur (Tip genişletme)
        if left_type == "float" or right_type == "float":
            return "float"

        # Mantıksal veya karşılaştırma operatörleri her zaman int (0 veya 1) döner diye simüle edebiliriz
        if node.op_token.type in (TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE,
                                  TokenType.AND, TokenType.OR):
            return "int"

        return "int"

    def visit_UnaryOpNode(self, node):
        """Negatif sayıların tipini içerideki değere göre belirler (-5 -> int, -3.14 -> float)"""
        return self.visit(node.expr)

    def visit_LiteralNode(self, node):
        """Sabit değerlerin tiplerini doğrudan token tipinden anlarız."""
        if node.token.type == TokenType.INTEGER_LITERAL:
            return "int"
        elif node.token.type == TokenType.FLOAT_LITERAL:
            return "float"
        elif node.token.type == TokenType.STRING_LITERAL:
            return "string"
        return None

    def visit_VariableNode(self, node):
        """Bir ifadenin içinde değişken kullanıldığında tablodan tipini sorgular."""
        symbol = self.symbol_table.lookup(node.var_name)
        if symbol is None:
            self.errors.append(
                f"Line {node.token.line}: Semantic Error - Undeclared variable. "
                f"Variable '{node.var_name}' used in expression is not declared."
            )
            return "int"  # Çökmeyi önlemek için varsayılan bir tip dönüyoruz
        return symbol.type

    def visit_IfNode(self, node):
        self.visit(node.condition)
        for stmt in node.then_branch:
            self.visit(stmt)
        if node.else_branch:
            for stmt in node.else_branch:
                self.visit(stmt)

    def visit_WhileNode(self, node):
        self.visit(node.condition)
        for stmt in node.body:
            self.visit(stmt)

    def visit_PrintNode(self, node):
        self.visit(node.argument)