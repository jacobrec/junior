

class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return "(%s(%s): %s)" % (str(self.type), str(self.lexeme), str(self.literal))

    def __repr__(self):
        return str(self)


class TokenType():
    # Single-character tokens
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"
    QUESTION = "?"
    COLON = ":"
    PERCENT = "%"

    # One or two character tokens
    BANG = "!"
    BANG_EQUAL = "!="
    EQUAL = "="
    EQUAL_EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="
    PLUS_PLUS = "++"
    PLUS_EQUAL = "+="
    MINUS_MINUS = "--"
    MINUS_EQUAL = "-="
    AND_AND = "&&"
    OR_OR = "||"

    # Literals
    IDENTIFIER = "ID"
    STRING = "STR"
    NUMBER = "NUM"

    # Keywords
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUNCTION = "fun"
    FOR = "for"
    GOTO = "goto"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    BREAK = "break"
    CONTINUE = "continue"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "let"
    CONST = "const"

    EOF = "EOF"
