from h2py_runtime import *
x = H({'a': 5, 'b': H({'c': 7})})
y = HAddr('x')
z = HAddr((y, 'a'))
y = HAddr(('x', 'b'))
z = HAddr((y, 'c'))
y = HAddr((('x', 'b'), 'c'))