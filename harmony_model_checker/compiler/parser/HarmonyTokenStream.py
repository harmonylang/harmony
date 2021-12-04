from antlr4 import *
from antlr4.Token import CommonToken

from HarmonyParser import HarmonyParser


def make_indent_token(line: int):
    indent = CommonToken(type=HarmonyParser.INDENT)
    indent.line = line
    indent.text = "indent"
    return indent


class HarmonyTokenStream(CommonTokenStream):
    def __init__(self, lexer, parser):
        super().__init__(lexer)
        self.parser = parser

    def _handle_var_let(self):
        """
        Handles multi-line tokens in a for-declaration.
        Skips newlines until it encounters [=] in the token stream
        """
        pass

    def _handle_for_start(self):
        """
        Handles multi-line tokens in a for-declaration.
        Skips newlines until it encounters [in] in the token stream
        """
        pass

    def handle_compound(self):
        idx = 1
        end_token_str = ':'
        indentation_stack = []
        bracket_stack = []
        indents = []
        dedents = []
        newlines = []
        while True:
            t: CommonToken = self.LT(idx)
            if t.type == HarmonyParser.FOR:
                # Do this to avoid possible colons in for variable declarations
                while t.type != HarmonyParser.IN:
                    idx += 1
                    t = self.LT(idx)
                    if t.type == HarmonyParser.INDENT:
                        indents.append((t, idx - 1))
                        indentation_stack.append(t)
                    elif t.type == HarmonyParser.DEDENT:
                        dedents.append((t, idx - 1))
                        indentation_stack.pop()
                    elif t.type == HarmonyParser.NL:
                        newlines.append((t, idx - 1))
                    elif t.type in {HarmonyParser.OPEN_BRACK, HarmonyParser.OPEN_BRACES, HarmonyParser.OPEN_PAREN}:
                        bracket_stack.append(t)
                    elif t.type in {HarmonyParser.CLOSE_BRACK, HarmonyParser.CLOSE_BRACES, HarmonyParser.CLOSE_PAREN}:
                        bracket_stack.pop()
                    elif t.type == HarmonyParser.EOF:
                        break

            if t.type == HarmonyParser.INDENT:
                indents.append((t, idx - 1))
                indentation_stack.append(t)
            elif t.type == HarmonyParser.DEDENT:
                dedents.append((t, idx - 1))
                indentation_stack.pop()
            elif t.type == HarmonyParser.NL:
                newlines.append((t, idx - 1))
            elif t.type in {HarmonyParser.OPEN_BRACK, HarmonyParser.OPEN_BRACES, HarmonyParser.OPEN_PAREN}:
                bracket_stack.append(t)
            elif t.type in {HarmonyParser.CLOSE_BRACK, HarmonyParser.CLOSE_BRACES, HarmonyParser.CLOSE_PAREN}:
                bracket_stack.pop()
            elif t.type == HarmonyParser.EOF or (not bracket_stack and t.text == end_token_str):
                break
            idx += 1

        colon_idx = idx
        end_token: CommonToken = self.LT(colon_idx)
        l1: CommonToken = self.LT(idx + 1)
        l2: CommonToken = self.LT(idx + 2)
        if l1.type == HarmonyParser.NL and l2.type == HarmonyParser.DEDENT:
            indentation_stack.pop()
            self.tokens.pop(self.index + colon_idx + 1)
            self.tokens.pop(self.index + colon_idx)
        elif l1.type == HarmonyParser.INDENT:
            pass  # This is normal
        elif l1.type == HarmonyParser.NL:
            self.tokens.pop(self.index + colon_idx)
        else:
            pass  # One-line stmt. This is fine

        for _ in indentation_stack:
            # Move the indentation stack
            new_indent = make_indent_token(end_token.line)
            self.tokens.insert(self.index + colon_idx, new_indent)

        reduction_set = newlines + indents + dedents
        reduction_set.sort(key=lambda v: v[1], reverse=True)
        for t, p in reduction_set:
            self.tokens.pop(self.index + p)

    def handle_assignment(self):
        idx = 2  # Prevents the first token from being recognized as the next statement
        indentation_stack = []
        indents = []
        dedents = []
        newlines = []
        current_indent = 0 if not self.parser.indentation else self.parser.indentation[-1]
        while True:
            t: CommonToken = self.LT(idx)
            if t.type == HarmonyParser.INDENT:
                indents.append((t, idx - 1))
                indentation_stack.append(t)
            elif t.type == HarmonyParser.DEDENT:
                if indentation_stack:
                    dedents.append((t, idx - 1))
                    indentation_stack.pop()
                else:
                    break
            elif t.type == HarmonyParser.NL:
                newlines.append((t, idx - 1))
            elif t.type == HarmonyParser.EOF or t.column <= current_indent:
                break
            elif t.type == HarmonyParser.SEMI_COLON:
                break
            idx += 1

        newlines = newlines[:-1]
        reduction_set = newlines + indents + dedents
        reduction_set.sort(key=lambda v: v[1], reverse=True)
        for t, p in reduction_set:
            self.tokens.pop(self.index + p)
