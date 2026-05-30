from parser.ast_nodes import (
    ProgramNode, DeclarationNode, AssignmentNode, BinOpNode,
    UnaryOpNode, LiteralNode, VariableNode, IfNode, WhileNode, PrintNode
)
from lexer.token import TokenType

class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.errors = []

    def analyze(self, root_node):
        self.visit(root_node)
        return self.errors

    def visit(self, node):
        if node is None:
            return None
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    def visit_ProgramNode(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_DeclarationNode(self, node):
        success = self.symbol_table.insert(node.var_name, node.data_type)
        if not success:
            self.errors.append(
                f"Line {node.line}: Semantic Error - Duplicate declaration. Variable '{node.var_name}' is already declared."
            )

    def visit_AssignmentNode(self, node):
        var_symbol = self.symbol_table.lookup(node.var_name)
        if var_symbol is None:
            self.errors.append(
                f"Line {node.line}: Semantic Error - Undeclared variable. Variable '{node.var_name}' must be declared before assignment."
            )
            return

        expr_type = self.visit(node.expr)

        # Katı tip güvenliği sağlandı. Hem int<-float hem de sayısal değişkenlere string ataması engellendi!
        if var_symbol.type == "int" and expr_type == "float":
            self.errors.append(
                f"Line {node.line}: Semantic Error - Type mismatch. Cannot assign float value to int variable '{node.var_name}'."
            )
        elif var_symbol.type in ("int", "float") and expr_type == "string":
            self.errors.append(
                f"Line {node.line}: Semantic Error - Type mismatch. Cannot assign string value to numeric variable '{node.var_name}'."
            )

    def visit_BinOpNode(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type == "string" or right_type == "string":
            return "string"
        if left_type == "float" or right_type == "float":
            return "float"
        if node.op_token.type in (TokenType.EQ, TokenType.NEQ, TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE,
                                  TokenType.AND, TokenType.OR):
            return "int"
        return "int"

    def visit_UnaryOpNode(self, node):
        return self.visit(node.expr)

    def visit_LiteralNode(self, node):
        if node.token.type == TokenType.INTEGER_LITERAL:
            return "int"
        elif node.token.type == TokenType.FLOAT_LITERAL:
            return "float"
        elif node.token.type == TokenType.STRING_LITERAL:
            return "string"
        return None

    def visit_VariableNode(self, node):
        symbol = self.symbol_table.lookup(node.var_name)
        if symbol is None:
            self.errors.append(
                f"Line {node.token.line}: Semantic Error - Undeclared variable. Variable '{node.var_name}' used in expression is not declared."
            )
            return "int"
        return symbol.type

    def visit_IfNode(self, node):
        self.visit(node.condition)
        for stmt in node.then_branch: self.visit(stmt)
        if node.else_branch:
            for stmt in node.else_branch: self.visit(stmt)

    def visit_WhileNode(self, node):
        self.visit(node.condition)
        for stmt in node.body: self.visit(stmt)

    def visit_PrintNode(self, node):
        self.visit(node.argument)