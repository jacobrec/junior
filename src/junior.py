import lexer
import parser
import interpreter
from tokens import TokenType
from printer import printAst
import sys
import readline

hadError = False
hadRuntimeError = False


def main():
    if len(sys.argv) > 2:
        print("Usage: Junior [file]")
    elif len(sys.argv) == 2:
        runFile(sys.argv[1])
    else:
        runPrompt()


def runPrompt():
    print("### Junior Interpreter ###")
    print("Built in functions: @quit, @help")
    i = interpreter.Interpreter()

    line = ""
    while True:
        line = input(">>> ")
        if line == "@quit":
            return
        elif line == "@help":
            print("TODO: add help here")
        else:
            run(line, i)
            hadError = False


def runFile(fileName):
    with open(fileName, 'r') as f:
        run(f.read())
    if hadError:
        sys.exit(65)


def run(inp, interp=None):

    val = interpreter.interpret(parser.parse(lexer.lex(inp)), interp)
    if val is not None:
        print(chr(187) + " " + str(val))


def error(token, message):
    if token.type == TokenType.EOF:
        report(token.line, "", message)
    else:
        report(token.line, " at '" + token.lexeme + "'", message)


def runtimeError(token, message):
    print("[line %d] Runtime Error on %s: %s" %
          (token.line, token.type, message))


def report(line, where, message):
    print("[line %d] Error%s: %s" % (line, where, message))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("@quit")
