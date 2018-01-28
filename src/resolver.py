import interpreter


def resolve(ast):
    i = interpreter.Interpreter()
    r = Resolver(i)

    for stmt in ast:
        r.resolve(stmt)
        # try:
        #     r.resolve(stmt)
        # except RuntimeError as e:
        #     junior.runtimeError(e.tok, e.msg)


class Resolver():
    def __init__(self, interp):
        self.interpreter = interp
        self.scopes = []

    def visitBlock(self, stmt):
        self.beginScope()
        for s in stmt.stmts:
            self.resolve(s)
        self.endScope()

    def visitVar(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve(stmt.initializer)
        self.define(stmt.name)

    def visitFunction(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolveFunction(stmt)

    def visitVariable(self, expr):
        if len(self.scopes) > 0 and not self.scopes[-1][expr.name.lexeme]:
            self.error(expr.name, "Cannot access variable before assignement")
        self.resolveLocal(expr)

    def visitAssignment(self, expr):
        self.resolve(expr.value)
        self.resolveLocal(expr)

    def resolve(self, stmt):
        stmt.accept(self)

    def resolveLocal(self, expr):
        ss = list(reversed(self.scopes))
        for x in range(len(ss)):
            if expr.name.lexeme in ss[x].keys():
                self.interpreter.resolve(expr, len(self.scopes) - 1 - x)
                break

    def resolveFunction(self, func):
        self.beginScope()
        for param in func.args:
            self.declare(param)
            self.define(param)
        # for s in func.body:
        self.resolve(func.body)
        self.endScope()

    def beginScope(self):
        self.scopes.append({})

    def endScope(self):
        self.scopes.pop()

    def define(self, name):
        if len(self.scopes) > 0:
            self.scopes[-1][name.lexeme] = True

    def declare(self, name):
        if len(self.scopes) > 0:
            self.scopes[-1][name.lexeme] = False

    def visitExpression(self, stmt):
        self.resolve(stmt.expr)

    def visitIf(self, stmt):
        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)
        try:
            self.resolve(stmt.elseBranch)
        except AttributeError:
            pass  # else is not a thing

    def visitContinue(self, stmt):
        if stmt.value is not None:
            self.resolve(stmt.value)

    def visitBreak(self, stmt):
        if stmt.value is not None:
            self.resolve(stmt.value)

    def visitReturn(self, stmt):
        if stmt.value is not None:
            self.resolve(stmt.value)

    def visitFor(self, stmt):  # TODO: try catch this later
        self.resolve(stmt.init)
        self.resolve(stmt.condition)
        self.resolve(stmt.incr)
        self.resolve(stmt.body)

    def visitBinary(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visitCall(self, expr):
        for arg in expr.args:
            self.resolve(arg)

    def visitGrouping(sefl, expr):
        sefl.resolve(expr.expression)

    def visitLogical(self, expr):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visitUnary(self, expr):
        self.resolve(expr.right)

    def visitLiteral(self, expr):
        pass
