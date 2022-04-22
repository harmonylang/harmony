from h2py_runtime import *

def f(x):
    result = None
    x.get()('y').get()['z'] = 7
    result = x.get()('y').get()('w')
    return result
a = H({'w': 5, 'z': 10})
x = H({'y': HAddr('a')})
assert f(HAddr('x')) == 5
assert a('z') == 7