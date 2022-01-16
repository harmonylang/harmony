from antlr4.Token import Token
from antlr_denter.DenterHelper import DenterHelper


_MIXED_INDENTATION_ERROR_TEXT = """Indentation Error: Mixing tabs and spaces for indentation"""

class ModifiedDenterHelper(DenterHelper):
    def __init__(self, lexer, nl_token, colon_token, indent_token, dedent_token, ignore_eof):
        super().__init__(nl_token, indent_token, dedent_token, ignore_eof)
        self.lexer = lexer
        self.previous_token: Token = None
        self.colon_token = colon_token
        self.encountered_indentation_styles = {
            "tab": False,
            "space": False
        }

    def handle_newline_token(self, t: Token):
        """
        Overrides the [handle_newline_token] method of [DenterHelper].
        Checks if the preceding token is a colon. If so, then emit an indent
        token. Otherwise, treat it as a normal newline.
        """
        next_next = self.pull_token()
        while next_next.type == self.nl_token:
            """
            Skip while we observe newlines.
            """
            t = next_next
            next_next = self.pull_token()
        if next_next.type == Token.EOF:
            return self.apply(next_next)

        # Get the length of the indentation.
        nl_text = t.text
        indent = len(nl_text) - 1
        if indent > 0 and nl_text[0] == '\r':
            indent -= 1  # decrease indent by 1 if it is Windows CR character.

        # get the length of the previous indentation.
        prev_indent = self.indentations[0]

        if indent == prev_indent:
            # if equal size, then treat the token as a newline
            r = t
        elif indent > prev_indent:
            # if greater, then we have a new indentation.
            syntax_error_dispatcher = self.lexer.getErrorListenerDispatch()
            if '\t' in t.text:
                self.encountered_indentation_styles["tab"] = True
                if self.encountered_indentation_styles["space"]:
                    syntax_error_dispatcher.syntaxError(None, t, t.line, t.column, _MIXED_INDENTATION_ERROR_TEXT, None)
            elif ' ' in t.text:
                self.encountered_indentation_styles["space"] = True
                if self.encountered_indentation_styles["tab"]:
                    syntax_error_dispatcher.syntaxError(None, t, t.line, t.column, _MIXED_INDENTATION_ERROR_TEXT, None)

            if self.previous_token is not None and self.previous_token == self.colon_token:
                # treat this token as a indent
                r = self.create_token(self.indent_token, t)
                self.indentations.insert(0, indent)
            else:
                # ignore the newline token and retrieve the next non-newline token
                while next_next.type == self.nl_token:
                    """
                    Skip while we observe newlines.
                    """
                    next_next = self.pull_token()
                return next_next
        else:
            # if less, it is a possible dedent
            r = self.unwind_to(indent, t)
        self.dents_buffer.append(next_next)
        return r

    def next_token(self):
        r = super().next_token()
        self.previous_token = r.type
        return r
