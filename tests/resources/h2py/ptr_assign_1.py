from h2py_runtime import *

def f(x_ptr):
    result = None
    x_ptr.assign(5)
    return result
x = 3
f(HAddr(('x',)))
print(x)