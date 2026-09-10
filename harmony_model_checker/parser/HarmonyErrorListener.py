from typing import List
from antlr4.error.ErrorListener import ErrorListener  # type: ignore

from harmony_model_checker.exception import ErrorToken
from harmony_model_checker.parser.HarmonyParser import HarmonyParser

class HarmonyLexerErrorListener(ErrorListener):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.errors: List[ErrorToken] = []

    def _is_duplicate(self, line, column, message: str) -> bool:
        # ANTLR can report the same underlying failure twice for one bad
        # spot in the input: once while an ambiguous rule (like nary_expr,
        # whose alternatives all start with expr_rule) speculatively
        # predicts which alternative to take by simulating a full parse
        # ahead of time, and again when the real, non-speculative parse
        # reaches the same dead end for real. Both are genuine ANTLR error
        # reports (not a bug in error *recovery* - recovery's own normal
        # suppression doesn't apply across these two independent passes),
        # but they describe the exact same spot in the source, so only the
        # first is worth showing a person. See e.g. "?5" and other invalid
        # '?' operands (or, for that matter, a bare "?" or an unterminated
        # expression), which route through nary_expr's speculative
        # prediction on the way to question_operand.
        return bool(self.errors) and (self.errors[-1].line, self.errors[-1].column, self.errors[-1].message) == (line, column, message)

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        lexeme = str(offending_symbol.text) if offending_symbol and hasattr(offending_symbol, 'text') else ""
        message = str(msg) + " syntax error"
        column = column + 1
        if self._is_duplicate(line, column, message):
            return
        self.errors.append(ErrorToken(
            filename=self.filename,
            lexeme=lexeme,
            message=message,
            line=line,
            column=column,
            is_eof_error=False
        ))

class HarmonyParserErrorListener(ErrorListener):
    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename
        self.errors: List[ErrorToken] = []

    def _is_duplicate(self, line, column, message: str) -> bool:
        # See the matching comment on HarmonyLexerErrorListener above -
        # same phenomenon, at the parser level, where it's far more common:
        # any rule ANTLR can't decide between via plain lookahead (nary_expr
        # is the prime example here - all three of its alternatives start
        # with expr_rule, so it needs a full speculative parse to tell them
        # apart) reports its own error when that speculative parse hits a
        # dead end, and the real parse then reaches the identical dead end
        # again moments later and reports it a second time.
        return bool(self.errors) and (self.errors[-1].line, self.errors[-1].column, self.errors[-1].message) == (line, column, message)

    def _add(self, lexeme, message, line, column):
        if self._is_duplicate(line, column, message):
            return
        self.errors.append(ErrorToken(
            filename=self.filename,
            lexeme=lexeme,
            message=message,
            line=line,
            column=column,
            is_eof_error=False
        ))

    def syntaxError(self, recognizer, offending_symbol, line, column, msg, e):
        lexeme = offending_symbol.text
        line = line
        column = column + 1

        if offending_symbol.type == HarmonyParser.INDENT:
            self._add(lexeme, "Indentation error", line, column)
            return

        if offending_symbol.type == HarmonyParser.DEDENT:
            self._add(lexeme, "Unexpected dedent. May be caused by indentation error.", line, column)
            return

        if isinstance(msg, str):
            if msg.startswith("no viable alternative at input"):
                msg = f"Unexpected token {lexeme}"
            elif msg.startswith("extraneous input"):
                msg = f"Extraneous input {lexeme}. May be caused by another error."
            elif msg.startswith("mismatched input"):
                msg = f"Unexpected token {lexeme}"

        self._add(lexeme, str(msg), line, column)
