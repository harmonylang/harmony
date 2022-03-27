import harmony_model_checker.h2py.h2py_runtime as h2py_runtime

# Symbolic constants for indexing into a token.
T_TOKEN = 0
T_FILE = 1
T_LINENO = 2
T_COLNO = 3


def escape_name(name: str) -> str:
    while name in dir(h2py_runtime):
        name = f'_{name}'
    return name
