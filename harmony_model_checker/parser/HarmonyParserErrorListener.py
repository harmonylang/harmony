from typing import List
from antlr4.error.ErrorListener import ErrorListener

from harmony_model_checker.exception import ErrorToken, HarmonyCompilerError


class HarmonyParserErrorListener(ErrorListener):
    def __init__(self, filename: str):
        super(HarmonyParserErrorListener, self).__init__()
        self.filename = filename
        self.errors: List[ErrorToken] = []

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        lexeme = offending_symbol.text
        line = offending_symbol.line
        column = offending_symbol.column

        self.errors.append(ErrorToken(
            filename=self.filename,
            lexeme=lexeme,
            message=msg,
            line=line,
            column=column,
            is_eof_error=False
        ))
