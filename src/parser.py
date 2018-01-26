import junior
from tokens import TokenType
from tokens import Token
import expr as Expr
import stmt as Stmt

errorEndTokens = [
    TokenType.CLASS,
    TokenType.FUNCTION,
    TokenType.CLASS,
    TokenType.VAR,
    TokenType.FOR,
    TokenType.IF,
    TokenType.PRINT,
    TokenType.RETURN
]


def parse(lexTokens):
    return Parser(lexTokens).parse()


class Parser():
    def __init__(self, toks):
        self.toks = toks
        self.current = 0

    def declaration(self):
        if self.match(TokenType.VAR, TokenType.CONST):
            return self.varDeclaration(self.peek(-1))
        if self.match(TokenType.FUNCTION):
            return self.function("function")
        return self.statement()

    def varDeclaration(self, tok):
        init = None
        tok = self.peek(-1).type
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name")
        if self.match(TokenType.EQUAL):
            init = self.expression()
        return Stmt.Var(name, init, False if tok == TokenType.VAR else True)

    def function(self, type):
        name = self.consume(TokenType.IDENTIFIER, "Expect %s name" % type)
        args = []

        self.consume(TokenType.LEFT_PAREN,
                     "Expect '(' in %s declaration" % type)

        while not self.check(TokenType.RIGHT_PAREN):
            args.append(self.consume(TokenType.IDENTIFIER,
                                     "Expected parameter name"))
            self.match(TokenType.COMMA)
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters")
        if len(args) > 250:
            self.error(peek(), "Too many arguments")

        self.consume(TokenType.LEFT_BRACE,
                     "requires block after %s declaration" % type)
        body = self.blockStatement()

        return Stmt.Function(name, args, body)

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.printStatement()
        elif self.match(TokenType.LEFT_BRACE):
            return self.blockStatement()
        elif self.match(TokenType.IF):
            return self.ifStatement()
        elif self.match(TokenType.FOR):
            return self.forStatement()
        elif self.match(TokenType.BREAK):
            return self.breakStatement()
        elif self.match(TokenType.CONTINUE):
            return self.breakStatement("continue")
        elif self.match(TokenType.RETURN):
            return self.returnStatement()

        return self.expressionStatement()

    def printStatement(self):
        value = self.expression()
        return Stmt.Print(value)

    def expressionStatement(self):
        value = self.expression()
        return Stmt.Expression(value)

    def ifStatement(self):
        condition = self.expression()
        self.consume(TokenType.LEFT_BRACE, "requires block after if statement")
        thenBranch = self.blockStatement()

        elseBranch = None
        if self.match(TokenType.ELSE):
            self.consume(TokenType.LEFT_BRACE,
                         "requires block after else statement")
            elseBranch = self.blockStatement()

        return Stmt.If(condition, thenBranch, elseBranch)

    def forStatement(self):

        init = None
        cond = None
        incr = None

        if self.match(TokenType.LEFT_BRACE):  # infinite loop
            return Stmt.Block([Stmt.For(init, cond, incr, self.blockStatement())])
        elif self.match(TokenType.COMMA):
            first = None
        elif self.match(TokenType.VAR, TokenType.CONST):
            first = self.varDeclaration(self.peek(-1))
        else:
            first = self.expressionStatement()

        if self.match(TokenType.LEFT_BRACE):  # while loop
            return Stmt.Block([Stmt.For(None, first, None, self.blockStatement())])

        init = first
        self.consume(TokenType.COMMA,
                     "requires comma between initilizer and condition")
        if not self.match(TokenType.COMMA):
            cond = self.expression()
        else:
            cond = Expr.Literal(True)

        self.consume(TokenType.COMMA,
                     "requires comma between condition and increment")
        if not self.check(TokenType.RIGHT_BRACE):
            incr = self.expression()

        self.consume(TokenType.LEFT_BRACE, "requires block after for loop")

        return Stmt.Block([Stmt.For(init, cond, incr, self.blockStatement())])

    def breakStatement(self, type="break"):
        locTok = self.peek(-1)
        try:
            l = self.expression()
        except ParseError:
            l = Expr.Literal(1)

        if type == "continue":
            return Stmt.Continue(locTok, l)
        elif type == "break":
            return Stmt.Break(locTok, l)

    def returnStatement(self):
        locTok = self.peek(-1)
        try:
            val = self.expression()
        except ParseError:
            val = None
        return Stmt.Return(locTok, val)

    def blockStatement(self):
        return Stmt.Block(self.block())

    def block(self):
        stmts = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            stmts.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return stmts

    def expression(self):
        return self.assignment()

    def assignment(self):
        left = self.ternary()
        if self.match(TokenType.EQUAL):
            equals = self.peek(-1)
            value = self.assignment()
            if isinstance(left, Expr.Variable):
                return Expr.Assignment(left.name, value)
            self.error(equals, "Invalid assignment target.")

        elif self.match(TokenType.PLUS_EQUAL, TokenType.MINUS_EQUAL):
            tok = TokenType.MINUS
            if self.peek(-1).type == TokenType.PLUS_EQUAL:
                tok = TokenType.PLUS

            identifier = self.peek(-2)
            val = self.expression()

            return Expr.Assignment(Expr.Variable(identifier).name,
                                   Expr.Binary(Expr.Variable(identifier),
                                               Token(tok, None, None, None), val))
        return left

    def ternary(self):
        expr = self.logical_or()
        while self.match(TokenType.QUESTION):
            op1 = self.peek(-1)
            middle = self.logical_or()
            self.consume(TokenType.COLON, "Missing ':' in ternary")
            op2 = self.peek(-1)

            right = self.logical_or()
            expr = Expr.Ternary(expr, op1, middle, op2, right)
        return expr

    def logical_or(self):
        expr = self.logical_and()
        while self.match(TokenType.OR_OR):
            op = self.peek(-1)
            right = self.logical_and()
            expr = Expr.Logical(expr, op, right)
        return expr

    def logical_and(self):
        expr = self.equality()
        while self.match(TokenType.AND_AND):
            op = self.peek(-1)
            right = self.equality()
            expr = Expr.Logical(expr, op, right)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            op = self.peek(-1)
            right = self.comparison()
            expr = Expr.Binary(expr, op, right)
        return expr

    def comparison(self):
        expr = self.addition()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            op = self.peek(-1)
            right = self.addition()
            expr = Expr.Binary(expr, op, right)
        return expr

    def addition(self):
        expr = self.multiplication()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.peek(-1)
            right = self.multiplication()
            expr = Expr.Binary(expr, op, right)

        return expr

    def multiplication(self):
        expr = self.unary()
        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            op = self.peek(-1)
            right = self.unary()
            expr = Expr.Binary(expr, op, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            op = self.peek(-1)
            right = self.unary()
            return Expr.Unary(op, right)
        if self.match(TokenType.PLUS_PLUS, TokenType.MINUS_MINUS):
            return self.crement()
        return self.call()

    def call(self):
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finishCall(expr)
            else:
                break

        return expr

    def finishCall(self, expr):
        args = []
        if not self.check(TokenType.RIGHT_PAREN):
            args.append(self.expression())
            while self.match(TokenType.COMMA):
                args.append(self.expression())

        loc = self.consume(TokenType.RIGHT_PAREN, "Expecting ')' after args")

        if len(args) > 250:
            self.error(peek(), "Cannot have more than 250 arguments.")

        return Expr.Call(expr, loc, args)

    def primary(self):
        if self.match(TokenType.FALSE):
            return Expr.Literal(False)
        if self.match(TokenType.TRUE):
            return Expr.Literal(True)
        if self.match(TokenType.NIL):
            return Expr.Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.peek(-1).literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Missing ')' after expression")
            return Expr.Grouping(expr)
        if self.match(TokenType.IDENTIFIER):
            return Expr.Variable(self.peek(-1))

        raise self.error(self.peek(), "Requires an expression")

    def crement(self):
        isAdding = False
        if self.peek(-1).type == TokenType.PLUS_PLUS:
            isAdding = True

        identifier = self.peek(-2)

        if isAdding:
            tok = TokenType.PLUS
        else:
            tok = TokenType.MINUS
        val = 1

        return Expr.Assignment(Expr.Variable(identifier).name,
                               Expr.Binary(Expr.Variable(identifier),
                                           Token(tok, None, None, None), Expr.Literal(val)))

    def match(self,  *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, tokType, message):
        if self.check(tokType):
            return self.advance()

        raise self.error(self.peek(), message + " Got %s" %
                         str(self.peek().type))

    def error(self, tok, message):
        return ParseError(message, tok)

    def sync(self):
        self.advance()
        while not self.isAtEnd():
            if self.peek(-1).type == TokenType.SEMICOLON:
                return

            if self.peek() in errorEndTokens:
                return
            self.advance()

    def check(self, type):
        if self.isAtEnd():
            return False
        else:
            return self.peek().type == type

    def peek(self, skip=0):
        return self.toks[self.current + skip]

    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.peek(-1)

    def isAtEnd(self):
        return self.peek().type == TokenType.EOF

    def parse(self):
        stmts = []
        while not self.isAtEnd():
            try:
                stmts.append(self.declaration())
            except ParseError as e:
                junior.error(e.tok, e.msg)
                self.sync()
        return stmts


class ParseError(Exception):
    def __init__(self, msg, tok):
        self.msg = msg
        self.tok = tok
