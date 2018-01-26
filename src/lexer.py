import junior
from tokens import TokenType
from tokens import Token

singleChar = {
    "(": TokenType.LEFT_PAREN,
    ")": TokenType.RIGHT_PAREN,
    "{": TokenType.LEFT_BRACE,
    "}": TokenType.RIGHT_BRACE,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
    "-": TokenType.MINUS,
    "+": TokenType.PLUS,
    ";": TokenType.SEMICOLON,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "!": TokenType.BANG,
    "=": TokenType.EQUAL,
    "<": TokenType.LESS,
    ">": TokenType.GREATER,
    ":": TokenType.COLON,
    "?": TokenType.QUESTION,
    "%": TokenType.PERCENT
}

multiChar = {
    "!": {"=": TokenType.BANG_EQUAL},
    "=": {"=": TokenType.EQUAL_EQUAL},
    "<": {"=": TokenType.LESS_EQUAL},
    ">": {"=": TokenType.GREATER_EQUAL},
    "+": {"+": TokenType.PLUS_PLUS, "=": TokenType.PLUS_EQUAL},
    "-": {"-": TokenType.MINUS_MINUS, "=": TokenType.MINUS_EQUAL},
    "&": {"&": TokenType.AND_AND},
    "|": {"|": TokenType.OR_OR},

}

skipChar = [" ", "\r", "\t"]

reservedWords = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "false": TokenType.FALSE,
    "for": TokenType.FOR,
    "fun": TokenType.FUNCTION,
    "goto": TokenType.GOTO,
    "if": TokenType.IF,
    "nil": TokenType.NIL,
    "or": TokenType.OR,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "break": TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "super": TokenType.SUPER,
    "this": TokenType.THIS,
    "true": TokenType.TRUE,
    "let": TokenType.VAR,
    "const": TokenType.CONST,
}


def lex(src):
    l = Lexerizer(src)
    return l.scanTokens()


class Lexerizer():
    def __init__(self, source):
        self.source = source
        self.tokens = []

        self.start = 0
        self.current = 0
        self.line = 1

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scanToken(self):
        c = self.advance()
        if c is "/" and self.peek() == "/":  # handle comments
            while self.peek() != '\n' and not self.isAtEnd():
                self.skip()  # line comment, discard the rest of the line
        elif c is "/" and self.peek() == "*":  # handle comments
            while not (self.peek() == '*' and self.peek(1) == '/') and not self.isAtEnd():
                if self.peek() == '\n':  # preserve line numbers
                    self.line += 1
                self.skip()  # block comment, discard the rest of the tokens

            self.skip(2)
        elif c is '\n':  # handle newlines
            self.line += 1
        elif c in skipChar:  # ignore whitespace
            pass
        elif c == '"':  # string literal
            self.getNextString()
        elif c.isdigit():  # number literals
            self.getNextNumber()
        elif c.isalpha():
            self.getIdentifier()
        else:  # these are characters we want to process as operators
            try:
                self.addToken(multiChar[c][self.peek()])
                self.skip()
            except KeyError:
                try:
                    self.addToken(singleChar[c])
                except KeyError:
                    junior.error(Token(None, self.source[self.start:self.current],
                                       None, self.line), "Unexpected character")

    def getIdentifier(self):
        while self.peek().isalnum():
            self.skip()
        text = self.source[self.start: self.current]
        try:
            type = reservedWords[text]
        except KeyError:
            type = TokenType.IDENTIFIER
        self.addToken(type)

    def getNextNumber(self, isNegative=False):
        # isNegative is so it's easy to later support negitive number literals
        while self.peek().isdigit():
            self.skip()

        if self.peek() == "." and self.peek(1).isdigit():
            self.skip()

        while self.peek().isdigit():
            self.skip()

        try:
            value = int(self.source[self.start:self.current])
        except ValueError:
            value = float(self.source[self.start:self.current])

        self.addToken(TokenType.NUMBER, value)

    def getNextString(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == "\n":
                self.line += 1
            self.skip()

        if self.isAtEnd():
            junior.error(self.line, "Unterminated string.")
            return

        self.skip()
        self.addToken(TokenType.STRING,
                      self.source[self.start + 1:self.current - 1])

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def skip(self, amount=1):
        self.current += amount

    def peek(self, skip=0):
        if self.current + skip >= len(self.source):
            return '\0'
        return self.source[self.current + skip]

    def addToken(self, type, literal=None):
        self.tokens.append(Token(type, self.source[self.start:self.current],
                                 literal, self.line))

    def isAtEnd(self):
        return self.current >= len(self.source)
