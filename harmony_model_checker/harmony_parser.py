"""
Hand-written recursive descent parser for the Harmony language (see
Harmony.g4). It keeps the style already started: every parse_X function
takes (document, offset) - plus, for anything that can open an indented
block, an `indent` column - and returns a ParseResult whose start/end mark
the span it consumed on success, or whose value is a human-readable
message on failure. Nothing raises; callers check .success.

Fixes made to the code that was already here:

  * skip_blanks silently dropped tabs, '\\r', and comments (WS/COMMENT in
    the .g4 skip all three). Fixed, so tab-indented or commented Harmony
    source now parses.
  * lc/uc had a stray extra "u" spliced into the alphabet. Harmless (just
    a duplicate letter), but cleaned up.
  * parse_keyword labelled its failure ParseResult "identifier" instead of
    "keyword" - cosmetic, fixed.
  * `reserved` only listed 9 words, so parse_keyword failed to recognize
    True/False/None, every unary_op keyword (len, str, ...), and all the
    statement keywords - meaning parse_basic_expression's bool/None
    branches were dead code (kw.value was always the failure message "not
    a keyword", never "True"/"None"), and unary keywords like `len` fell
    through to being parsed as plain applications instead. Expanded
    `reserved` to every reserved word in the grammar, and made every
    caller check .success before looking at .value.
  * `unary_ops` incorrectly included 'save', 'setintlevel', 'stop' - those
    are their own expr_rule alternatives in the grammar, not unary_op.
    Moved them out and gave expr_rule its own cases for them.
  * parse_expression's bare-`in` branch silently discarded a real parse
    error following `in` (it fell through to the arith_op loop, which
    just treats "in" as leftover garbage). Fixed to propagate the error,
    matching how the "not in" branch already worked.
  * parse_basic_expression's paren/bracket case returned the *inner*
    tuple's start/end, not including the parens/brackets themselves.
    Fixed, and it now also handles the empty-tuple/empty-list forms the
    grammar allows (`()`, `[]`).
  * INT only recognized decimal digits; the grammar also allows 0x/0b/0o
    literals. Added.
  * Genuinely new pieces, not in the original file at all: strings, atoms
    (.foo), set/dict literals and comprehensions, lambda, bound/
    tuple_bound, iter_parse (for/where clauses), ARROWID in application,
    every statement form, and whole-program parsing with Python-style
    indentation blocks.

Indentation: this parser has no separate lexer/token stream, so there's no
denter producing INDENT/DEDENT tokens the way the .g4's custom lexer does.
Instead, block-related functions carry an extra `indent` argument - the
column the *current* statement sits at - and a block it opens must be
indented strictly further than that. next_logical_line scans forward from
a real line start, skipping blank and comment-only lines (they don't
affect indentation, same as Python), and reports the indentation width
and start of the next real line.

Two things this does NOT implement, both rare edge cases: the grammar's
"dummy block" alternative (normal_block: INDENT (block_stmts | INDENT
block) DEDENT, for a block that is itself immediately just a deeper block
with no statements at the shallower level), and validation that a file
consistently uses tabs XOR spaces - indentation width is just a character
count, matching the .g4's own comment on the NL rule ("For tabs just
switch out ' '* with '\\t'*").
"""

from contextlib import contextmanager

lc = "abcdefghijklmnopqrstuvwxyz"
uc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
letters = "_" + lc + uc
alnum = letters + digits

unary_ops = {
    'abs',
    'all',
    'any',
    'bin',
    'choose',
    'dict',
    'get_context',
    'get_ident',
    'hash',
    'hex',
    'int',
    'keys',
    'len',
    'list',
    'max',
    'min',
    'not',
    'oct',
    'reversed',
    'set',
    'sorted',
    'str',
    'sum',
    'type',
    'zip',
}

# Three precedence levels, loosest to tightest: logic_ops ('and'/'or'/
# '=>') bind loosest, then compare_ops, then arith_ops (everything
# else - +, -, *, /, //, %, mod, &, |, ^, **, <<, >>), which are all
# still flat/left-to-right *among themselves* - Harmony doesn't
# distinguish + from *, say - only the three levels are ordered
# relative to each other. See parse_expression for how these three
# combine into nary_expr's actual precedence climb.
logic_ops = {'=>'}
word_logic_ops = {"and", "or"}

compare_ops = {
    '==',
    '!=',
    '<',
    '<=',
    '>',
    '>=',
}

arith_ops = {
    '&',
    '|',
    '^',
    '-',
    '+',
    '*',
    '//',
    '/',
    '%',
    '**',
    '<<',
    '>>',
}

# Word-shaped arith ops are matched via parse_keyword instead of
# parse_bin_op's symbol scan.
word_arith_ops = {"mod"}

# Within arith_ops, only this subset gets real, standard-arithmetic
# precedence (mult-tier binds tighter than add-tier) when mixed together
# - see _group_standard_arith. Anything outside this subset (&, |, ^, **,
# <<, >>) has no defined relative precedence against the others, so
# mixing two *different* operators where either one falls outside this
# set is ambiguous, per the user's own rule.
_ADD_TIER_OPS = {'+', '-'}
_MULT_TIER_OPS = {'*', '/', '//', '%', 'mod'}
STANDARD_ARITH_OPS = _ADD_TIER_OPS | _MULT_TIER_OPS

# Outside the standard-arithmetic set, a *repeated* operator is usually
# still unambiguous even without any defined precedence, because it's
# associative (and, for &/|/^, commutative too) - "a & b & c" has one
# value no matter how you group it. '<<', '>>' and '**' don't have that
# property ((a<<b)<<c != a<<(b<<c), (a**b)**c != a**(b**c)), so - unlike
# every other arith_op - even *repeating* one of these is ambiguous, not
# just mixing it with something else. A single occurrence is still fine.
_NON_CHAINABLE_OPS = {'<<', '>>', '**'}

aug_assign_ops = {
    '&=',
    '|=',
    '^=',
    '-=',
    '+=',
    '*=',
    '/=',
    '//=',
    '%=',
    '**=',
    '>>=',
    '<<=',
    '=>=',
}
word_aug_assign_ops = {"and", "or", "mod"}

# Every reserved word in Harmony.g4 - anything a NAME may not be.
reserved = {
    "True", "False", "None",
    "and", "or", "mod", "not", "in", "if", "else",
    "end",
    "setintlevel", "save", "stop", "lambda",
    "import", "from", "as", "print",
    "const", "await", "assert", "var", "trap", "pass", "return", "break",
    "continue", "del", "spawn", "finally", "invariant", "go", "builtin",
    "sequential", "when", "let", "elif", "while", "global", "def",
    "returns", "exists", "where", "for", "atomically", "eternal",
} | unary_ops


class AST:
    def __init__(self):
        pass


class ParseResult:
    def __init__(self, type, success, value, start, end):
        self.type = type
        self.success = success
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self):
        return "%s:%s:%s:%d:%d" % (self.type, self.success, self.value, self.start, self.end)


# ---------------------------------------------------------------------------
# Whitespace. skip_blanks eats spaces, comments, and backslash-newline
# continuations unconditionally; a *bare* newline is only eaten while
# _bracket_depth says we're lexically inside an unmatched '(', '[' or '{'
# (or between a 'for' and its 'in') - exactly mirroring how the .g4's own
# lexer only discards NL while self.opened/self.opened_for is nonzero -
# OR while the token immediately before it is one that can never end an
# expression on its own (a binary/prefix operator, '=', a trailing ','),
# per Harmony's line-continuation rule: "x = 3 +\n    4" is one statement,
# because a line ending in an operator obviously isn't finished yet - see
# _ends_with_continuation - OR while the *next* real line is indented
# strictly deeper than the statement currently being parsed (_stmt_indent),
# Harmony's other line-continuation rule: "x = 3\n        + 4" is also one
# statement, purely because the second line is indented further than the
# first, regardless of what token '3' ends on - see _deeper_indent_follows.
# Everywhere else a newline ends the logical line, which is what lets
# parse_application (and friends) stop instead of reading into the next
# statement. The one exception, spelled out explicitly rather than folded
# in here, is a let_decl/when_decl's own optional trailing NL - see
# _skip_optional_nl below.
# ---------------------------------------------------------------------------

_bracket_depth = [0]

# The column the statement currently being parsed by parse_stmt starts at
# (see parse_stmt, which is the sole place this is set, scoped via
# try/finally to exactly the span of parsing that one statement) - 0
# outside of any parse_stmt call, matching top-level's own indent. Read by
# _deeper_indent_follows to decide whether a following line is a
# continuation of THIS statement (indented further than where it itself
# started) rather than a new sibling statement (which must sit at exactly
# this same column) or a nested block the statement itself opens (handled
# entirely separately, via skip_line_blanks/next_logical_line, never
# skip_blanks - see parse_block/parse_normal_block - so it's never at risk
# of being swallowed as a "continuation" by this mechanism).
_stmt_indent = [0]

# Symbols/words that always demand something after them, so a newline
# right after one is never the end of a statement - it's Harmony's
# implicit line-continuation rule. Deliberately scoped to *expression*
# operators (arith/aug-assign/unary/assign, plus the nary_expr
# connectives and a trailing comma); statement-leading keywords like
# RETURN or PRINT are a separate, not-yet-requested question - see the
# conversation. Symbols are checked as exact suffixes (any length is
# fine, no ordering needed); words are checked as whole words via
# _ends_with_word so e.g. an identifier that merely ends in "not" isn't
# mistaken for the keyword.
_CONTINUATION_SYMBOLS = tuple(
    arith_ops | compare_ops | logic_ops | aug_assign_ops | {'=', ',', '..', '~', '?', '!'}
)
_CONTINUATION_WORDS = (
    word_arith_ops | word_logic_ops | unary_ops |
    {'not', 'in', 'if', 'else', 'where', 'setintlevel', 'save', 'stop', 'lambda'}
)

# For the OTHER continuation rule (_deeper_indent_follows: a following
# line indented deeper than the current statement) the check runs the
# opposite direction - what does the NEXT line start with? - and needs a
# much narrower set: only symbols/words that can EXCLUSIVELY appear as a
# binary infix operator (or ARROWID, an explicit chain-continuator),
# NEVER as the first token of a fresh statement/expression in their own
# right. This is deliberately narrower than _CONTINUATION_SYMBOLS/WORDS
# above (which are fine being permissive, since they're about a token
# that just ended - there's no "which statement is this?" ambiguity to
# worry about there): '-', '~', '?', '!' are excluded here even though
# they're in _CONTINUATION_SYMBOLS, because each is ALSO a valid unary/
# prefix operator that could legitimately start a brand new statement
# (e.g. a fresh "-x" or "!p" on its own line) - and 'if'/'else'/'not'
# are excluded from the words for the same reason ('if'/'else' start
# compound statements; 'not' is a unary_op). Treating an ambiguous
# leading token as "definitely a continuation" would risk silently
# merging an accidentally over-indented NEW statement into the previous
# one instead of reporting a clear indentation error - see the
# conversation for the motivating "z = f(x)\n        g(y)" case that
# silently (and wrongly) parsed as one statement before this narrowing.
_LEADING_CONTINUATION_SYMBOLS = tuple(
    (arith_ops - {'-'}) | compare_ops | logic_ops | aug_assign_ops | {'=', ',', '..', '->'}
)
_LEADING_CONTINUATION_WORDS = word_arith_ops | word_logic_ops | word_aug_assign_ops


def _ends_with_word(document, offset, word):
    n = len(word)
    if offset < n or document[offset - n:offset] != word:
        return False
    if offset - n > 0 and document[offset - n - 1] in alnum:
        return False
    return True


def _starts_with_word(document, offset, word):
    n = len(word)
    if document[offset:offset + n] != word:
        return False
    if offset + n < len(document) and document[offset + n] in alnum:
        return False
    return True


def _starts_with_unambiguous_continuation(document, offset):
    """True if the text starting at `offset` (the first real content of
    a line, past its own leading indentation) begins with a symbol/word
    from the narrow _LEADING_CONTINUATION_SYMBOLS/WORDS sets - i.e. it
    can only be continuing an expression from a previous, less-indented
    line, never starting a fresh statement of its own. See those sets'
    own comment for why this has to be much more conservative than
    _ends_with_continuation."""
    for sym in _LEADING_CONTINUATION_SYMBOLS:
        if document[offset:offset + len(sym)] == sym:
            return True
    for word in _LEADING_CONTINUATION_WORDS:
        if _starts_with_word(document, offset, word):
            return True
    return False


def _skip_trailing_comment(document, offset):
    """If the text immediately before `offset` is a comment (a '#...'
    line comment, or a '(* ... *)' block comment) rather than real code,
    return the offset just before that comment started. Needed because
    skip_blanks is called redundantly all over the place (every
    token-level parser calls it again at entry), and once one call has
    already skipped past a comment, a later call lands with `offset`
    sitting right after the comment's own text - e.g. right after the
    word "sorted" in "# ... to be sorted\\n". Without this, that comment
    wording gets mistaken for a real preceding token by
    _ends_with_continuation (since "sorted" is itself a reserved unary
    operator), wrongly treating the following newline as insignificant.
    This walks back through any such comment (and, recursively, more
    than one) to the real code that precedes it."""
    if offset >= 2 and document[offset - 2:offset] == '*)':
        open_pos = document.rfind('(*', 0, offset - 2)
        if open_pos != -1 and document.find('*)', open_pos + 2) == offset - 2:
            return _skip_trailing_comment(document, open_pos)
    line_start = document.rfind('\n', 0, offset) + 1
    pos = line_start
    in_string = None
    while pos < offset:
        c = document[pos]
        if in_string:
            if c == '\\' and pos + 1 < offset:
                pos += 2
                continue
            if c == in_string:
                in_string = None
            pos += 1
            continue
        if c in ('"', "'"):
            in_string = c
            pos += 1
            continue
        if c == '#':
            return pos
        pos += 1
    return offset


def _ends_with_continuation(document, offset):
    """True if the token ending exactly at `offset` can't end an
    expression/statement by itself - e.g. 'x = 3 +' or 'x = 3 +   ' - so
    a newline (and any further blank lines/comments) right after it is
    insignificant, same as being inside brackets."""
    while True:
        new_offset = _skip_trailing_comment(document, offset)
        while new_offset > 0 and document[new_offset - 1] in ' \t':
            new_offset -= 1
        if new_offset == offset:
            break
        offset = new_offset
    for word in _CONTINUATION_WORDS:
        if _ends_with_word(document, offset, word):
            return True
    for sym in _CONTINUATION_SYMBOLS:
        if document[offset - len(sym):offset] == sym:
            return True
    return False


def _deeper_indent_follows(document, offset):
    """True if, once the rest of THIS line is behind us (skip_line_blanks'
    own domain of inline spaces/tabs/comments - never a real newline) and
    any further blank/comment-only lines are skipped too, the next real
    line is BOTH indented strictly deeper than the statement currently
    being parsed (_stmt_indent) AND starts with something that can only
    be continuing an expression, never starting a fresh statement of its
    own (_starts_with_unambiguous_continuation) - e.g. 'x = 3\\n        +
    4' is one statement because the second line sits further right than
    'x' itself did AND starts with '+', which can't lead a statement,
    regardless of what token '3' ends on (contrast _ends_with_continuation,
    which looks at the preceding token instead). The second condition is
    what keeps an accidentally over-indented but otherwise ordinary-
    looking new statement ('z = f(x)\\n        g(y)') from being silently
    swallowed into the previous one - see the module's own conversation-
    sourced notes on _LEADING_CONTINUATION_SYMBOLS/WORDS for why.
    Deliberately walks the rest of the CURRENT line first via
    skip_line_blanks rather than measuring indentation from `offset`
    directly, since `offset` is typically mid-line (right where some
    earlier token just ended, not at a real line start) - measuring
    "indentation" there would just be counting that token's own trailing
    spaces."""
    pos = skip_line_blanks(document, offset)
    if pos >= len(document) or document[pos] not in '\r\n':
        return False   # more real content on this same line - irrelevant here
    if document[pos] == '\r':
        pos += 1
    if pos < len(document) and document[pos] == '\n':
        pos += 1
    width, after_indent = next_logical_line(document, pos)
    return (width is not None and width > _stmt_indent[0]
            and _starts_with_unambiguous_continuation(document, after_indent))


@contextmanager
def _colon_header():
    """Bumps _bracket_depth for the span of a statement header that's
    always going to end in a ':' (an if/elif/else/while/for/let-when/
    atomically/def header). A newline anywhere in there is insignificant
    - just like inside brackets - and only becomes meaningful again once
    the ':' (and its block) is reached. Harmony treats these the same
    way it treats being inside parens, so this reuses the same counter
    rather than introducing a separate mechanism."""
    _bracket_depth[0] += 1
    try:
        yield
    finally:
        _bracket_depth[0] -= 1


def skip_blanks(document, offset):
    # Decided once, from the position we started at (before this call
    # has skipped anything): does the token that just ended here allow a
    # newline to follow it? If so that holds for the whole call, so any
    # number of blank/comment lines after e.g. a trailing '+' are also
    # skipped, not just the first newline. Three independent reasons a
    # newline can be insignificant: inside brackets, right after a token
    # that can't end an expression on its own, or (checked last, and only
    # when neither of the first two already settled it, since it's the
    # most expensive of the three) because the next real line is indented
    # deeper than this statement's own start.
    allow_nl = (_bracket_depth[0] > 0
                or _ends_with_continuation(document, offset)
                or _deeper_indent_follows(document, offset))
    while True:
        if offset < len(document) and document[offset] in ' \t':
            offset += 1
            continue
        if offset + 1 < len(document) and document[offset] == '\\' and document[offset + 1] == '\n':
            offset += 2
            continue
        if document[offset:offset + 2] == '(*':
            end = document.find('*)', offset + 2)
            offset = end + 2 if end != -1 else len(document)
            continue
        if offset < len(document) and document[offset] == '#':
            while offset < len(document) and document[offset] not in '\r\n':
                offset += 1
            continue
        if offset < len(document) and document[offset] in '\r\n' and allow_nl:
            offset += 1
            continue
        break
    return offset


def skip_line_blanks(document, offset):
    """Like skip_blanks, but never crosses a real end-of-line even when
    _bracket_depth is nonzero: it skips inline spaces/tabs, backslash-
    newline continuations, '#' comments, and '(* ... *)' block comments,
    stopping at an actual '\\r'/'\\n' or EOF. Used to find "is there more
    on this line" without accidentally skipping into the next one."""
    while offset < len(document):
        c = document[offset]
        if c in ' \t':
            offset += 1
        elif c == '\\' and offset + 1 < len(document) and document[offset + 1] == '\n':
            offset += 2
        elif document[offset:offset + 2] == '(*':
            end = document.find('*)', offset + 2)
            offset = end + 2 if end != -1 else len(document)
        elif c == '#':
            while offset < len(document) and document[offset] not in '\r\n':
                offset += 1
        else:
            break
    return offset


def _skip_optional_nl(document, offset):
    """Consume one optional NL (with any inline blanks/comments before
    it) - for the "NL?" in let_decl/when_decl, which is a real newline
    that's allowed, not merely insignificant whitespace."""
    pos = skip_line_blanks(document, offset)
    if pos < len(document) and document[pos] == '\r':
        pos += 1
    if pos < len(document) and document[pos] == '\n':
        pos += 1
    return pos


def parse_number(document, offset):
    offset = skip_blanks(document, offset)
    if offset >= len(document):
        return ParseResult("number", False, "EOF instead of number", offset, offset)
    start = offset
    if document[offset] == '0' and offset + 1 < len(document) and document[offset + 1] in 'xbo':
        base, valid = {
            'x': (16, "0123456789abcdefABCDEF"),
            'b': (2, "01"),
            'o': (8, "01234567"),
        }[document[offset + 1]]
        digit_start = offset + 2
        pos = digit_start
        while pos < len(document) and document[pos] in valid:
            pos += 1
        if pos == digit_start:
            return ParseResult("number", False, "expected digits after '0%s'" % document[offset + 1], offset, pos + 1)
        if pos < len(document) and document[pos] in "_" + lc + uc:
            return ParseResult("number", False, "number cannot end in letter", start, pos + 1)
        return ParseResult("number", True, int(document[digit_start:pos], base), start, pos)
    if document[offset] not in digits:
        return ParseResult("number", False, "expected a digit", offset, offset + 1)
    number = int(document[offset])
    offset += 1
    while offset < len(document) and document[offset] in digits:
        number *= 10
        number += int(document[offset])
        offset += 1
    if offset < len(document) and document[offset] in "_" + lc + uc:
        return ParseResult("number", False, "number cannot end in letter", start, offset + 1)
    return ParseResult("number", True, number, start, offset)


def parse_identifier(document, offset):
    offset = skip_blanks(document, offset)
    if offset >= len(document):
        return ParseResult("identifier", False, "EOF instead of identifier", offset, offset)
    if document[offset] not in "_" + lc + uc:
        return ParseResult("identifier", False, "expected a letter or _", offset, offset + 1)
    start = offset
    id = document[offset]
    offset += 1
    while offset < len(document) and document[offset] in "_" + lc + uc + digits:
        id += document[offset]
        offset += 1
    if id in reserved:
        return ParseResult("identifier", False, "identifier is a reserved word", start, offset)
    return ParseResult("identifier", True, id, start, offset)


def parse_keyword(document, offset):
    offset = skip_blanks(document, offset)
    if offset >= len(document):
        return ParseResult("keyword", False, "EOF instead of keyword", offset, offset)
    if document[offset] not in lc + uc:
        return ParseResult("keyword", False, "expected a letter", offset, offset + 1)
    start = offset
    id = document[offset]
    offset += 1
    while offset < len(document) and document[offset] in "_" + lc + uc:
        id += document[offset]
        offset += 1
    if id not in reserved:
        return ParseResult("keyword", False, "not a keyword", start, offset)
    return ParseResult("keyword", True, id, start, offset)


def expect_keyword(document, offset, word):
    kw = parse_keyword(document, offset)
    if kw.success and kw.value == word:
        return kw
    return ParseResult("keyword", False, "expected '%s'" % word, offset, offset + max(1, len(word)))


def expect_char(document, offset, ch):
    pos = skip_blanks(document, offset)
    if pos < len(document) and document[pos] == ch:
        return ParseResult("char", True, ch, pos, pos + 1)
    return ParseResult("char", False, "expected '%s'" % ch, pos, pos + 1)


# STRING ::= SHORT_STRING | LONG_STRING
def parse_string(document, offset):
    offset = skip_blanks(document, offset)
    if offset >= len(document):
        return ParseResult("string", False, "EOF instead of string", offset, offset)
    for triple in ('"""', "'''"):
        if document[offset:offset + 3] == triple:
            start = offset
            pos = offset + 3
            while True:
                if pos >= len(document):
                    return ParseResult("string", False, "unterminated triple-quoted string", start, pos)
                if document[pos] == '\\' and pos + 1 < len(document):
                    pos += 2
                    continue
                if document[pos:pos + 3] == triple:
                    pos += 3
                    return ParseResult("string", True, document[start:pos], start, pos)
                pos += 1
    if document[offset] in ('"', "'"):
        quote = document[offset]
        start = offset
        pos = offset + 1
        while True:
            if pos >= len(document) or document[pos] in '\r\n':
                return ParseResult("string", False, "unterminated string", start, pos)
            if document[pos] == '\\' and pos + 1 < len(document):
                pos += 2
                continue
            if document[pos] == quote:
                pos += 1
                return ParseResult("string", True, document[start:pos], start, pos)
            pos += 1
    return ParseResult("string", False, "expected a string", offset, offset + 1)


# ATOM ::= '.' (HEX_INTEGER | NAME)   where HEX_INTEGER ::= '0X' hexdigit+
def parse_atom(document, offset):
    offset = skip_blanks(document, offset)
    if offset >= len(document) or document[offset] != '.':
        return ParseResult("atom", False, "expected an atom", offset, offset + 1)
    start = offset
    pos = offset + 1
    if document[pos:pos + 2] == '0X':
        digit_start = pos + 2
        p = digit_start
        while p < len(document) and document[p] in "0123456789abcdefABCDEF":
            p += 1
        if p == digit_start:
            return ParseResult("atom", False, "expected hex digits after '0X'", offset, p + 1)
        return ParseResult("atom", True, document[start:p], start, p)
    if pos >= len(document) or document[pos] not in letters:
        return ParseResult("atom", False, "expected a name after '.'", offset, offset + 1)
    p = pos + 1
    while p < len(document) and document[p] in alnum:
        p += 1
    return ParseResult("atom", True, document[start:p], start, p)


def parse_unary_op(document, offset):
    # '?' (address-of) is deliberately NOT in this set - unlike every
    # other unary_op, its operand isn't an unrestricted expr_rule.
    # parse_expr_rule handles '?' as a special case, via
    # parse_question_operand, before ever reaching here. See that
    # function's docstring for why.
    offset = skip_blanks(document, offset)
    if offset >= len(document):
        return ParseResult("unary_op", False, "EOF instead of unary operator", offset, offset)
    op = parse_keyword(document, offset)
    if op.success and op.value in unary_ops:
        return op
    if document[offset] not in {'-', '~', '!'}:
        return ParseResult("unary_op", False, "expected a unary operator", offset, offset + 1)
    return ParseResult("unary_op", True, document[offset], offset, offset + 1)


# Matches one binary operator from the given symbol/word sets at
# `offset` - checked as a keyword for word-shaped operators (so e.g. an
# identifier that merely starts with "and" isn't mistaken for the
# keyword) and by longest-match for symbol-shaped ones, careful not to
# swallow the '=' of an augmented-assignment token (e.g. '+=' is a
# single token, not '+' followed by '='). Shared by the three
# precedence-level matchers below - each just passes a different
# (symbols, words) pair.
def _match_op(document, offset, symbols, words):
    offset = skip_blanks(document, offset)
    if offset >= len(document):
        return ParseResult("bin_op", False, "EOF instead of binary operator", offset, offset)
    op = parse_keyword(document, offset)
    if op.success and op.value in words:
        return ParseResult("binary_op", True, op.value, op.start, op.end)
    found = ''
    for x in symbols:
        if len(x) > len(found) and len(document) - offset >= len(x) and document[offset:offset + len(x)] == x:
            found = x
    if found == '':
        return ParseResult("bin_op", False, "expected a binary operator", offset, offset + 1)
    if document[offset + len(found):offset + len(found) + 1] == '=' and (found + '=') in aug_assign_ops:
        return ParseResult("bin_op", False, "expected a binary operator", offset, offset + 1)
    return ParseResult("bin_op", True, found, offset, offset + len(found))


# Level 3 (tightest): & | ^ - + * // / % mod ** << >>. Still flat/
# left-to-right among themselves, same as before this change.
def parse_arith_op(document, offset):
    return _match_op(document, offset, arith_ops, word_arith_ops)


# Level 2: == != < <= > >=.
def parse_compare_op(document, offset):
    return _match_op(document, offset, compare_ops, set())


# Level 1 (loosest): 'and' 'or' '=>'.
def parse_logic_op(document, offset):
    return _match_op(document, offset, logic_ops, word_logic_ops)


def parse_assign_op(document, offset):
    offset = skip_blanks(document, offset)
    if offset >= len(document) or document[offset] != '=':
        return ParseResult("assign_op", False, "expected '='", offset, offset + 1)
    # don't swallow '==' or '=>'
    if offset + 1 < len(document) and document[offset + 1] in ('=', '>'):
        return ParseResult("assign_op", False, "expected '='", offset, offset + 1)
    return ParseResult("assign_op", True, '=', offset, offset + 1)


def parse_aug_assign_op(document, offset):
    offset = skip_blanks(document, offset)
    if offset >= len(document):
        return ParseResult("aug_assign_op", False, "EOF instead of augmented assignment operator", offset, offset)
    kw = parse_keyword(document, offset)
    if kw.success and kw.value in word_aug_assign_ops:
        if kw.end < len(document) and document[kw.end] == '=':
            return ParseResult("aug_assign_op", True, kw.value + '=', kw.start, kw.end + 1)
        return ParseResult("aug_assign_op", False, "expected '=' after '%s'" % kw.value, kw.end, kw.end + 1)
    op = ''
    for x in aug_assign_ops:
        if len(x) > len(op) and len(document) - offset >= len(x) and document[offset:offset + len(x)] == x:
            op = x
    if op == '':
        return ParseResult("aug_assign_op", False, "expected an augmented assignment operator", offset, offset + 1)
    return ParseResult("aug_assign_op", True, op, offset, offset + len(op))


# ARROWID ::= '->' ' '* NAME   (its own lexer token - not subject to the
# reserved-word check that plain NAME gets)
def parse_arrowid(document, offset):
    offset = skip_blanks(document, offset)
    if document[offset:offset + 2] != '->':
        return ParseResult("arrowid", False, "expected '->'", offset, offset + 1)
    pos = offset + 2
    while pos < len(document) and document[pos] in ' \t':
        pos += 1
    if pos >= len(document) or document[pos] not in letters:
        return ParseResult("arrowid", False, "expected a name after '->'", offset, pos + 1)
    name_start = pos
    pos += 1
    while pos < len(document) and document[pos] in alnum:
        pos += 1
    return ParseResult("arrowid", True, document[name_start:pos], offset, pos)


# basic_expression ::= '(' tuple_rule? ')' | '[' tuple_rule? ']'
#                     | '{' set_rule? ','? '}' | '{' ':' '}'
#                     | number | identifier | string | atom | bool | None
#                     | lambda bound ':' nary_expr 'end'
def parse_paren_or_bracket(document, offset, close_ch, label):
    # Everything from here to the matching close is lexically "inside
    # brackets" - bare newlines in there are insignificant, same as the
    # .g4 lexer's self.opened counter makes NL invisible.
    start = offset
    _bracket_depth[0] += 1
    try:
        pos = skip_blanks(document, offset + 1)
        if pos < len(document) and document[pos] == close_ch:
            return ParseResult(label, True, [], start, pos + 1)
        inner = parse_tuple(document, offset + 1)
        if not inner.success:
            return inner
        pos = skip_blanks(document, inner.end)
        if pos >= len(document):
            return ParseResult(label, False, "expected closing '%s'" % close_ch, pos, pos)
        if document[pos] != close_ch:
            return ParseResult(label, False, "expected closing '%s'" % close_ch, pos, pos + 1)
    finally:
        _bracket_depth[0] -= 1
    return ParseResult(label, True, inner, start, pos + 1)


def parse_set_or_dict(document, offset):
    start = offset
    _bracket_depth[0] += 1
    try:
        pos = skip_blanks(document, offset + 1)
        if pos < len(document) and document[pos] == ':':
            pos2 = skip_blanks(document, pos + 1)
            if pos2 < len(document) and document[pos2] == '}':
                return ParseResult("empty_dict", True, {}, start, pos2 + 1)
        if pos < len(document) and document[pos] == '}':
            return ParseResult("set_rule", True, [], start, pos + 1)
        inner = parse_set_rule(document, offset + 1)
        if not inner.success:
            return inner
        pos = skip_blanks(document, inner.end)
        if pos < len(document) and document[pos] == ',':
            pos = skip_blanks(document, pos + 1)
        if pos >= len(document) or document[pos] != '}':
            return ParseResult("set_rule", False, "expected closing '}'", pos, pos + 1)
    finally:
        _bracket_depth[0] -= 1
    return ParseResult("set_rule", True, inner, start, pos + 1)


def parse_lambda(document, offset):
    kw = expect_keyword(document, offset, 'lambda')
    if not kw.success:
        return ParseResult("lambda_expr", False, "expected 'lambda'", offset, offset + 1)
    bound = parse_bound(document, kw.end)
    if not bound.success:
        return bound
    colon = expect_char(document, bound.end, ':')
    if not colon.success:
        return ParseResult("lambda_expr", False, "expected ':'", bound.end, bound.end + 1)
    body = parse_expression(document, colon.end)
    if not body.success:
        return body
    end_kw = expect_keyword(document, body.end, 'end')
    if not end_kw.success:
        return ParseResult("lambda_expr", False, "expected 'end'", body.end, body.end + 1)
    return ParseResult("lambda_expr", True, (bound, body), offset, end_kw.end)


def parse_basic_expression(document, offset):
    offset = skip_blanks(document, offset)
    if offset >= len(document):
        return ParseResult("basic_expression", False, "EOF instead of expression", offset, offset)

    if document[offset] == '(':
        return parse_paren_or_bracket(document, offset, ')', "paren_tuple")
    if document[offset] == '[':
        return parse_paren_or_bracket(document, offset, ']', "bracket_tuple")
    if document[offset] == '{':
        return parse_set_or_dict(document, offset)
    if document[offset] in ('"', "'"):
        return parse_string(document, offset)
    if document[offset] == '.':
        return parse_atom(document, offset)

    kw = parse_keyword(document, offset)
    if kw.success and kw.value in ("False", "True"):
        return ParseResult("bool", True, kw.value, kw.start, kw.end)
    if kw.success and kw.value == "None":
        return ParseResult("none", True, kw.value, kw.start, kw.end)
    if kw.success and kw.value == "lambda":
        return parse_lambda(document, offset)

    number = parse_number(document, offset)
    if number.success:
        return number

    id = parse_identifier(document, offset)
    if id.success:
        return id

    return ParseResult("basic_expression", False, "expected an expression", offset, offset + 1)


# set_rule ::= nary_expr ( ':' nary_expr (iter_parse | (',' nary_expr ':' nary_expr)*)
#                        | iter_parse
#                        | '..' nary_expr
#                        | (',' nary_expr)*
#                        )
def parse_set_rule(document, offset):
    first = parse_expression(document, offset)
    if not first.success:
        return first
    start = first.start
    pos = first.end

    colon = expect_char(document, pos, ':')
    if colon.success:
        value = parse_expression(document, colon.end)
        if not value.success:
            return value
        pos = value.end
        kw = parse_keyword(document, pos)
        if kw.success and kw.value in ('for', 'where'):
            it = parse_iter_parse(document, pos)
            if not it.success:
                return it
            return ParseResult("dict_comprehension", True, (first, value, it), start, it.end)
        pairs = [(first, value)]
        while True:
            p = skip_blanks(document, pos)
            if p >= len(document) or document[p] != ',':
                break
            key = parse_expression(document, p + 1)
            if not key.success:
                break
            colon2 = expect_char(document, key.end, ':')
            if not colon2.success:
                break
            val = parse_expression(document, colon2.end)
            if not val.success:
                break
            pairs.append((key, val))
            pos = val.end
        return ParseResult("dict", True, pairs, start, pos)

    kw = parse_keyword(document, pos)
    if kw.success and kw.value in ('for', 'where'):
        it = parse_iter_parse(document, pos)
        if not it.success:
            return it
        return ParseResult("set_comprehension", True, (first, it), start, it.end)

    range_pos = skip_blanks(document, pos)
    if document[range_pos:range_pos + 2] == '..':
        hi = parse_expression(document, range_pos + 2)
        if not hi.success:
            return hi
        return ParseResult("range", True, (first, hi), start, hi.end)

    elems = [first]
    while True:
        p = skip_blanks(document, pos)
        if p >= len(document) or document[p] != ',':
            break
        nxt = parse_expression(document, p + 1)
        if not nxt.success:
            break
        elems.append(nxt)
        pos = nxt.end
    return ParseResult("set", True, elems, start, pos)


# nary_rule ::= expr_rule ("not"? "in" expr_rule | "if" nary_rule "else" expr_rule)
#             | logic_expr
# logic_expr   ::= compare_expr (logic_op compare_expr)*     (lowest: and/or/=>)
# compare_expr ::= arith_expr (compare_op arith_expr)*       (== != < <= > >=)
# arith_expr   ::= expr_rule (arith_op expr_rule)*           (tightest: + - * / // % mod & | ^ ** << >>)
def parse_expression(document, offset):
    first = parse_expr_rule(document, offset)
    if not first.success:
        return first
    next = parse_keyword(document, first.end)
    if next.success and next.value == "if":
        cond = parse_expression(document, next.end)
        if not cond.success:
            return cond
        next = parse_keyword(document, cond.end)
        if next.success and next.value == "else":
            next = parse_expr_rule(document, next.end)
            if not next.success:
                return next
            return ParseResult("ifelse", True, (first, cond, next), first.start, next.end)
        return ParseResult("nary_rule", False, "expected 'else'", next.start, next.end)
    if next.success and next.value == "not":
        next = parse_keyword(document, next.end)
        if next.success and next.value == "in":
            next = parse_expr_rule(document, next.end)
            if not next.success:
                return next
            return ParseResult("notin", True, (first, next), first.start, next.end)
        else:
            return ParseResult("nary_rule", False, "expected 'in'", next.start, next.end)
    if next.success and next.value == "in":
        result = parse_expr_rule(document, next.end)
        if not result.success:
            return result
        return ParseResult("in", True, (first, result), first.start, result.end)
    # None of not-in/in/if-else matched, so this is the remaining
    # "(arith_op expr_rule)*" alternative - now three precedence
    # levels, loosest to tightest: 'and'/'or'/'=>' bind loosest, then
    # comparisons, then everything else. `first` was already parsed as
    # a plain expr_rule above (needed for the if/not/in peek), so it
    # seeds the tightest (arith) level; each looser level is then built
    # on top of the level below it.
    return _logic_chain_from(document, first)


# Builds one precedence level's flat, left-to-right operator chain on
# top of an already-parsed first operand (of whatever level is one
# tighter than this one) - operators at a single level don't nest
# relative to each other, only the three levels nest relative to *each
# other*, via which operand_parser is passed in (parse_expr_rule for
# the tightest level, or one of the *_chain functions below to recurse
# into the next looser level).
def _op_chain_from(document, first, op_parser, operand_parser):
    components = [first]
    operators = []
    offset = first.end
    while True:
        op = op_parser(document, offset)
        if not op.success:
            if not operators:
                return first
            return ParseResult("nary_rule", True, (components, operators), first.start, offset)
        next = operand_parser(document, op.end)
        if not next.success:
            return next
        operators.append(op)
        components.append(next)
        offset = next.end


# Level 3 (tightest): built directly on expr_rule operands. Flat/
# left-to-right isn't quite the whole story any more: once all the
# operators in the chain are known, _resolve_arith_chain decides whether
# the chain stands as-is, gets regrouped by standard +-*/ precedence, or
# is rejected as ambiguous. See its docstring.
def _arith_chain(document, offset):
    first = parse_expr_rule(document, offset)
    if not first.success:
        return first
    return _arith_chain_from(document, first)


def _arith_chain_from(document, first):
    flat = _op_chain_from(document, first, parse_arith_op, parse_expr_rule)
    if flat.type != "nary_rule" or not flat.success:
        # 0 or 1 operators (just `first` itself) - or a real parse
        # failure lower down - nothing to regroup or validate.
        return flat
    return _resolve_arith_chain(flat)


# A flat arith chain ("a op1 b op2 c ...") is:
#   - legal & unchanged if every operator is identical, UNLESS it's
#     repeated 2+ times and is one of '<<'/'>>'/'**' - those aren't
#     associative, so even repeating one is ambiguous (see
#     _NON_CHAINABLE_OPS above); every other repeated operator (e.g.
#     "a & b & c") is fine, evaluated left to right;
#   - legal & *regrouped* by standard arithmetic precedence if the
#     operators aren't all identical but every one of them is in
#     {+, -, *, /, //, mod, %} - "a + b * c" becomes "a + (b * c)";
#   - ambiguous (a parse error) otherwise - two different operators
#     appear and at least one of them isn't in that standard set, e.g.
#     "a + b >> c" (& mixing '|'/'+' the same way).
def _resolve_arith_chain(flat):
    components, operators = flat.value
    op_values = {op.value for op in operators}
    if len(op_values) == 1:
        op = next(iter(op_values))
        if len(operators) >= 2 and op in _NON_CHAINABLE_OPS:
            return ParseResult(
                "nary_rule", False,
                "ambiguous expression: repeating '%s' has no defined grouping - use parentheses" % op,
                operators[1].start, operators[1].end)
        return flat
    if op_values <= STANDARD_ARITH_OPS:
        return _group_standard_arith(components, operators, flat.start, flat.end)
    bad = operators[0]
    for op in operators[1:]:
        if op.value != operators[0].value:
            bad = op
            break
    return ParseResult(
        "nary_rule", False,
        "ambiguous expression: mixing '%s' and '%s' has no defined precedence - use parentheses" % (operators[0].value, bad.value),
        bad.start, bad.end)


# Regroups a flat chain whose operators are all drawn from
# {+, -, *, /, //, mod, %} (but aren't all identical) into real two-tier
# precedence: consecutive multiplicative-tier operators (*, /, //, mod,
# %) are grouped into their own sub-chain first, and those groups are
# then combined left-to-right by the additive-tier operators (+, -)
# between them - e.g. "a + b * c - d" becomes a flat top-level chain
# [a, (b*c), d] with operators [+, -].
def _group_standard_arith(components, operators, start, end):
    if not any(op.value in _ADD_TIER_OPS for op in operators):
        # No '+'/'-' at all - every operator is some mix of the
        # multiplicative-tier ones, which don't have any further
        # precedence relative to each other, so the flat shape already
        # says everything there is to say.
        return ParseResult("nary_rule", True, (components, operators), start, end)
    top_components = []
    top_operators = []
    group = [components[0]]
    group_ops = []
    for op, comp in zip(operators, components[1:]):
        if op.value in _ADD_TIER_OPS:
            top_components.append(_arith_group(group, group_ops))
            top_operators.append(op)
            group = [comp]
            group_ops = []
        else:
            group.append(comp)
            group_ops.append(op)
    top_components.append(_arith_group(group, group_ops))
    return ParseResult("nary_rule", True, (top_components, top_operators), start, end)


def _arith_group(components, operators):
    if not operators:
        return components[0]
    return ParseResult("nary_rule", True, (components, operators), components[0].start, components[-1].end)


# Level 2: built on top of level 3.
def _compare_chain(document, offset):
    first = parse_expr_rule(document, offset)
    if not first.success:
        return first
    return _compare_chain_from(document, first)


def _compare_chain_from(document, first_expr_rule):
    arith = _arith_chain_from(document, first_expr_rule)
    if not arith.success:
        return arith
    return _op_chain_from(document, arith, parse_compare_op, _arith_chain)


# Level 1 (loosest): built on top of level 2. Same "all identical or
# it's ambiguous" rule as the arith level, but simpler: no operator
# subset gets its own precedence here, so the only way a mixed chain is
# legal is if it isn't actually mixed - "x and y and z" and "x or y or
# z" are fine, but "x and y or z" and "x => y => z" (repeating '=>'
# isn't legal either - only 'and'/'or' may repeat) are both rejected.
def _logic_chain_from(document, first_expr_rule):
    compare = _compare_chain_from(document, first_expr_rule)
    if not compare.success:
        return compare
    chain = _op_chain_from(document, compare, parse_logic_op, _compare_chain)
    if chain is compare:
        # No logic_op found at all - a pure passthrough of `compare`,
        # which may itself already be a multi-operator nary_rule from a
        # tighter level (already validated there, e.g. arith's own
        # regrouping) - nothing to check at *this* level.
        return chain
    if chain.type != "nary_rule" or not chain.success:
        return chain
    _components, operators = chain.value
    if len(operators) >= 2:
        op_values = {op.value for op in operators}
        if len(op_values) != 1 or op_values <= {'=>'}:
            bad = operators[1]
            return ParseResult(
                "nary_rule", False,
                "ambiguous expression: chained '%s' is not legal - only repeated 'and' or repeated 'or' may chain without parentheses" % bad.value,
                bad.start, bad.end)
    return chain


# application ::= basic_expression (ARROWID | basic_expression)*
def parse_application(document, offset):
    first = parse_basic_expression(document, offset)
    if not first.success:
        return first
    application = [first]
    start = first.start
    end = first.end
    while True:
        arrow = parse_arrowid(document, end)
        if arrow.success:
            application.append(arrow)
            end = arrow.end
            continue
        next = parse_basic_expression(document, end)
        if not next.success:
            break
        application.append(next)
        end = next.end
    if len(application) == 1:
        return application[0]
    return ParseResult("application", True, application, start, end)


# True if `r` is a (possibly parenthesized) bare '!'-prefixed
# expr_rule - the "(!p)" in "(!p)[x]". Its own operand is unrestricted,
# exactly like every other use of '!' - whether "!e" is actually valid
# depends on what e evaluates to, not on syntax. Used only to recognize
# a '!'-headed base for _is_identifier_headed below; a bare "!p" (or
# "(!p)") with nothing following it is a different matter entirely (see
# that function's docstring).
def _is_dereference(r):
    if r.type == "expr_rule":
        op, _operand = r.value
        return op.value == '!'
    if r.type == "paren_tuple":
        inner = r.value
        if isinstance(inner, list) or inner.type == "tuple":
            return False
        return _is_dereference(inner)
    return False


# True if `r` - a parsed application/basic_expression result - is, once
# any purely-grouping parentheses are seen through, a legal base for
# '?' (and, identically, for an assign_target - see parse_assign_target):
# either a plain identifier, or a '!'-prefixed expression that has at
# least one more step (an index, an attribute, an application) after it.
#
# The second case needs some justification: "!e" dereferences a thunk
# to reach whatever it points at, and going on to index/attribute-
# access *that* is exactly as legitimate as doing so on a name - e.g.
# "(!p)[x] = 1" writes into slot x of whatever p points at, the same
# way "a[x] = 1" writes into slot x of a. What's NOT legal is a bare
# "?!p" (or "??x") with nothing further: "!(?e) == e" is the defining
# round-trip identity ("a = b" being shorthand for "!(?a) = b" only
# makes sense because of it), so "?!p" alone just hands back p itself
# with no further addressing accomplished - a no-op, not a mistake to
# special-case around. The extra step is what makes it more than that:
# "?(!p)[x]" address-computes through p's *own* thunk extended by x
# (matching "?a[x]" when p happens to hold "?a"), not by snapshotting
# whatever "!p" evaluates to - which is exactly why it has to be
# recognized here structurally rather than by first evaluating "!p" to
# a plain value and falling back on "a value is its own address".
#
# This deliberately does NOT extend to a '?'-prefixed base ("?(?a)[x]"
# stays illegal) - '!' and '?' cancel as a *pair* ("!(?e) == e"), but
# there's no matching identity for '?' composed with itself, so there's
# no equivalent justification for exempting it here.
#
# Parentheses don't count as a "real" head themselves - "parentheses
# are only for parsing purposes" - so "(f())" sees through to "f()",
# identifier-headed the same as if the parens weren't there; but a
# genuine multi-element tuple/list literal ("(a, b)", "[1, 2]", or an
# empty "()"/"[]") is a real value, not a name, and neither is anything
# else basic_expression allows (a number, string, bool, None, lambda)
# or any other expr_rule shape (setintlevel/save/stop, or a unary_op
# other than '!' - including another '?', which is exactly why "??x"
# stays excluded).
def _is_identifier_headed(r):
    if r.type == "identifier":
        return True
    if r.type == "application":
        head = r.value[0]
        return _is_identifier_headed(head) or _is_dereference(head)
    if r.type == "paren_tuple":
        inner = r.value
        if isinstance(inner, list):
            return False  # empty '()' - the empty-tuple value, not a name
        if inner.type == "tuple":
            return False  # a real multi-element tuple literal, e.g. (a, b)
        return _is_identifier_headed(inner)  # pure grouping - see through it
    return False


# question_operand ::= (NAME | '!' expr_rule) (ARROWID | basic_expression)*
#   -- with any purely-grouping parentheses seen through first, and the
#      '!' alternative only when at least one (ARROWID | basic_expression)
#      actually follows it - see _is_identifier_headed for why.
#
# '?e' (address-of) requires e to name something addressable in the
# first place - a shared/global variable, or a function, or (extending
# something already addressable) an application/indexing/attribute
# chain rooted at one of those: "?a", "?a.foo", "?a[1]", "?a->b",
# "?f(1)", "?f(1)(2)", "?(f())" (parens are just grouping), and
# "?(!p)[x]" (see _is_identifier_headed) are all legal, but "?5",
# "?[1, 2][0]", "?(1, 2)", "?(a, b)", "??x" and "?!p" are not.
# Parsed permissively first as an ordinary expr_rule, same as
# everywhere else, purely to find its extent - then re-checked against
# the restriction above, the same permissive-parse-then-validate
# pattern _as_assign_target uses.
def parse_question_operand(document, offset):
    expr = parse_expr_rule(document, offset)
    if not expr.success:
        return expr
    if not _is_identifier_headed(expr):
        return ParseResult(
            "question_operand", False,
            "'?' requires an operand that starts with an identifier (a variable or function name), not a literal, a collection, or another unary operator",
            expr.start, expr.end)
    return expr


# expr_rule ::= 'setintlevel' expr_rule | 'save' expr_rule | 'stop' expr_rule
#             | '?' question_operand | unary_op expr_rule | application
def parse_expr_rule(document, offset):
    offset = skip_blanks(document, offset)
    if offset >= len(document):
        return ParseResult("expr_rule", False, "EOF instead of expression", offset, offset)
    start = offset
    kw = parse_keyword(document, offset)
    if kw.success and kw.value in ("setintlevel", "save", "stop"):
        expr = parse_expr_rule(document, kw.end)
        if not expr.success:
            return expr
        return ParseResult(kw.value, True, expr, start, expr.end)
    if document[offset] == '?':
        expr = parse_question_operand(document, offset + 1)
        if not expr.success:
            return expr
        op = ParseResult("unary_op", True, '?', offset, offset + 1)
        return ParseResult("expr_rule", True, (op, expr), start, expr.end)
    op = parse_unary_op(document, offset)
    if op.success:
        expr = parse_expr_rule(document, op.end)
        if not expr.success:
            return expr
        return ParseResult("expr_rule", True, (op, expr), start, expr.end)
    return parse_application(document, offset)


def parse_expr(document, offset):
    return parse_expression(document, offset)


# tuple_rule ::= nary_expr (iter_parse | (',' nary_expr)* ','?)
def parse_tuple(document, offset):
    expr = parse_expression(document, offset)
    if not expr.success:
        return expr
    start = expr.start

    kw = parse_keyword(document, expr.end)
    if kw.success and kw.value == "for":
        it = parse_iter_parse(document, expr.end)
        if not it.success:
            return it
        return ParseResult("comprehension", True, (expr, it), start, it.end)

    tuple = [expr]
    count = 0
    while True:
        offset = skip_blanks(document, expr.end)
        if offset >= len(document):
            break
        if document[offset] != ',':
            break
        count += 1
        offset += 1
        expr = parse_expression(document, offset)
        if not expr.success:
            break
        tuple.append(expr)
        offset = expr.end
    if count == 0:
        return tuple[0]
    return ParseResult("tuple", True, tuple, start, offset)


# assign_target ::= '(' assign_target_list ')' | '[' assign_target_list ']'
#                  | '!' expr_rule | application
#
# A restricted form of tuple_rule for the left-hand side(s) of '=' and
# augmented-assign - and, since "a = b" is shorthand for "!(?a) = b",
# an assign_target and a '?'-operand are the exact same kind of thing
# (an lvalue) and get the exact same restriction: 'application' is
# legal only when it's identifier-headed, in the sense
# _is_identifier_headed defines (a bare NAME, an application/indexing/
# attribute chain rooted in one, or one rooted in a dereference with
# something further after it - "(!p)[x]" - all with any purely-
# grouping parentheses seen through). A bare literal or collection is
# NOT a legal target any more ("5 = 5", "[1,2] = x" are both now
# rejected) - "a value is its own address" stopped being the operative
# reasoning the moment '?' itself stopped accepting one.
#
# '!expr_rule' dereferences a thunk and doesn't restrict its operand's
# *shape*: whether "!e" is actually valid depends on what e evaluates
# to, not on syntax, which is all this parser can see.
#
# There's deliberately no '?expr_rule' alternative: "a = b" is
# shorthand for "!(?a) = b" - any target not already of the primitive
# '!...' form gets wrapped in one more '?' before being assigned into -
# so "?e = val" would itself expand to "!(?(?e)) = val", requiring
# "??e". But '?' now requires *its own* operand to start with an
# identifier (see parse_question_operand), and "?e" never does (it
# starts with '?') - so "??e" can never be legal, for any e, which
# makes "?e = val" always illegal too, for any e. Nothing is lost:
# assigning through a thunk you already hold is exactly what the
# surviving '!' alternative is for ("!p = 3").
#
# A parenthesized/bracketed group is a destructuring target-list
# (Python-compatible: "(a, b) = 1, 2" means exactly "a, b = 1, 2" -
# parens are just grouping), never "the address of the tuple value" -
# UNLESS it's immediately followed by more application-chain material
# with no separator (another basic_expr, or an ARROWID), which means it
# was only ever the *head* of a longer application/indexing chain, not
# a standalone target - e.g. "(!p)[x]" is indexing (!p) by x, not a
# destructuring pattern, because "[x]" follows the ")" directly, the
# same way application itself tells "(a)(b)" (one value applied to
# another) apart from two separate things. In that case the whole
# thing is re-parsed as a plain application instead, and validated as
# identifier-headed like any other application. A literal *empty*
# '()'/'[]' also falls through to 'application', where it's rejected -
# there's nothing to destructure, and (unlike before) it no longer
# gets a pass as "just the empty-tuple/list value" either.
def parse_assign_target(document, offset):
    offset = skip_blanks(document, offset)
    if offset < len(document) and document[offset] == '!':
        expr = parse_expr_rule(document, offset + 1)
        if not expr.success:
            return expr
        return ParseResult("assign_target", True, ("!", expr), offset, expr.end)
    for open_ch, close_ch in (('(', ')'), ('[', ']')):
        if offset < len(document) and document[offset] == open_ch:
            _bracket_depth[0] += 1
            try:
                pos = skip_blanks(document, offset + 1)
                if pos < len(document) and document[pos] == close_ch:
                    # A literal empty () / [] - nothing to destructure,
                    # so fall through below to treat it as the bare
                    # empty-tuple/list *value* instead.
                    break
                targets = parse_assign_target_list(document, offset + 1)
                if not targets.success:
                    return targets
                pos = skip_blanks(document, targets.end)
                if pos >= len(document) or document[pos] != close_ch:
                    return ParseResult("assign_target", False, "expected closing '%s'" % close_ch, pos, pos + 1)
                close_end = pos + 1
            finally:
                _bracket_depth[0] -= 1
            if _application_continues(document, close_end):
                break
            return ParseResult("assign_target", True, targets, offset, close_end)
    app = parse_application(document, offset)
    if not app.success:
        return app
    if not _is_identifier_headed(app):
        return ParseResult(
            "assign_target", False,
            "invalid assignment target: not an identifier, nor an application/indexing/attribute chain rooted in one (or in a dereference with something further after it)",
            app.start, app.end)
    return app


def _application_continues(document, offset):
    """True if parse_application's own loop would keep going from
    `offset` - i.e. there's an ARROWID or another basic_expr right
    there with no separator. Tells apart a parenthesized/bracketed
    group that's the *whole* assign_target (nothing follows it, or a
    ',' starts a further destructuring element) from one that's merely
    the *head* of a longer application/indexing chain, like "(!p)[x]"."""
    return parse_arrowid(document, offset).success or parse_basic_expression(document, offset).success


# assign_target_list ::= assign_target (',' assign_target)* ','?
def parse_assign_target_list(document, offset):
    first = parse_assign_target(document, offset)
    if not first.success:
        return first
    start = first.start
    targets = [first]
    pos = first.end
    while True:
        p = skip_blanks(document, pos)
        if p >= len(document) or document[p] != ',':
            break
        pos = p + 1
        nxt = parse_assign_target(document, pos)
        if not nxt.success:
            break
        targets.append(nxt)
        pos = nxt.end
    if len(targets) == 1:
        return targets[0]
    return ParseResult("assign_target_list", True, targets, start, pos)


def _as_assign_target(document, chunk):
    """`chunk` was already parsed permissively as a tuple_rule (parse_
    assign_stmt doesn't know a chunk is a target rather than the final
    value until it sees whether an '=' follows it) - confirm it actually
    has one of the legal assignment-target shapes by re-parsing that
    exact span with the restricted assign_target grammar, rather than
    the permissive one that was only used to find where it ends. The
    comparison is normalized past trailing blanks/comments on both
    sides, not a bare offset equality: parse_tuple's own comma-loop
    speculatively skip_blanks-es past trailing whitespace while peeking
    for one more ',' that isn't there, and reports that as part of its
    .end - assign_target_list's matching loop doesn't, so the two ends
    can differ by exactly that trailing whitespace even when the target
    is perfectly valid (e.g. "a, b = 1, 2")."""
    target = parse_assign_target_list(document, chunk.start)
    if target.success and skip_blanks(document, target.end) == skip_blanks(document, chunk.end):
        return target
    if not target.success:
        return ParseResult("assign_target", False, target.value, target.start, target.end)
    return ParseResult("assign_target", False, "invalid assignment target", target.end, target.end + 1)


# tuple_bound ::= NAME | '(' bound ')' | '[' bound ']' | '(' ')' | '[' ']'
def parse_tuple_bound(document, offset):
    offset = skip_blanks(document, offset)
    for open_ch, close_ch in (('(', ')'), ('[', ']')):
        if offset < len(document) and document[offset] == open_ch:
            _bracket_depth[0] += 1
            try:
                pos = skip_blanks(document, offset + 1)
                if pos < len(document) and document[pos] == close_ch:
                    return ParseResult("tuple_bound", True, [], offset, pos + 1)
                inner = parse_bound(document, offset + 1)
                if not inner.success:
                    return inner
                pos = skip_blanks(document, inner.end)
                if pos >= len(document) or document[pos] != close_ch:
                    return ParseResult("tuple_bound", False, "expected closing '%s'" % close_ch, pos, pos + 1)
                return ParseResult("tuple_bound", True, inner, offset, pos + 1)
            finally:
                _bracket_depth[0] -= 1
    name = parse_identifier(document, offset)
    if name.success:
        return name
    return ParseResult("tuple_bound", False, "expected a name or a bound pattern", offset, offset + 1)


# bound ::= (tuple_bound ',')* tuple_bound
def parse_bound(document, offset):
    first = parse_tuple_bound(document, offset)
    if not first.success:
        return first
    parts = [first]
    start = first.start
    pos = first.end
    while True:
        p = skip_blanks(document, pos)
        if p >= len(document) or document[p] != ',':
            break
        nxt = parse_tuple_bound(document, p + 1)
        if not nxt.success:
            break
        parts.append(nxt)
        pos = nxt.end
    if len(parts) == 1:
        return parts[0]
    return ParseResult("bound", True, parts, start, pos)


# for_parse ::= 'for' (bound | bound ':' bound) 'in' nary_expr
def parse_for_parse(document, offset):
    kw = expect_keyword(document, offset, 'for')
    if not kw.success:
        return ParseResult("for_parse", False, "expected 'for'", offset, offset + 1)
    # Between FOR and IN a bare newline is insignificant too - mirrors
    # the .g4 lexer's self.opened_for counter (incremented by FOR,
    # decremented by IN) existing for exactly this.
    _bracket_depth[0] += 1
    try:
        b1 = parse_bound(document, kw.end)
        if not b1.success:
            return b1
        b2 = None
        pos = b1.end
        colon = expect_char(document, pos, ':')
        if colon.success:
            b2 = parse_bound(document, colon.end)
            if not b2.success:
                return b2
            pos = b2.end
        in_kw = expect_keyword(document, pos, 'in')
        if not in_kw.success:
            return ParseResult("for_parse", False, "expected 'in'", pos, pos + 1)
    finally:
        _bracket_depth[0] -= 1
    src = parse_expression(document, in_kw.end)
    if not src.success:
        return src
    return ParseResult("for_parse", True, (b1, b2, src), offset, src.end)


# where_parse ::= 'where' nary_expr
def parse_where_parse(document, offset):
    kw = expect_keyword(document, offset, 'where')
    if not kw.success:
        return ParseResult("where_parse", False, "expected 'where'", offset, offset + 1)
    cond = parse_expression(document, kw.end)
    if not cond.success:
        return cond
    return ParseResult("where_parse", True, cond, offset, cond.end)


# iter_parse ::= for_parse (NL? (for_parse | where_parse))*
#
# Like let_when_decl's trailing NL?, the newline between chained
# for/where clauses is a real, meaningful one (this is normally called at
# bracket depth 0, e.g. directly under a for_block's colon, so plain
# skip_blanks won't cross it) - so it has to be consumed explicitly
# rather than assumed away.
def parse_iter_parse(document, offset):
    first = parse_for_parse(document, offset)
    if not first.success:
        return first
    clauses = [first]
    pos = first.end
    while True:
        candidate = _skip_optional_nl(document, pos)
        kw = parse_keyword(document, candidate)
        if kw.success and kw.value == 'for':
            nxt = parse_for_parse(document, candidate)
        elif kw.success and kw.value == 'where':
            nxt = parse_where_parse(document, candidate)
        else:
            break
        if not nxt.success:
            return nxt
        clauses.append(nxt)
        pos = nxt.end
    return ParseResult("iter_parse", True, clauses, offset, pos)


# ---------------------------------------------------------------------------
# Statements. From here down `skip_blanks` (newline-eating) is still used
# for everything *inside* a statement, right up until the point where the
# grammar itself calls for a real end-of-line - only the block layer below
# needs to reason about real lines and indentation.
# ---------------------------------------------------------------------------

def _keyword_then_expr(document, offset, word, label):
    kw = expect_keyword(document, offset, word)
    if not kw.success:
        return ParseResult(label, False, "expected '%s'" % word, offset, offset + 1)
    expr = parse_expression(document, kw.end)
    if not expr.success:
        return expr
    return ParseResult(label, True, expr, offset, expr.end)


def _bare_keyword(document, offset, word, label):
    kw = expect_keyword(document, offset, word)
    if not kw.success:
        return ParseResult(label, False, "expected '%s'" % word, offset, offset + 1)
    return ParseResult(label, True, word, kw.start, kw.end)


def parse_await_stmt(document, offset):
    return _keyword_then_expr(document, offset, 'await', 'await_stmt')


def parse_trap_stmt(document, offset):
    return _keyword_then_expr(document, offset, 'trap', 'trap_stmt')


def parse_return_stmt(document, offset):
    # Harmony has no 'return' statement (a function reports its result
    # by assigning to a declared 'returns' name instead) - but 'return'
    # stays reserved and gets its own grammar production anyway, purely
    # so a Python habit like "return 3" parses as its own recognizable
    # statement and checker.py can reject it with a clear, specific
    # message, rather than it either misparsing or - since 'return'
    # would otherwise be an ordinary identifier - being accepted as a
    # meaningless expression statement (application of an undeclared
    # 'return' to its argument) that only earns a generic "assumed
    # global" warning.
    return _keyword_then_expr(document, offset, 'return', 'return_stmt')


def parse_finally_stmt(document, offset):
    return _keyword_then_expr(document, offset, 'finally', 'finally_stmt')


def parse_invariant_stmt(document, offset):
    return _keyword_then_expr(document, offset, 'invariant', 'invariant_stmt')


def parse_del_stmt(document, offset):
    return _keyword_then_expr(document, offset, 'del', 'del_stmt')


def parse_pass_stmt(document, offset):
    return _bare_keyword(document, offset, 'pass', 'pass_stmt')


def parse_break_stmt(document, offset):
    return _bare_keyword(document, offset, 'break', 'break_stmt')


def parse_continue_stmt(document, offset):
    return _bare_keyword(document, offset, 'continue', 'continue_stmt')


# assert_stmt ::= 'assert' expr (',' expr)?
def parse_assert_stmt(document, offset):
    kw = expect_keyword(document, offset, 'assert')
    if not kw.success:
        return ParseResult("assert_stmt", False, "expected 'assert'", offset, offset + 1)
    cond = parse_expression(document, kw.end)
    if not cond.success:
        return cond
    pos = skip_blanks(document, cond.end)
    if pos < len(document) and document[pos] == ',':
        message = parse_expression(document, pos + 1)
        if not message.success:
            return message
        return ParseResult("assert_stmt", True, (cond, message), offset, message.end)
    return ParseResult("assert_stmt", True, (cond, None), offset, cond.end)


# print_stmt ::= 'print' expr (',' expr)?
def parse_print_stmt(document, offset):
    kw = expect_keyword(document, offset, 'print')
    if not kw.success:
        return ParseResult("print_stmt", False, "expected 'print'", offset, offset + 1)
    value = parse_expression(document, kw.end)
    if not value.success:
        return value
    pos = skip_blanks(document, value.end)
    if pos < len(document) and document[pos] == ',':
        endpoint = parse_expression(document, pos + 1)
        if not endpoint.success:
            return endpoint
        return ParseResult("print_stmt", True, (value, endpoint), offset, endpoint.end)
    return ParseResult("print_stmt", True, (value, None), offset, value.end)


# global_stmt ::= 'global' expr (',' expr)*
def parse_global_stmt(document, offset):
    kw = expect_keyword(document, offset, 'global')
    if not kw.success:
        return ParseResult("global_stmt", False, "expected 'global'", offset, offset + 1)
    first = parse_expression(document, kw.end)
    if not first.success:
        return first
    items = [first]
    pos = first.end
    while True:
        p = skip_blanks(document, pos)
        if p >= len(document) or document[p] != ',':
            break
        nxt = parse_expression(document, p + 1)
        if not nxt.success:
            return nxt
        items.append(nxt)
        pos = nxt.end
    return ParseResult("global_stmt", True, items, offset, pos)


# sequential_stmt ::= 'sequential' NAME (',' NAME)*
def parse_sequential_stmt(document, offset):
    kw = expect_keyword(document, offset, 'sequential')
    if not kw.success:
        return ParseResult("sequential_stmt", False, "expected 'sequential'", offset, offset + 1)
    first = parse_identifier(document, kw.end)
    if not first.success:
        return first
    names = [first]
    pos = first.end
    while True:
        p = skip_blanks(document, pos)
        if p >= len(document) or document[p] != ',':
            break
        nxt = parse_identifier(document, p + 1)
        if not nxt.success:
            return nxt
        names.append(nxt)
        pos = nxt.end
    return ParseResult("sequential_stmt", True, names, offset, pos)


# builtin_stmt ::= 'builtin' NAME STRING
def parse_builtin_stmt(document, offset):
    kw = expect_keyword(document, offset, 'builtin')
    if not kw.success:
        return ParseResult("builtin_stmt", False, "expected 'builtin'", offset, offset + 1)
    name = parse_identifier(document, kw.end)
    if not name.success:
        return name
    s = parse_string(document, name.end)
    if not s.success:
        return s
    return ParseResult("builtin_stmt", True, (name, s), offset, s.end)


# var_stmt ::= 'var' bound '=' tuple_rule
#            | 'var' NAME (',' NAME)*    // bare declaration, no initializer -
#                                        // a flat list of plain names may
#                                        // omit '= ...' this way (like
#                                        // 'global x, y'/'sequential x, y'),
#                                        // but never an actual destructuring
#                                        // bound - 'var (x, y)' or 'var [x, y]'
#                                        // (or one nested inside an
#                                        // otherwise-flat list, like
#                                        // 'var x, (y, z)') still requires an
#                                        // initializer, since there's nothing
#                                        // to destructure otherwise
def _is_flat_name_bound(bound):
    """True for a bound made of nothing but plain names - a single one
    ('x'), or a parenthesis-free list of them ('x, y, z') - the exact
    shape 'global'/'sequential' already accept bare. False for anything
    involving an actual '(...)'/'[...]' destructuring pattern, however
    deeply nested (including one nested inside an otherwise-flat list,
    like 'x, (y, z)') - see parse_var_stmt."""
    if bound.type == "identifier":
        return True
    if bound.type == "bound":
        return all(part.type == "identifier" for part in bound.value)
    return False


def parse_var_stmt(document, offset):
    kw = expect_keyword(document, offset, 'var')
    if not kw.success:
        return ParseResult("var_stmt", False, "expected 'var'", offset, offset + 1)
    bound = parse_bound(document, kw.end)
    if not bound.success:
        return bound
    eq = parse_assign_op(document, bound.end)
    if not eq.success:
        if not _is_flat_name_bound(bound):
            # A real destructuring bound ('var (x, y)', 'var [x, y]', or
            # one of these nested inside an otherwise-flat list) has
            # nothing to destructure without a '= tuple_rule' - unlike a
            # flat list of plain names, this is still an error.
            return ParseResult("var_stmt", False, "expected '='", bound.end, bound.end + 1)
        return ParseResult("var_stmt", True, (bound, None), offset, bound.end)
    rhs = parse_tuple(document, eq.end)
    if not rhs.success:
        return rhs
    return ParseResult("var_stmt", True, (bound, rhs), offset, rhs.end)


# const_assign_stmt ::= 'const' bound '=' expr
def parse_const_assign_stmt(document, offset):
    kw = expect_keyword(document, offset, 'const')
    if not kw.success:
        return ParseResult("const_assign_stmt", False, "expected 'const'", offset, offset + 1)
    bound = parse_bound(document, kw.end)
    if not bound.success:
        return bound
    eq = parse_assign_op(document, bound.end)
    if not eq.success:
        return ParseResult("const_assign_stmt", False, "expected '='", bound.end, bound.end + 1)
    rhs = parse_expression(document, eq.end)
    if not rhs.success:
        return rhs
    return ParseResult("const_assign_stmt", True, (bound, rhs), offset, rhs.end)


# spawn_stmt ::= 'spawn' 'eternal'? expr
def parse_spawn_stmt(document, offset):
    kw = expect_keyword(document, offset, 'spawn')
    if not kw.success:
        return ParseResult("spawn_stmt", False, "expected 'spawn'", offset, offset + 1)
    pos = kw.end
    eternal = expect_keyword(document, pos, 'eternal')
    if eternal.success:
        pos = eternal.end
    value = parse_expression(document, pos)
    if not value.success:
        return value
    return ParseResult("spawn_stmt", True, (eternal.success, value), offset, value.end)


# go_stmt ::= 'go' expr (',' expr)?
#
# The original grammar had this as two bare adjacent exprs ('go expr
# expr'), which is unparseable in general: application has no
# terminator, so the first expr always greedily swallows the second (the
# same reason a comma separates print_stmt's and assert_stmt's optional
# second expr). Changed to require a comma; the second expr - the value
# STOP returns to this go - is optional and defaults to None when absent
# (represented here as Python None, matching how print_stmt/assert_stmt
# represent their own missing optional expr).
def parse_go_stmt(document, offset):
    kw = expect_keyword(document, offset, 'go')
    if not kw.success:
        return ParseResult("go_stmt", False, "expected 'go'", offset, offset + 1)
    target = parse_expression(document, kw.end)
    if not target.success:
        return target
    pos = skip_blanks(document, target.end)
    if pos < len(document) and document[pos] == ',':
        value = parse_expression(document, pos + 1)
        if not value.success:
            return value
        return ParseResult("go_stmt", True, (target, value), offset, value.end)
    return ParseResult("go_stmt", True, (target, None), offset, target.end)


# assign_stmt ::= (assign_target_list '=')+ tuple_rule
#
# Each '=' segment is parsed permissively first (as a tuple_rule, same as
# the final value) just to find where it ends - we can't tell a target
# from the final value until we see whether an '=' follows it. Once a
# real '=' has been found, though, this is committed to being an
# assignment: from there on, an invalid target (_as_assign_target) or a
# broken right-hand side is a genuine syntax error, not a "wrong
# statement kind, let expr_stmt/aug_assign_stmt have a turn" signal -
# that distinction is what "expected '='" (type "assign_stmt", the only
# shallow/retry-safe failure) vs. type "assign_stmt_target" (committed)
# communicates to parse_simple_stmt.
def parse_assign_stmt(document, offset):
    targets = []
    cur = parse_tuple(document, offset)
    if not cur.success:
        return ParseResult("assign_stmt", False, cur.value, cur.start, cur.end)
    start = cur.start
    eq = parse_assign_op(document, cur.end)
    if not eq.success:
        return ParseResult("assign_stmt", False, "expected '='", cur.end, cur.end + 1)
    while True:
        target = _as_assign_target(document, cur)
        if not target.success:
            return ParseResult("assign_stmt_target", False, target.value, target.start, target.end)
        targets.append(target)
        nxt = parse_tuple(document, eq.end)
        if not nxt.success:
            return ParseResult("assign_stmt_target", False, nxt.value, nxt.start, nxt.end)
        cur = nxt
        eq2 = parse_assign_op(document, cur.end)
        if not eq2.success:
            break
        eq = eq2
    return ParseResult("assign_stmt", True, (targets, cur), start, cur.end)


# aug_assign_stmt ::= assign_target_list aug_assign_op tuple_rule
# See parse_assign_stmt above for why the target is validated only after
# a real aug_assign_op is found, and why that failure gets its own type
# ("aug_assign_stmt_target") distinct from the shallow "no operator here
# at all" one.
def parse_aug_assign_stmt(document, offset):
    lhs = parse_tuple(document, offset)
    if not lhs.success:
        return ParseResult("aug_assign_stmt", False, lhs.value, lhs.start, lhs.end)
    op = parse_aug_assign_op(document, lhs.end)
    if not op.success:
        return ParseResult("aug_assign_stmt", False, "expected an augmented assignment operator", lhs.end, lhs.end + 1)
    lhs = _as_assign_target(document, lhs)
    if not lhs.success:
        return ParseResult("aug_assign_stmt_target", False, lhs.value, lhs.start, lhs.end)
    rhs = parse_tuple(document, op.end)
    if not rhs.success:
        return ParseResult("aug_assign_stmt_target", False, rhs.value, rhs.start, rhs.end)
    return ParseResult("aug_assign_stmt", True, (lhs, op, rhs), lhs.start, rhs.end)


# expr_stmt ::= expr_rule   (note: *not* a full nary_expr/tuple_rule - a
# bare expression statement is meant for things like function calls, not
# arithmetic left lying around; see parse_simple_stmt for how this plays
# with assign_stmt/aug_assign_stmt sharing the same starting prefix)
def parse_expr_stmt(document, offset):
    expr = parse_expr_rule(document, offset)
    if not expr.success:
        return expr
    return ParseResult("expr_stmt", True, expr, expr.start, expr.end)


# import_names_seq ::= NAME (',' NAME)*
def parse_import_names_seq(document, offset):
    first = parse_identifier(document, offset)
    if not first.success:
        return first
    names = [first]
    pos = first.end
    while True:
        p = skip_blanks(document, pos)
        if p >= len(document) or document[p] != ',':
            break
        nxt = parse_identifier(document, p + 1)
        if not nxt.success:
            return nxt
        names.append(nxt)
        pos = nxt.end
    return ParseResult("import_names_seq", True, names, offset, pos)


def parse_import_name(document, offset):
    kw = expect_keyword(document, offset, 'import')
    if not kw.success:
        return ParseResult("import_name", False, "expected 'import'", offset, offset + 1)
    names = parse_import_names_seq(document, kw.end)
    if not names.success:
        return names
    return ParseResult("import_name", True, names, offset, names.end)


def parse_import_from(document, offset):
    kw = expect_keyword(document, offset, 'from')
    if not kw.success:
        return ParseResult("import_from", False, "expected 'from'", offset, offset + 1)
    mod = parse_identifier(document, kw.end)
    if not mod.success:
        return mod
    imp = expect_keyword(document, mod.end, 'import')
    if not imp.success:
        return ParseResult("import_from", False, "expected 'import'", mod.end, mod.end + 1)
    pos = skip_blanks(document, imp.end)
    if pos < len(document) and document[pos] == '*':
        return ParseResult("import_from", True, (mod, "*"), offset, pos + 1)
    names = parse_import_names_seq(document, imp.end)
    if not names.success:
        return names
    return ParseResult("import_from", True, (mod, names), offset, names.end)


# import_stmt ::= (import_name | import_from) ';'? NL
def parse_import_stmt(document, offset):
    stmt = parse_import_name(document, offset)
    if not stmt.success:
        alt = parse_import_from(document, offset)
        if not alt.success:
            return ParseResult("import_stmt", False, "expected an import statement", offset, offset + 1)
        stmt = alt
    pos = skip_line_blanks(document, stmt.end)
    if pos < len(document) and document[pos] == ';':
        pos = skip_line_blanks(document, pos + 1)
    end = pos
    if end < len(document) and document[end] == '\r':
        end += 1
    if end < len(document) and document[end] == '\n':
        end += 1
    elif end < len(document):
        return ParseResult("import_stmt", False, "expected end of line after import", end, end + 1)
    return ParseResult("import_stmt", True, stmt, offset, end)


# simple_stmt ::= 'atomically'? ( const_assign_stmt | await_stmt | var_stmt
#     | finally_stmt | invariant_stmt | del_stmt | spawn_stmt | trap_stmt
#     | go_stmt | print_stmt | pass_stmt | break_stmt | continue_stmt
#     | return_stmt | sequential_stmt | global_stmt | builtin_stmt
#     | assert_stmt | aug_assign_stmt | assign_stmt | expr_stmt )
#
# assign_stmt/aug_assign_stmt/expr_stmt all start by parsing an expression,
# so they're tried last, in that order - each is a self-contained,
# side-effect-free attempt, so trying the next one after a failure is safe.
# Alternatives with their own leading keyword: once that keyword has
# matched we're committed, so a deeper failure must be propagated rather
# than swallowed while we try the remaining alternatives (which is what a
# plain try-each-in-turn loop would otherwise do).
_SIMPLE_STMT_KEYWORDS = {
    'const': parse_const_assign_stmt,
    'await': parse_await_stmt,
    'var': parse_var_stmt,
    'finally': parse_finally_stmt,
    'invariant': parse_invariant_stmt,
    'del': parse_del_stmt,
    'spawn': parse_spawn_stmt,
    'trap': parse_trap_stmt,
    'go': parse_go_stmt,
    'print': parse_print_stmt,
    'pass': parse_pass_stmt,
    'break': parse_break_stmt,
    'continue': parse_continue_stmt,
    'return': parse_return_stmt,
    'sequential': parse_sequential_stmt,
    'global': parse_global_stmt,
    'builtin': parse_builtin_stmt,
    'assert': parse_assert_stmt,
}


def parse_simple_stmt(document, offset):
    start = offset
    pos = offset
    atomic = expect_keyword(document, pos, 'atomically')
    if atomic.success:
        pos = atomic.end

    kw = parse_keyword(document, pos)
    if kw.success and kw.value in _SIMPLE_STMT_KEYWORDS:
        result = _SIMPLE_STMT_KEYWORDS[kw.value](document, pos)
    else:
        # None of these start with a reserved keyword, so there's no
        # 1-token lookahead to dispatch on - try them in turn. Each is a
        # self-contained, side-effect-free attempt (no shared state), so
        # falling through to the next on failure is safe *only* while
        # assign_stmt/aug_assign_stmt fail "shallowly" (type "assign_stmt"/
        # "aug_assign_stmt" - no operator here at all): once one of them
        # has found a real '='/aug-assign-op it's committed (type
        # "..._target"), and a failure past that point (an invalid target,
        # or a broken right-hand side) is a real syntax error, not a
        # signal to let expr_stmt have a turn.
        result = parse_assign_stmt(document, pos)
        if not result.success and result.type == "assign_stmt":
            result = parse_aug_assign_stmt(document, pos)
        if not result.success and result.type in ("assign_stmt", "aug_assign_stmt"):
            result = parse_expr_stmt(document, pos)
            if not result.success:
                # None of the three matched at all (they all bottom out
                # in "couldn't find an expression here"), so this is a
                # plain "not a simple_stmt", not a deeper commit failure -
                # report it at the true starting point (before an
                # 'atomically' prefix that turned out to lead nowhere),
                # so callers trying other statement kinds can tell it's
                # safe to retry from scratch. Tagged with the dedicated
                # "simple_stmt" type - mirroring parse_compound_stmt's own
                # "expected a compound statement" sentinel - rather than
                # reusing whatever type expr_stmt's failure happened to
                # carry: parse_stmt needs a signal it can check
                # unconditionally, since *position* alone can't tell
                # "never got going" apart from "a real commit failure
                # that happens to be reported at this exact spot" (e.g.
                # "?x = 3" is rejected right at its own first character).
                result = ParseResult("simple_stmt", False, result.value, start, start + 1)

    if not result.success:
        return result
    if atomic.success:
        return ParseResult("simple_stmt", True, ("atomically", result), start, result.end)
    return result


def _is_bare_expr_stmt(stmt):
    """Whether `stmt` (one parse_simple_stmt result) is a plain
    expr_stmt with no assignment operator anywhere in it - the shape
    that's compatible with "the rest of this line is a stray compare_op/
    logic_op, so the writer probably meant a comparison/logical
    expression to actually be a statement (or typoed '=' as '==')" -
    see _stray_operator_hint, used only to make that specific mistake's
    error message friendlier, not to change what parses."""
    if stmt.type == "expr_stmt":
        return True
    if stmt.type == "simple_stmt" and isinstance(stmt.value, tuple) and stmt.value[0] == "atomically":
        return stmt.value[1].type == "expr_stmt"
    return False


def _stray_operator_hint(document, pos):
    """None, or a friendlier explanation for the common case where a
    complete expr_stmt is immediately followed by a comparison or
    logic operator - e.g. "1 == 2" or "x and y" sitting alone as a
    whole statement. expr_stmt is deliberately just an expr_rule (see
    parse_expr_stmt) - one precedence level tighter than a full
    comparison/logical expr - because a bare comparison/logic
    expression has nowhere for its result to go, so Harmony doesn't
    allow one as a statement by itself; this is almost always either a
    stray '==' meant to be '=' (assignment), or a condition that was
    meant to go after 'if'/'while' and got typed on its own instead.
    Without this, the resulting error ("expected end of line after
    statement", pointing at the operator) is accurate but doesn't
    explain why parsing stopped exactly there - see the docstring's own
    motivating report."""
    op = parse_compare_op(document, pos)
    if op.success:
        if op.value == '==':
            return ("'==' is a comparison, not a statement - its result would "
                    "just be discarded, so this looks like a typo of '=' "
                    "(assignment), or a condition missing its 'if'/'while'")
        return ("'%s' is a comparison, not a statement - its result would "
                "just be discarded, so it needs an 'if'/'while' in front of "
                "it (or somewhere else to be used)" % op.value)
    op = parse_logic_op(document, pos)
    if op.success:
        return ("'%s' is a logical expression, not a statement - its result "
                "would just be discarded, so it needs an 'if'/'while' in "
                "front of it (or somewhere else to be used)" % op.value)
    return None


# one_line_stmt ::= simple_stmt (';'? NL | ';' one_line_stmt)
def parse_one_line_stmt(document, offset):
    stmt = parse_simple_stmt(document, offset)
    if not stmt.success:
        return stmt
    pos = skip_line_blanks(document, stmt.end)
    if pos < len(document) and document[pos] == ';':
        pos += 1
        pos2 = skip_line_blanks(document, pos)
        if pos2 < len(document) and document[pos2] not in '\r\n':
            rest = parse_one_line_stmt(document, pos)
            if not rest.success:
                return rest
            return ParseResult("one_line_stmt", True, (stmt, rest), stmt.start, rest.end)
        pos = pos2
    end = pos
    if end < len(document) and document[end] == '\r':
        end += 1
    if end < len(document) and document[end] == '\n':
        end += 1
    elif end < len(document):
        hint = _stray_operator_hint(document, end) if _is_bare_expr_stmt(stmt) else None
        message = "expected end of line after statement"
        if hint is not None:
            message = "%s (%s)" % (message, hint)
        return ParseResult("one_line_stmt", False, message, end, end + 1)
    return ParseResult("one_line_stmt", True, (stmt,), stmt.start, end)


# ---------------------------------------------------------------------------
# Compound statements and indentation-sensitive blocks.
# `indent` is always "the column the enclosing statement sits at"; a block
# that statement opens must be indented strictly further than that.
# ---------------------------------------------------------------------------

def measure_indent(document, offset):
    """offset must be at the start of a source line. Returns (width,
    offset_after_the_leading_whitespace)."""
    start = offset
    while offset < len(document) and document[offset] in (' ', '\t'):
        offset += 1
    return offset - start, offset


def next_logical_line(document, offset):
    """offset must be at the start of a source line. Skips blank and
    comment-only lines (they don't affect indentation, same as Python) and
    returns (width, offset) for the next line with real content, or
    (None, offset) at end of file."""
    pos = offset
    while True:
        width, after_indent = measure_indent(document, pos)
        rest = after_indent
        if rest < len(document) and document[rest] == '#':
            while rest < len(document) and document[rest] not in '\r\n':
                rest += 1
        if rest >= len(document):
            return None, rest
        if document[rest] in '\r\n':
            if document[rest] == '\r':
                rest += 1
            if rest < len(document) and document[rest] == '\n':
                rest += 1
            pos = rest
            continue
        return width, after_indent


# block ::= normal_block | one_line_stmt
def parse_block(document, offset, indent):
    pos = skip_line_blanks(document, offset)
    if pos < len(document) and document[pos] not in '\r\n':
        return parse_one_line_stmt(document, offset)
    return parse_normal_block(document, offset, indent)


# normal_block ::= INDENT block_stmts DEDENT   (the grammar's rarer
# "dummy block" alternative, INDENT INDENT block DEDENT, isn't implemented
# - see the module docstring)
def parse_normal_block(document, offset, indent):
    pos = skip_line_blanks(document, offset)
    if pos < len(document) and document[pos] not in '\r\n':
        return ParseResult("normal_block", False, "expected end of line before an indented block", pos, pos + 1)
    if pos < len(document) and document[pos] == '\r':
        pos += 1
    if pos < len(document) and document[pos] == '\n':
        pos += 1
    width, body_start = next_logical_line(document, pos)
    if width is None or width <= indent:
        return ParseResult("normal_block", False, "expected an indented block", pos, pos + 1)
    stmts = []
    cur = body_start
    while True:
        stmt = parse_stmt(document, cur, width)
        if not stmt.success:
            return stmt
        stmts.append(stmt)
        w, next_start = next_logical_line(document, stmt.end)
        if w is None or w < width:
            return ParseResult("normal_block", True, stmts, offset, stmt.end)
        if w > width:
            return ParseResult("normal_block", False, "unexpected indent", next_start, next_start + 1)
        cur = next_start


def parse_if_block(document, offset, indent):
    kw = expect_keyword(document, offset, 'if')
    if not kw.success:
        return ParseResult("if_block", False, "expected 'if'", offset, offset + 1)
    with _colon_header():
        cond = parse_expression(document, kw.end)
        if not cond.success:
            return cond
        colon = expect_char(document, cond.end, ':')
        if not colon.success:
            return ParseResult("if_block", False, "expected ':'", cond.end, cond.end + 1)
    body = parse_block(document, colon.end, indent)
    if not body.success:
        return body

    elifs = []
    pos = body.end
    while True:
        w, line_start = next_logical_line(document, pos)
        if w != indent:
            break
        kw2 = parse_keyword(document, line_start)
        if not (kw2.success and kw2.value == 'elif'):
            break
        e = parse_elif_block(document, line_start, indent)
        if not e.success:
            return e
        elifs.append(e)
        pos = e.end

    else_block = None
    w, line_start = next_logical_line(document, pos)
    if w == indent:
        kw2 = parse_keyword(document, line_start)
        if kw2.success and kw2.value == 'else':
            e = parse_else_block(document, line_start, indent)
            if not e.success:
                return e
            else_block = e
            pos = e.end

    return ParseResult("if_block", True, (cond, body, elifs, else_block), offset, pos)


def parse_elif_block(document, offset, indent):
    kw = expect_keyword(document, offset, 'elif')
    if not kw.success:
        return ParseResult("elif_block", False, "expected 'elif'", offset, offset + 1)
    with _colon_header():
        cond = parse_expression(document, kw.end)
        if not cond.success:
            return cond
        colon = expect_char(document, cond.end, ':')
        if not colon.success:
            return ParseResult("elif_block", False, "expected ':'", cond.end, cond.end + 1)
    body = parse_block(document, colon.end, indent)
    if not body.success:
        return body
    return ParseResult("elif_block", True, (cond, body), offset, body.end)


def parse_else_block(document, offset, indent):
    kw = expect_keyword(document, offset, 'else')
    if not kw.success:
        return ParseResult("else_block", False, "expected 'else'", offset, offset + 1)
    with _colon_header():
        colon = expect_char(document, kw.end, ':')
        if not colon.success:
            return ParseResult("else_block", False, "expected ':'", kw.end, kw.end + 1)
    body = parse_block(document, colon.end, indent)
    if not body.success:
        return body
    return ParseResult("else_block", True, body, offset, body.end)


def parse_while_block(document, offset, indent):
    kw = expect_keyword(document, offset, 'while')
    if not kw.success:
        return ParseResult("while_block", False, "expected 'while'", offset, offset + 1)
    with _colon_header():
        cond = parse_expression(document, kw.end)
        if not cond.success:
            return cond
        colon = expect_char(document, cond.end, ':')
        if not colon.success:
            return ParseResult("while_block", False, "expected ':'", cond.end, cond.end + 1)
    body = parse_block(document, colon.end, indent)
    if not body.success:
        return body
    return ParseResult("while_block", True, (cond, body), offset, body.end)


def parse_for_block(document, offset, indent):
    with _colon_header():
        it = parse_iter_parse(document, offset)
        if not it.success:
            return it
        colon = expect_char(document, it.end, ':')
        if not colon.success:
            return ParseResult("for_block", False, "expected ':'", it.end, it.end + 1)
    body = parse_block(document, colon.end, indent)
    if not body.success:
        return body
    return ParseResult("for_block", True, (it, body), offset, body.end)


def parse_atomic_block(document, offset, indent):
    kw = expect_keyword(document, offset, 'atomically')
    if not kw.success:
        return ParseResult("atomic_block", False, "expected 'atomically'", offset, offset + 1)
    with _colon_header():
        colon = expect_char(document, kw.end, ':')
        if not colon.success:
            return ParseResult("atomic_block", False, "expected ':'", kw.end, kw.end + 1)
    body = parse_block(document, colon.end, indent)
    if not body.success:
        return body
    return ParseResult("atomic_block", True, body, offset, body.end)


# let_decl ::= 'let' bound '=' tuple_rule NL?
def parse_let_decl(document, offset):
    kw = expect_keyword(document, offset, 'let')
    if not kw.success:
        return ParseResult("let_decl", False, "expected 'let'", offset, offset + 1)
    bound = parse_bound(document, kw.end)
    if not bound.success:
        return bound
    eq = parse_assign_op(document, bound.end)
    if not eq.success:
        return ParseResult("let_decl", False, "expected '='", bound.end, bound.end + 1)
    rhs = parse_tuple(document, eq.end)
    if not rhs.success:
        return rhs
    return ParseResult("let_decl", True, (bound, rhs), offset, _skip_optional_nl(document, rhs.end))


# when_decl ::= 'when' ('exists' bound 'in' expr | expr) NL?
def parse_when_decl(document, offset):
    kw = expect_keyword(document, offset, 'when')
    if not kw.success:
        return ParseResult("when_decl", False, "expected 'when'", offset, offset + 1)
    exists_kw = expect_keyword(document, kw.end, 'exists')
    if exists_kw.success:
        bound = parse_bound(document, exists_kw.end)
        if not bound.success:
            return bound
        in_kw = expect_keyword(document, bound.end, 'in')
        if not in_kw.success:
            return ParseResult("when_decl", False, "expected 'in'", bound.end, bound.end + 1)
        cond = parse_expression(document, in_kw.end)
        if not cond.success:
            return cond
        return ParseResult("when_decl", True, ("exists", bound, cond), offset, _skip_optional_nl(document, cond.end))
    cond = parse_expression(document, kw.end)
    if not cond.success:
        return cond
    return ParseResult("when_decl", True, ("cond", cond), offset, _skip_optional_nl(document, cond.end))


# let_when_decl ::= (let_decl | when_decl) let_when_decl?
def parse_let_when_decl(document, offset):
    first = parse_let_decl(document, offset)
    if not first.success:
        first = parse_when_decl(document, offset)
        if not first.success:
            return ParseResult("let_when_decl", False, "expected 'let' or 'when'", offset, offset + 1)
    rest = parse_let_when_decl(document, first.end)
    if rest.success:
        return ParseResult("let_when_decl", True, [first] + rest.value, offset, rest.end)
    return ParseResult("let_when_decl", True, [first], offset, first.end)


def parse_let_when_block(document, offset, indent):
    with _colon_header():
        decls = parse_let_when_decl(document, offset)
        if not decls.success:
            return decls
        colon = expect_char(document, decls.end, ':')
        if not colon.success:
            return ParseResult("let_when_block", False, "expected ':'", decls.end, decls.end + 1)
    body = parse_block(document, colon.end, indent)
    if not body.success:
        return body
    return ParseResult("let_when_block", True, (decls, body), offset, body.end)


# method_decl ::= 'def' NAME bound ('returns' NAME)? ':' block
def parse_method_decl(document, offset, indent):
    kw = expect_keyword(document, offset, 'def')
    if not kw.success:
        return ParseResult("method_decl", False, "expected 'def'", offset, offset + 1)
    with _colon_header():
        name = parse_identifier(document, kw.end)
        if not name.success:
            return name
        params = parse_bound(document, name.end)
        if not params.success:
            return params
        pos = params.end
        returns = None
        ret_kw = expect_keyword(document, pos, 'returns')
        if ret_kw.success:
            ret_name = parse_identifier(document, ret_kw.end)
            if not ret_name.success:
                return ret_name
            returns = ret_name
            pos = ret_name.end
        colon = expect_char(document, pos, ':')
        if not colon.success:
            return ParseResult("method_decl", False, "expected ':'", pos, pos + 1)
    body = parse_block(document, colon.end, indent)
    if not body.success:
        return body
    return ParseResult("method_decl", True, (name, params, returns, body), offset, body.end)


# Each alternative has its own unique leading keyword, so dispatch on it
# and commit: a failure past that point is a real syntax error, not a cue
# to try something else.
_COMPOUND_STMT_KEYWORDS = {
    'if': parse_if_block,
    'while': parse_while_block,
    'for': parse_for_block,
    'let': parse_let_when_block,
    'when': parse_let_when_block,
    'def': parse_method_decl,
}


# compound_stmt ::= 'atomically' (':' block | if_block | while_block
#                                | for_block | let_when_block | method_decl)
#                 | if_block | while_block | for_block | let_when_block
#                 | method_decl
#
# Folded from the grammar's original ATOMICALLY? (... | atomic_block |
# ...), which put ATOMICALLY in two places - compound_stmt's optional
# prefix and atomic_block's own leading token - making a plain "is there
# a ':' " lookahead necessary just to tell which one applies. Same
# language (module a pointless 'atomically atomically: block' stutter
# the old shape technically also accepted), one deterministic dispatch:
# after 'atomically', either a ':' follows directly (it's a bare atomic
# block) or one of the compound keywords does (it's that compound
# statement, atomically).
def parse_compound_stmt(document, offset, indent):
    atomic = expect_keyword(document, offset, 'atomically')
    if atomic.success:
        with _colon_header():
            colon = expect_char(document, atomic.end, ':')
        if colon.success:
            result = parse_atomic_block(document, offset, indent)
        else:
            kw = parse_keyword(document, atomic.end)
            if not (kw.success and kw.value in _COMPOUND_STMT_KEYWORDS):
                return ParseResult("compound_stmt", False, "expected a compound statement after 'atomically'", atomic.end, atomic.end + 1)
            result = _COMPOUND_STMT_KEYWORDS[kw.value](document, atomic.end, indent)
        if not result.success:
            return result
        return ParseResult("compound_stmt", True, ("atomically", result), offset, result.end)

    kw = parse_keyword(document, offset)
    if not (kw.success and kw.value in _COMPOUND_STMT_KEYWORDS):
        return ParseResult("compound_stmt", False, "expected a compound statement", offset, offset + 1)
    return _COMPOUND_STMT_KEYWORDS[kw.value](document, offset, indent)


# label ::= (NAME ':')+
def parse_label(document, offset):
    parts = []
    start = offset
    cur = offset
    while True:
        name = parse_identifier(document, cur)
        if not name.success:
            break
        colon = expect_char(document, name.end, ':')
        if not colon.success:
            break
        parts.append(name)
        cur = colon.end
    if not parts:
        return ParseResult("label", False, "expected a label", offset, offset + 1)
    return ParseResult("label", True, parts, start, cur)


# stmt ::= (label? | ':') (';'* NL | one_line_stmt | compound_stmt | import_stmt)
#        | (label | ':') normal_block
#
# `indent` is the column this statement itself sits at (needed only in
# case this turns out to be a compound_stmt, or a labeled block, that
# opens a nested block of its own).
def parse_stmt(document, offset, indent):
    """Thin wrapper around _parse_stmt_inner that scopes _stmt_indent to
    exactly the span of parsing this one statement - `indent` here is
    always this statement's own starting column (both call sites -
    parse_program's loop and parse_normal_block's loop - call this right
    after measuring the current line's own width), which is exactly what
    _deeper_indent_follows needs to judge a later line as this
    statement's continuation. Restored on every exit (success, failure,
    or an exception) so a statement's own continuation reach never leaks
    into whatever's parsed after it returns."""
    old = _stmt_indent[0]
    _stmt_indent[0] = indent
    try:
        return _parse_stmt_inner(document, offset, indent)
    finally:
        _stmt_indent[0] = old


def _parse_stmt_inner(document, offset, indent):
    start = offset
    label = parse_label(document, offset)
    bare_colon = None
    if label.success:
        after_prefix = label.end
        prefix = label
    else:
        bare_colon = expect_char(document, offset, ':')
        after_prefix = bare_colon.end if bare_colon.success else offset
        prefix = bare_colon if bare_colon.success else None
    has_prefix = label.success or (bare_colon is not None and bare_colon.success)

    # blank statement: (label? | ':') ';'* NL - but when a label/':' prefix
    # is present, this exact shape (prefix, then nothing but NL) is also
    # how "(label|':') normal_block" starts; the two only diverge on
    # whether the *following* line is indented deeper than this block, so
    # peek at it before committing to "blank".
    p = skip_line_blanks(document, after_prefix)
    while p < len(document) and document[p] == ';':
        p = skip_line_blanks(document, p + 1)
    if p >= len(document) or document[p] in '\r\n':
        end = p
        if end < len(document) and document[end] == '\r':
            end += 1
        if end < len(document) and document[end] == '\n':
            end += 1
        if has_prefix:
            w, _ = next_logical_line(document, end)
            if w is not None and w > indent:
                block = parse_normal_block(document, after_prefix, indent)
                if block.success:
                    return ParseResult("stmt", True, ("labeled_block", prefix, block), start, block.end)
                return block
        return ParseResult("stmt", True, ("blank", prefix), start, end)

    # one_line_stmt/compound_stmt/import_stmt are tried in turn, but once
    # one of them has recognized its leading keyword it is committed: a
    # failure that starts *past* after_prefix happened after that
    # commitment and is a real syntax error, not a signal to try the next
    # alternative. Only a failure sitting exactly at after_prefix (never
    # got going at all) is safe to shrug off and retry.
    #
    # one_line_stmt adds a *type* check on top of the position one, unlike
    # compound_stmt/import_stmt below: position alone isn't enough here,
    # since a genuine commit failure (type "assign_stmt_target" and
    # friends) can still happen to be reported at after_prefix itself -
    # e.g. "?x = 3" is rejected right at its own first character, which
    # a bare position check would wrongly read as "never got going".
    # parse_simple_stmt's dedicated "simple_stmt" failure type is the
    # authoritative signal for that case; the position check is still
    # needed alongside it so a *chained* statement's shallow failure
    # (";" - a "simple_stmt" a few statements in) isn't mistaken for the
    # top-level attempt itself never having started.
    one_line = parse_one_line_stmt(document, after_prefix)
    if one_line.success:
        return ParseResult("stmt", True, ("simple", prefix, one_line), start, one_line.end)
    if one_line.type != "simple_stmt" or one_line.start != after_prefix:
        return one_line

    compound = parse_compound_stmt(document, after_prefix, indent)
    if compound.success:
        return ParseResult("stmt", True, ("compound", prefix, compound), start, compound.end)
    if compound.start != after_prefix:
        return compound

    imp = parse_import_stmt(document, after_prefix)
    if imp.success:
        return ParseResult("stmt", True, ("import", prefix, imp), start, imp.end)
    if imp.start != after_prefix:
        return imp

    if has_prefix:
        block = parse_normal_block(document, after_prefix, indent)
        if block.success:
            return ParseResult("stmt", True, ("labeled_block", prefix, block), start, block.end)
        return block

    return ParseResult("stmt", False, "expected a statement", offset, offset + 1)


# program ::= stmt* EOF
def parse_program(document):
    stmts = []
    pos = 0
    while True:
        w, line_start = next_logical_line(document, pos)
        if w is None:
            return ParseResult("program", True, stmts, 0, line_start)
        if w != 0:
            return ParseResult("program", False, "unexpected indentation at top level", line_start, line_start + 1)
        stmt = parse_stmt(document, line_start, 0)
        if not stmt.success:
            return stmt
        stmts.append(stmt)
        pos = stmt.end


# doc = "1 if 2 for 3"
# pr = parse_tuple(doc, 0)
# print(pr)
