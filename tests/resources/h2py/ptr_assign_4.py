from h2py_runtime import *
memory = H({0: None, 1: None, 2: None})
idx = 0

def malloc():
    result = None
    result = HAddr(('memory', idx))
    idx = idx + 1
    return result

def malloc_init(x):
    result = None
    result = malloc()
    result.assign(x)
    return result
x = malloc_init('Hello!')
assert x.get() == 'Hello!'
y = malloc_init('Goodbye!')
assert y.get() == 'Goodbye!'
