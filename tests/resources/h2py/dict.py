from h2py_runtime import *
x = H({'y': 5, 'z': 10})
print(x('y') + x('z'))