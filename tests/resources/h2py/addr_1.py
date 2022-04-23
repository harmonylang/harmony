from h2py_runtime import *
x = H({'a': 5})
y = HAddr('x')
z = HAddr((y, 'a'))
z.assign(7)
assert x('a') == 7