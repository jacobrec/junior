from tokens import TokenType
from tokens import Token
import junior
import time
import nativefuncs


class Interpreter():
    def __init__(self):
        self.globals = Enviroment()
        self.enviroment = self.globals

        nativefuncs.addNatives(self.globals)

    def visitVar(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.enviroment.define(stmt.name, value, stmt.isConst)
        return value

    def visitAssignment(self, stmt):
        value = self.evaluate(stmt.value)
        self.enviroment.assign(stmt.name, value)
        return value

    def visitExpression(self, stmt):
        value = self.evaluate(stmt.expr)
        return value

    def visitIf(self, stmt):
        val = None
        if self.evaluate(stmt.condition):
            val = self.evaluate(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            val = self.evaluate(stmt.elseBranch)
        return val

    def visitFor(self, stmt):
        if stmt.init is not None:
            self.evaluate(stmt.init)
        while True if stmt.condition is None else self.evaluate(stmt.condition):
            try:
                self.evaluate(stmt.body)
                if stmt.incr is not None:
                    self.evaluate(stmt.incr)
            except JExit as l:
                if l.amount > 1:
                    l.amount -= 1
                    raise l
                elif l.type == TokenType.CONTINUE:
                    if stmt.incr is not None:
                        self.evaluate(stmt.incr)
                    continue
                elif l.type == TokenType.BREAK:
                    break
                else:
                    raise l
        return None

    def visitContinue(self, stmt):
        raise JExit(TokenType.CONTINUE, stmt.layers.value)

    def visitBreak(self, stmt):
        raise JExit(TokenType.BREAK, stmt.layers.value)

    def visitReturn(self, stmt):
        raise JExit(TokenType.RETURN, 1, self.evaluate(stmt.value))

    def visitPrint(self, stmt):
        value = self.evaluate(stmt.expr)
        print(str(value))

    def visitCall(self, expr):
        func = self.evaluate(expr.caller)
        if hasattr(func, "call"):
            args = [self.evaluate(x) for x in expr.args]

            if len(args) != func.argNum():
                raise RuntimeError(
                    expr.locTok, "Expected %d arguments but you only gave me %d"
                    % (func.argNum(), len(args)))
            return func.call(self, args)
        raise RuntimeError(expr.locTok, "not a callable object")

    def visitFunction(self, stmt):
        func = Function(stmt, self.enviroment)
        if stmt.name is not None:
            self.enviroment.define(stmt.name, func)
            return None
        return func

    def visitBlock(self, block):
        return self.executeBlock(block.stmts, Enviroment(enclosing=self.enviroment))

    def visitVariable(self, expr):
        return self.enviroment.get(expr.name)

    def visitTernary(self, expr):
        left = self.evaluate(expr.left)
        middle = self.evaluate(expr.middle)
        right = self.evaluate(expr.right)

        if expr.op1.type is TokenType.QUESTION and expr.op2.type is TokenType.COLON:
            return middle if left else right

        return None

    def visitLogical(self, expr):
        left = self.evaluate(expr.left)
        if expr.op.type is TokenType.AND_AND:
            if not left:
                return left
        elif expr.op.type is TokenType.OR_OR:
            if left:
                return left

        return self.evaluate(expr.right)

    def visitBinary(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.op.type is TokenType.MINUS:
            try:
                return left - right
            except TypeError:
                self.error(expr.op, "Invalid types")
        elif expr.op.type is TokenType.SLASH:
            try:
                return left / right
            except TypeError:
                self.error(expr.op, "Invalid types")
        elif expr.op.type is TokenType.STAR:
            try:
                return left * right
            except TypeError:
                self.error(expr.op, "Invalid types")
        elif expr.op.type is TokenType.PERCENT:
            try:
                return left % right
            except TypeError:
                self.error(expr.op, "Invalid types")
        elif expr.op.type is TokenType.PLUS:
            try:
                return left + right
            except TypeError:
                self.error(expr.op, "Invalid types")
        elif expr.op.type is TokenType.GREATER:
            try:
                return left > right
            except TypeError:
                self.error(expr.op, "Invalid types")
        elif expr.op.type is TokenType.GREATER_EQUAL:
            try:
                return left >= right
            except TypeError:
                self.error(expr.op, "Invalid types")
        elif expr.op.type is TokenType.LESS:
            try:
                return left < right
            except TypeError:
                self.error(expr.op, "Invalid types")
        elif expr.op.type is TokenType.LESS_EQUAL:
            try:
                return left <= right
            except TypeError:
                self.error(expr.op, "Invalid types")
        elif expr.op.type is TokenType.EQUAL_EQUAL:
            try:
                return left == right
            except TypeError:
                self.error(expr.op, "Invalid types")
        elif expr.op.type is TokenType.BANG_EQUAL:
            try:
                return left != right
            except TypeError:
                self.error(expr.op, "Invalid types")

        return None

    def visitGrouping(self, expr):
        return self.evaluate(expr.expression)

    def visitLiteral(self, expr):
        return expr.value

    def visitUnary(self, expr):
        right = self.evaluate(expr.right)
        if expr.op.type is TokenType.MINUS:
            try:
                return -right
            except TypeError:
                self.error(expr.op, "Operand must be a number")
        elif expr.op.type is TokenType.BANG:
            return not right

        return None

    def executeBlock(self, stmts, enviro):
        prev = self.enviroment
        try:
            self.enviroment = enviro
            for stmt in stmts:
                self.evaluate(stmt)
        except JExit as l:
            raise l
        finally:
            self.enviroment = prev

    def error(self, token, message):
        raise RuntimeError(token, message)

    def evaluate(self, expr):
        return expr.accept(self)


class RuntimeError(Exception):
    def __init__(self, tok, msg):
        self.msg = msg
        self.tok = tok


def interpret(stmts, interp=None):
    if interp is None:
        interp = Interpreter()

    if len(stmts) == 1:
        try:
            return interp.evaluate(stmts[0])
        except RuntimeError as e:
            junior.runtimeError(e.tok, e.msg)
            return None
    else:
        for stmt in stmts:
            try:
                interp.evaluate(stmt)
            except RuntimeError as e:
                # print(e)
                junior.runtimeError(e.tok, e.msg)
    return None


class Enviroment():
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.__values = {}
        self.__consts = []

    def define(self, name, value, isConst=False):
        if name.lexeme in self.__values:
            raise RuntimeError(
                name, "Variable %s already defined" % name.lexeme)
            return
        if isConst:
            self.__consts.append(name.lexeme)
        self.__values[name.lexeme] = value

    def assign(self, name, value):
        if name.lexeme in self.__consts:
            raise RuntimeError(
                name, "Constant %s cannot be changed" % name.lexeme)
            return
        elif name.lexeme in self.__values:
            self.__values[name.lexeme] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise RuntimeError(name, "Undefined variable %s" % name.lexeme)

    def get(self, name):
        try:
            return self.__values[name.lexeme]
        except KeyError:
            if self.enclosing is not None:
                return self.enclosing.get(name)
            else:
                raise RuntimeError(name, "Undefined variable %s" % name.lexeme)

    def __str__(self):
        return str(self.__values)


class Callable():
    def __init__(self, call, argNum):
        self.call = call
        self.argNum = argNum


class Function():
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def call(self, interpreter, args):
        enviro = Enviroment(self.closure)
        for x in range(len(self.declaration.args)):
            enviro.define(self.declaration.args[x], args[x])

        try:
            interpreter.executeBlock(self.declaration.body.stmts, enviro)
        except JExit as e:
            if e.type == TokenType.RETURN:
                return e.value
            else:
                raise e

    def argNum(self):
        return len(self.declaration.args)


class JExit(Exception):
    def __init__(self, type, amount, value=None):
        self.type = type
        self.amount = amount
        self.value = value
