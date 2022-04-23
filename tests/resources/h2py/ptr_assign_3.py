from h2py_runtime import *

def f(x, z):
    result = None
    x.get()['y'] = z
    return result
d = H({'y': 5})
f(HAddr('d'), 7)
assert d('y') == 7