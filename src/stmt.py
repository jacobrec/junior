# 11:02:05 PM on January 25, 2018
from printer import stringify

# Auto generated for class Stmt
class Stmt():
	pass


# Auto generated for class Expression
class Expression(Stmt):
	def __init__(self, expr):
		self.expr = expr

	def accept(self, visitor):
		return visitor.visitExpression(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Print
class Print(Stmt):
	def __init__(self, expr):
		self.expr = expr

	def accept(self, visitor):
		return visitor.visitPrint(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Var
class Var(Stmt):
	def __init__(self, name, initializer, isConst):
		self.name = name
		self.initializer = initializer
		self.isConst = isConst

	def accept(self, visitor):
		return visitor.visitVar(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Block
class Block(Stmt):
	def __init__(self, stmts):
		self.stmts = stmts

	def accept(self, visitor):
		return visitor.visitBlock(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class If
class If(Stmt):
	def __init__(self, condition, thenBranch, elseBranch):
		self.condition = condition
		self.thenBranch = thenBranch
		self.elseBranch = elseBranch

	def accept(self, visitor):
		return visitor.visitIf(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class For
class For(Stmt):
	def __init__(self, init, condition, incr, body):
		self.init = init
		self.condition = condition
		self.incr = incr
		self.body = body

	def accept(self, visitor):
		return visitor.visitFor(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Break
class Break(Stmt):
	def __init__(self, layers):
		self.layers = layers

	def accept(self, visitor):
		return visitor.visitBreak(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Continue
class Continue(Stmt):
	def __init__(self, layers):
		self.layers = layers

	def accept(self, visitor):
		return visitor.visitContinue(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Function
class Function(Stmt):
	def __init__(self, name, args, body):
		self.name = name
		self.args = args
		self.body = body

	def accept(self, visitor):
		return visitor.visitFunction(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


