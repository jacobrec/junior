import interpreter
from tokens import Token
import time
import os


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

    enviro.define(Token(None, "read", None, None), interpreter.Callable(
        # The function call
        lambda x, y: open(y[0], 'r').read(),
        lambda: 1                       # The number of arguments
    ))

    enviro.define(Token(None, "write", None, None), interpreter.Callable(
        lambda x, y: os.remove(y[0]) if y[1] is None else open(
            y[0], 'w+').write(y[1]),    # The function call
        lambda: 2                       # The number of arguments
    ))

    enviro.define(Token(None, "append", None, None), interpreter.Callable(

        lambda x, y: open(y[0], 'a+').write(y[1]),  # The function call
        lambda: 2                       # The number of arguments
    ))
