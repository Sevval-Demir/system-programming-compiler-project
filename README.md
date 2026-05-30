# Simple Two-Pass Compiler

A simple two-pass compiler simulator developed in Python as part of the System Programming course project. The compiler was implemented manually without using compiler-generator tools such as Lex, Yacc, Flex, Bison, or ANTLR.

## Features

- Lexical Analysis (Lexer)
- Recursive Descent Parser
- Abstract Syntax Tree (AST) Generation
- Symbol Table Management
- Semantic Analysis
- Error Detection and Reporting
- Source File Loading Support
- Graphical User Interface (Tkinter)

## Supported Language Constructs

### Variable Declarations

```c
int x;
float result;
```

### Assignments

```c
x = 10;
result = x + 3.5;
```

### Arithmetic Expressions

```c
result = x + y * 2;
```

Supported operators:

```text
+  -  *  /
```

### Conditional Statements

```c
if (x > 5) {
    print("Large");
}
else {
    print("Small");
}
```

### While Loops

```c
while (x > 0) {
    x = x - 1;
}
```

### Print Statements

```c
print("Hello");
print(x);
```

## Compiler Architecture

```text
Source Code
    │
    ▼
Lexical Analysis
    │
    ▼
Token Stream
    │
    ▼
Syntax Analysis
    │
    ▼
Abstract Syntax Tree (AST)
    │
    ▼
Semantic Analysis
    │
    ▼
Symbol Table & Error Reports
```

## Project Structure

```text
compiler_project/
│
├── lexer/
│   ├── lexer.py
│   ├── token.py
│   └── symbol_table.py
│
├── parser/
│   ├── parser.py
│   ├── ast_nodes.py
│   └── semantic_analyzer.py
│
├── tests/
│   ├── sample_program
│   └── samples.json
│
├── ui/
│   └── gui.py
│
├── main.py
├── README.md
└── tokens_output.txt
```

## Running the Project

Make sure Python 3 is installed.

```bash
python main.py
```

The graphical user interface will start automatically.

## Error Detection

### Lexical Errors

- Invalid characters
- Malformed numeric literals
- Unterminated string literals
- Unsupported operators

### Syntax Errors

- Missing semicolons
- Missing parentheses
- Invalid statements
- Invalid expressions

### Semantic Errors

- Duplicate declarations
- Undeclared variables
- Type mismatches

## Example Program

```c
int x;
int y;
float result;

x = 10;
y = 3;

result = x + y * 2;

if (result > 15) {
    print("Result is large");
}
else {
    print("Result is small");
}

print(result);
```

## Technologies Used

- Python 3
- Tkinter
- Object-Oriented Programming
- Recursive Descent Parsing
- Abstract Syntax Trees (AST)

## Author

Şevval Demir

Computer Engineering Department  
İstanbul Health and Technology University

System Programming Course Project