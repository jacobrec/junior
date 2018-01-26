import interpreter
from tokens import Token
import time


def addNatives(enviro):
    enviro.define(Token(None, "time", None, None), interpreter.Callable(
        lambda x, y: time.time(),       # The function call
        lambda: 0                       # The number of arguments
    ))

    enviro.define(Token(None, "print", None, None), interpreter.Callable(
        lambda x, y: print(y[0]),       # The function call
        lambda: 1                       # The number of arguments
    ))

    enviro.define(Token(None, "input", None, None), interpreter.Callable(
        lambda x, y: input(),           # The function call
        lambda: 0                       # The number of arguments
    ))
