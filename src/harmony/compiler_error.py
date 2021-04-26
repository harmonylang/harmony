
class HarmonyCompilerError(Exception):
    def __init__(
            self,
            filename: str = None,
            token: str = None,
            error_name: str = 'Error',
            message: str = 'An error occurred',
            line: int = None,
            col: int = None,
            **kwargs
    ):
        self.token = token
        self.filename = filename
        self.error_name = error_name
        self.message = message
        self.line = line
        self.col = col
        self.metadata = kwargs

    def __repr__(self):
        return f"""\
HarmonyCompilerError(
    filename={repr(self.filename)},
    token={repr(self.token)},
    error_name={repr(self.error_name)},
    message={repr(self.message)},
    line={repr(self.line)},
    col={repr(self.col)},
    **{repr(self.metadata)})"""

    def __str__(self):
        return f"""\
HarmonyCompilerError:
    filename:  {self.filename}
    token:     {self.token}
    errorName: {self.error_name}
    message:   {self.message}
    line:      {self.line}
    column:    {self.col}
    metadata:  {self.metadata}
"""

    def as_json(self):
        import json
        return json.JSONEncoder().encode(self.__dict__)
