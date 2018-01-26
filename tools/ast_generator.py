import datetime


def generateGroup(output, l):
    superClass = l[0][0]
    with open(output + (superClass.lower() + ".py"), "w") as output:
        output.write("# %s\n" % (
            datetime.datetime.now().strftime("%I:%M:%S %p on %B %d, %Y")))
        output.write("from printer import stringify\n\n")
        for x in l:
            output.write(generateClass(output, superClass, x) + "\n\n")


def generateClass(output, superClass, classData):
    out = "# Auto generated for class %s\n" % classData[0]
    if not classData[1]:
        out += "class %s():\n" % classData[0]
        out += "\tpass\n"
        return out
    out += "class %s(%s):\n" % (classData[0], superClass)
    out += "\tdef __init__(self, %s):\n" % (", ".join(classData[1]))
    for field in classData[1]:
        out += "\t\tself.%s = %s\n" % (field, field)
    out += "\n\tdef accept(self, visitor):\n"
    out += "\t\treturn visitor.visit%s(self)\n" % classData[0]
    out += "\n\tdef __str__(self):\n"
    out += "\t\treturn stringify(self)\n"
    out += "\n\tdef __repr__(self):\n"
    out += "\t\treturn stringify(self)\n"

    return out


class Expr:
    pass


class Binary(Expr):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


data = [[("Expr", []),
         ("Logical", ["left", "op", "right"]),
         ("Binary", ["left", "op", "right"]),
         ("Ternary", ["left", "op1", "middle", "op2", "right"]),
         ("Grouping", ["expression"]),
         ("Literal", ["value"]),
         ("Unary", ["op", "right"]),
         ("Variable", ["name"]),
         ("Assignment", ["name", "value"]),
         ("Call", ["caller", "locTok", "args"])
         ],

        [("Stmt", []),
         ("Expression", ["expr"]),
         ("Print", ["expr"]),
         ("Var", ["name", "initializer", "isConst"]),
         ("Block", ["stmts"]),
         ("If", ["condition", "thenBranch", "elseBranch"]),
         ("For", ["init", "condition", "incr", "body"]),
         ("Break", ["locTok", "layers"]),
         ("Continue", ["locTok", "layers"]),
         ("Return", ["locTok", "value"]),
         ("Function", ["name", "args", "body"])
         ]]
if __name__ == "__main__":
    folder = "src/"
    for group in data:
        generateGroup(folder, group)
