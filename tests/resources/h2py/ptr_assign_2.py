from h2py_runtime import *

def f(x_y_ptr):
    result = None
    x_y_ptr.assign(5)
    return result
x = H({'y': 3})
f(HAddr(('x', 'y')))
print(x('y'))