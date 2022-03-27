from h2py_runtime import *
x = H({'y': 5, 'z': 10})
x['y'] = 7
print(x('y') + x('z'))