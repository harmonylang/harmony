from h2py_runtime import *
x = choose(H({'y': 5, 'z': 7}))
assert x == 5 or x == 7