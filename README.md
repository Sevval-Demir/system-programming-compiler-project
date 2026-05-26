# Simple Two-Pass Compiler (Mini-Compiler Simulator)

This repository contains a hand-coded, **Two-Pass Compiler** developed for a subset of a high-level programming language as a Final Project for the **System Programming Course** (Spring 2025-2026).


---

## 🚀 Architectural Overview
The compiler is designed entirely from scratch **without using any compiler-generator tools** (such as Lex, Yacc, or ANTLR). It processes the source code through a clean, fully-modular pipeline:

1. **Pass 1 - Lexical Analysis (Lexer):** Scans the source code character-by-character, tokenizing constructs into structured keywords, identifiers, literals, and operators. It also handles initial lexical error tracking (e.g., malformed floats, unterminated strings).
2. **Symbol Table Management:** Maintains an optimized dictionary structure mapping variable names to their simulated 32-bit architectural memory addresses (incrementing by 4 bytes per variable).
3. **Pass 2 - Syntax Analysis (Parser):** Implements a manual **Recursive Descent Parser** that maps BNF grammar rules to özyinelemeli (recursive) functions, inherently resolving operator precedence.
4. **Semantic Analysis:** Traverses the generated Abstract Syntax Tree (AST) using a visitor-like pattern to enforce type compatibility, duplicate declaration checks, and undeclared variable detection.

---

## 📊 BNF Grammar Definition
```text
<Program>          ::= <StatementList>
<StatementList>    ::= <Statement> <StatementList> | ε
<Statement>        ::= <DeclarationStmt> | <AssignmentStmt> | <IfStmt> | <WhileStmt> | <PrintStmt>
<DeclarationStmt>  ::= <Type> IDENTIFIER ";"
<Type>             ::= "int" | "float"
<AssignmentStmt>   ::= IDENTIFIER "=" <Expression> ";"
<IfStmt>           ::= "if" "(" <Condition> ")" "{" <StatementList> "}" <ElsePart>
<ElsePart>         ::= "else" "{" <StatementList> "}" | ε
<WhileStmt>        ::= "while" "(" <Condition> ")" "{" <StatementList> "}"
<PrintStmt>        ::= "print" "(" <PrintArgument> ")" ";"
<PrintArgument>    ::= STRING_LITERAL | <Expression>
<Condition>        ::= <SimpleCondition> | <Condition> <LogicalOp> <SimpleCondition>
<SimpleCondition>  ::= <Expression> <RelOp> <Expression>
<LogicalOp>        ::= "&&" | "||"
<RelOp>            ::= "==" | "!=" | "<" | ">" | "<=" | ">="
<Expression>       ::= <Term> ( ( "+" | "-" ) <Term> )*
<Term>             ::= <Factor> ( ( "*" | "/" ) <Factor> )*
<Factor>           ::= IDENTIFIER | INTEGER_LITERAL | FLOAT_LITERAL | "(" <Expression> ")" | "-" <Factor>