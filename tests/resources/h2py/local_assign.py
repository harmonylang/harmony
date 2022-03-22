from h2py_runtime import *

def f(x, y):
    result = None
    z = x + y
    print(z)
    z = None
    return result
f(3, 4)