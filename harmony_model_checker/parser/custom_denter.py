from antlr4.Token import Token  # type: ignore
from antlr_denter.DenterHelper import DenterHelper  # type: ignore


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
    
    def _is_operator_token(self, t: Token) -> bool:
        return t.text in {
            '==', '!=', '<', '<=', '>', '>=',
            'and', 'or', '=>', '&', '|', '^',
            '-', '+', '*', '//', '/', '%', 'mod',
            '**', '<<', '>>', 'in', 'when', 'let',
            'not', ','
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
            # if greater, then check if we add an indent
            previous_token_is_colon = self.previous_token is not None and self.previous_token.type == self.colon_token
            nearby_tokens_are_operators = self._is_operator_token(self.previous_token) or self._is_operator_token(next_next)

            if not previous_token_is_colon and nearby_tokens_are_operators:
                return next_next
            else:
                r = self.create_token(self.indent_token, t)
                self.indentations.insert(0, indent)
        else:
            # if less, it is a possible dedent
            r = self.unwind_to(indent, t)
        self.dents_buffer.append(next_next)
        return r

    def next_token(self):
        r = super().next_token()
        self.previous_token = r
        return r
