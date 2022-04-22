from h2py_runtime import *

def f(x):
    result = None
    result = x.get()('y')
    return result
x = H({'y': 5})
assert f(HAddr('x')) == 5