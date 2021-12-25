from typing import Any


class HarmonyCompilerError(Exception):
    """
    Error encountered during the compilation of a Harmony program.
    """

    def __init__(self, message: str, filename: str = None, line: int = None,
                 column: int = None, lexeme: Any = None, is_eof_error=False):
        self.message = message
        self.token = {
            "line": line,
            "message": message,
            "column": column,
            "lexeme": str(lexeme),
            "filename": filename,
            "is_eof_error": is_eof_error
        }
