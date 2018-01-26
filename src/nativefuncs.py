import interpreter
from tokens import Token
import time


def addNatives(enviro):
    enviro.define(Token(None, "time", None, None), interpreter.Callable(
        lambda x, y: time.time(),       # The function call
        lambda: 0                       # The number of arguments
    ))
