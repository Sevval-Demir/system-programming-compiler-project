class ASTNode:
    """Tüm AST düğümlerinin türeyeceği taban sınıf."""
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements  # Program içindeki tüm satırların listesi

class DeclarationNode(ASTNode):
    def __init__(self, data_type, var_name, line):
        self.data_type = data_type   # 'int' veya 'float'
        self.var_name = var_name     # Değişken adı
        self.line = line             # Semantic analiz için satır bilgisi

class AssignmentNode(ASTNode):
    def __init__(self, var_name, expr, line):
        self.var_name = var_name     # Atama yapılan değişken adı
        self.expr = expr             # Atanan matematiksel/mantıksal ifade (ASTNode)
        self.line = line

class BinOpNode(ASTNode):
    """İki taraflı işlemleri tutar (+, -, *, /, >, ==, &&, || vb.)"""
    def __init__(self, left, op_token, right):
        self.left = left             # Sol tarafın düğümü (ASTNode)
        self.op_token = op_token     # Operatörün kendisi (Token nesnesi)
        self.right = right           # Sağ tarafın düğümü (ASTNode)

class UnaryOpNode(ASTNode):
    """Tek taraflı işlemleri tutar (Örn: -x veya -5 gibi negatif sayılar)"""
    def __init__(self, op_token, expr):
        self.op_token = op_token     # Eksi (-) token nesnesi
        self.expr = expr             # Değer/İfade düğümü

class LiteralNode(ASTNode):
    """Sayıları ve String sabitlerini tutar."""
    def __init__(self, token):
        self.token = token           # INTEGER_LITERAL, FLOAT_LITERAL veya STRING_LITERAL
        self.value = token.value

class VariableNode(ASTNode):
    """Değişken kullanımlarını tutar."""
    def __init__(self, token):
        self.token = token
        self.var_name = token.value

class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition     # Koşul ifadesi (ASTNode)
        self.then_branch = then_branch # If bloğu içi (Statement listesi)
        self.else_branch = else_branch # Else bloğu içi (Statement listesi veya None)

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition     # Döngü koşulu (ASTNode)
        self.body = body               # Döngü içi (Statement listesi)

class PrintNode(ASTNode):
    def __init__(self, argument, line):
        self.argument = argument       # Ekrana basılacak ifade (ASTNode)
        self.line = line


def export_ast_text(node, level=0):
    """
    AST yapısını hiyerarşik ve girintili bir metin (string) olarak döndürür.
    Tkinter arayüzünde ağacı göstermek için bu fonksiyonu kullanacağız.
    """
    if node is None:
        return ""

    indent = "    " * level
    branch = "├── " if level > 0 else ""
    result = ""
    node_type = type(node).__name__

    if node_type == "ProgramNode":
        result += "Program\n"
        for stmt in node.statements:
            result += export_ast_text(stmt, level + 1)

    elif node_type == "DeclarationNode":
        result += f"{indent}{branch}Declaration: {node.data_type} {node.var_name}\n"

    elif node_type == "AssignmentNode":
        result += f"{indent}{branch}Assignment: {node.var_name} =\n" + export_ast_text(node.expr, level + 1)

    elif node_type == "BinOpNode":
        result += f"{indent}{branch}BinaryOp: '{node.op_token.value}'\n" + export_ast_text(node.left, level + 1) + export_ast_text(node.right, level + 1)

    elif node_type == "UnaryOpNode":
        result += f"{indent}{branch}UnaryOp: '{node.op_token.value}'\n" + export_ast_text(node.expr, level + 1)

    elif node_type == "LiteralNode":
        result += f"{indent}{branch}Literal: {node.value}\n"

    elif node_type == "VariableNode":
        result += f"{indent}{branch}Variable: {node.var_name}\n"

    elif node_type == "IfNode":
        result += f"{indent}{branch}IfStatement\n{indent}    ├── Condition:\n" + export_ast_text(node.condition, level + 2) + f"{indent}    └── ThenBranch:\n"
        for stmt in node.then_branch:
            result += export_ast_text(stmt, level + 3)
        if node.else_branch:
            result += f"{indent}    └── ElseBranch:\n"
            for stmt in node.else_branch:
                result += export_ast_text(stmt, level + 3)

    elif node_type == "WhileNode":
        result += f"{indent}{branch}WhileLoop\n{indent}    ├── Condition:\n" + export_ast_text(node.condition, level + 2) + f"{indent}    └── Body:\n"
        for stmt in node.body:
            result += export_ast_text(stmt, level + 3)

    elif node_type == "PrintNode":
        result += f"{indent}{branch}PrintStatement\n" + export_ast_text(node.argument, level + 1)

    return result