from typing import List
from antlr4.error.ErrorListener import ErrorListener

from harmony_model_checker.exception import ErrorToken
from harmony_model_checker.parser.HarmonyParser import HarmonyParser

class HarmonyLexerErrorListener(ErrorListener):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.errors: List[ErrorToken] = []

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        lexeme = str(offending_symbol.text) if offending_symbol and hasattr(offending_symbol, 'text') else ""
        self.errors.append(ErrorToken(
            filename=self.filename,
            lexeme=lexeme,
            message=msg,
            line=line,
            column=column,
            is_eof_error=False
        ))

class HarmonyParserErrorListener(ErrorListener):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.errors: List[ErrorToken] = []

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        lexeme = offending_symbol.text
        line = offending_symbol.line
        column = offending_symbol.column

        if offending_symbol.type == HarmonyParser.INDENT:
            self.errors.append(ErrorToken(
                filename=self.filename,
                lexeme=lexeme,
                message="Indentation error",
                line=line,
                column=column,
                is_eof_error=False
            ))
            return

        self.errors.append(ErrorToken(
            filename=self.filename,
            lexeme=lexeme,
            message=msg,
            line=line,
            column=column,
            is_eof_error=False
        ))
