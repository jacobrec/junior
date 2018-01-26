# 08:40:00 AM on January 26, 2018
from printer import stringify

# Auto generated for class Expr
class Expr():
	pass


# Auto generated for class Logical
class Logical(Expr):
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def accept(self, visitor):
		return visitor.visitLogical(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Binary
class Binary(Expr):
	def __init__(self, left, op, right):
		self.left = left
		self.op = op
		self.right = right

	def accept(self, visitor):
		return visitor.visitBinary(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Ternary
class Ternary(Expr):
	def __init__(self, left, op1, middle, op2, right):
		self.left = left
		self.op1 = op1
		self.middle = middle
		self.op2 = op2
		self.right = right

	def accept(self, visitor):
		return visitor.visitTernary(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Grouping
class Grouping(Expr):
	def __init__(self, expression):
		self.expression = expression

	def accept(self, visitor):
		return visitor.visitGrouping(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Literal
class Literal(Expr):
	def __init__(self, value):
		self.value = value

	def accept(self, visitor):
		return visitor.visitLiteral(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Unary
class Unary(Expr):
	def __init__(self, op, right):
		self.op = op
		self.right = right

	def accept(self, visitor):
		return visitor.visitUnary(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Variable
class Variable(Expr):
	def __init__(self, name):
		self.name = name

	def accept(self, visitor):
		return visitor.visitVariable(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Assignment
class Assignment(Expr):
	def __init__(self, name, value):
		self.name = name
		self.value = value

	def accept(self, visitor):
		return visitor.visitAssignment(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


# Auto generated for class Call
class Call(Expr):
	def __init__(self, caller, locTok, args):
		self.caller = caller
		self.locTok = locTok
		self.args = args

	def accept(self, visitor):
		return visitor.visitCall(self)

	def __str__(self):
		return stringify(self)

	def __repr__(self):
		return stringify(self)


