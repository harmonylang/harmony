from h2py_runtime import *

def f(x, y):
    result = None
    z = x + y
    print(x + y)
    assert z == 5
    z = None
    return result
f(2, 3)