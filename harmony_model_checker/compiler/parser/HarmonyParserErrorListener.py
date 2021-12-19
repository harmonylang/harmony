from antlr4.error.ErrorListener import ErrorListener

from harmony_model_checker.compiler.exception import HarmonyCompilerError


class HarmonyParserErrorListener(ErrorListener):
    def __init__(self, filename: str):
        super(HarmonyParserErrorListener, self).__init__()
        self.filename = filename

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        lexeme = offending_symbol.text
        line = offending_symbol.line
        column = offending_symbol.column
        raise HarmonyCompilerError(
            filename=self.filename,
            lexeme=lexeme,
            message="Syntax Error",
            line=line,
            column=column
        )
