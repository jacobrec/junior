class AstPrinter():

    def visitVar(self, stmt):
        return self.wrap("Variable= ", stmt.name, stmt.value)

    def visitExpression(self, stmt):
        return self.wrap("Expr", stmt.expr)

    def visitAssignment(self, stmt):
        print("assign")
        return self.wrap("Variable= ",  stmt.name, stmt.value)

    def visitPrint(self, stmt):
        return self.wrap("Print", stmt.name, stmt.initializer)

    def visitVariable(self, stmt):
        return self.wrap("Variable: ", stmt.name)

    def visitTernary(self, expr):
        return self.wrap(expr.op1.lexeme, expr.left, expr.middle, expr.right)

    def visitBinary(self, expr):
        return self.wrap(expr.op.lexeme, expr.left, expr.right)

    def visitGrouping(self, expr):
        return self.wrap("Group", expr.expression)

    def visitLiteral(self, expr):
        if expr.value is None:
            return "nil"
        else:
            return str(expr.value)

    def visitUnary(self, expr):
        return self.wrap(expr.op.lexeme, expr.right)

    def wrap(self, name, *inner):
        return "(%s %s)" % (name, " ".join(list(map(lambda x: x.accept(self), inner))))

    def getString(self, stmt):
        return stmt.accept(self)


def printAst(stmts):
    print(stringify(stmts))


def stringify(stmt):
    return AstPrinter().getString(stmt)
