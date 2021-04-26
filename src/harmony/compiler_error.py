
class HarmonyCompilerError(Exception):
    def __init__(
            self,
            error_name: str = 'Error',
            line: int = 0,
            col: int = 0,
            **kwargs
    ):
        self.error_name = error_name
        self.line = line
        self.col = col
        self.metadata = kwargs

    def __repr__(self):
        return f"""\
HarmonyCompilerError(
    error_name={repr(self.error_name)},
    line={repr(self.line)},
    col={repr(self.col)},
    **{repr(self.metadata)})"""

    def __str__(self):
        return f"""\
HarmonyCompilerError:
    errorName: {self.error_name}
    line:      {self.line}
    column:    {self.col}
    metadata:  {self.metadata}
"""

    def as_json(self):
        import json
        return json.JSONEncoder().encode(self.__dict__)
