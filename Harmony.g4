grammar Harmony;

tokens { INDENT, DEDENT }

@lexer::header{
from .custom_denter import ModifiedDenterHelper
from .HarmonyParser import HarmonyParser
}
@lexer::members {

opened_for = 0
opened = 0

class HarmonyDenter(ModifiedDenterHelper):
    def __init__(self, lexer, nl_token, colon_token, indent_token, dedent_token, ignore_eof):
        super().__init__(lexer, nl_token, colon_token, indent_token, dedent_token, ignore_eof)
        self.lexer: HarmonyLexer = lexer

    def pull_token(self):
        return super(HarmonyLexer, self.lexer).nextToken()

denter = None
def nextToken(self):
    if not self.denter:
        self.denter = self.HarmonyDenter(self, self.NL, self.COLON, HarmonyParser.INDENT, HarmonyParser.DEDENT, ignore_eof=False)
    token = self.denter.next_token()
    return token
}

NL: '\r'? '\n' (' '* | '\t'*) {
if self.opened or self.opened_for:
    self.skip()
}; // For tabs just switch out ' '* with '\t'*
WS : (' '+ | '\t'+ | '\\' NL | COMMENT ) -> skip ; // skip just white space and '\' for multiline statements

fragment COMMENT
    : OPEN_MULTI_COMMENT .*? CLOSE_MULTI_COMMENT
    | COMMENT_START ~[\r\n\f]*
    ;

program: (stmt)* EOF;

// Adapted from Python3's Antlr4 Grammar
import_stmt: (import_name | import_from) SEMI_COLON? NL;
import_name: IMPORT import_names_seq;
import_from: FROM NAME IMPORT (STAR | import_names_seq);
import_names_seq: NAME (COMMA NAME)*;

tuple_bound
    : NAME
    | OPEN_PAREN bound CLOSE_PAREN
    | OPEN_BRACK bound CLOSE_BRACK
    | OPEN_PAREN CLOSE_PAREN
    | OPEN_BRACK CLOSE_BRACK
    ;
bound: (tuple_bound COMMA)* tuple_bound;

// Three precedence levels, loosest to tightest: logic_op binds
// loosest, then compare_op, then arith_op (everything else), which are
// all still flat/left-to-right *among themselves* - Harmony doesn't
// distinguish + from *, say - only the three levels are ordered
// relative to each other. See nary_expr/logic_expr/compare_expr/
// arith_expr below for how these combine into the actual precedence
// climb.
logic_op
    : 'and'
    | 'or'
    | '=>'
    ;

compare_op
    : '=='
    | '!='
    | '<'
    | '<='
    | '>'
    | '>='
    ;

arith_op
    : '&'
    | '|'
    | '^'
    | '-'
    | '+'
    | '*'
    | '//'
    | '/'
    | '%'
    | 'mod'
    | '**'
    | '<<'
    | '>>'
;

// '?' (address-of) is deliberately NOT here - unlike every other
// unary_op, its operand isn't an unrestricted expr_rule. See
// question_operand and expr_rule below.
unary_op
    : '-'
    | '~'
    | '!'
    | 'abs'
    | 'all'
    | 'any'
    | 'bin'
    | 'choose'
    | 'dict'
    | 'get_context'
    | 'get_ident'
    | 'hash'
    | 'hex'
    | 'int'
    | 'keys'
    | 'len'
    | 'list'
    | 'max'
    | 'min'
    | 'not'
    | 'oct'
    | 'reversed'
    | 'set'
    | 'sorted'
    | 'str'
    | 'sum'
    | 'type'
    | 'zip'
    ;

basic_expr
    : INT                    #int
    | BOOL                   #bool
    | ATOM                   #atom
    | NAME                   #name
    | STRING                 #str
    | NONE                   #none
    | OPEN_BRACES set_rule? COMMA? CLOSE_BRACES #set_rule_1
    | OPEN_BRACES COLON CLOSE_BRACES #empty_dict
    | OPEN_PAREN tuple_rule? CLOSE_PAREN  #paren_tuple
    | OPEN_BRACK tuple_rule? CLOSE_BRACK  #bracket_tuple
    | LAMBDA bound COLON nary_expr 'end'  #lambda_expr
    ;

set_rule
    : nary_expr (
          COLON nary_expr (iter_parse | (COMMA nary_expr COLON nary_expr)*)
        | iter_parse
        | RANGE nary_expr
        | (COMMA nary_expr)*
    )
;

iter_parse
    : for_parse (NL? (for_parse | where_parse))*
;

for_parse
    : FOR (bound | bound COLON bound) IN nary_expr
;
where_parse
    : WHERE nary_expr
;

tuple_rule
    : nary_expr (iter_parse | (COMMA nary_expr)* COMMA?)
;

nary_expr
    : expr_rule NOT? IN expr_rule
    | expr_rule IF nary_expr ELSE expr_rule
    | logic_expr
;

// logic_expr, like arith_expr below, is flat CFG-wise but carries an
// extra semantic restriction plain BNF can't express: a chain of 2+
// logic_op's is only legal if they're all the *same* operator, and that
// operator is 'and' or 'or' - never '=>'. So "x and y and z" and
// "x or y or z" are legal (evaluated left to right, same as before),
// but "x and y or z" and "x => y => z" are both rejected as ambiguous;
// a single logic_op of any kind (including a lone '=>') is always fine,
// since there's nothing to disambiguate.
logic_expr: compare_expr (logic_op compare_expr)*;
compare_expr: arith_expr (compare_op arith_expr)*;

// arith_expr is flat CFG-wise, but a chain of 2+ arith_op's carries its
// own extra semantic restriction:
//   - all identical, and NOT one of '<<' '>>' '**', AND NOT one of the
//     multiplicative-tier ops other than '*' (see below): legal,
//     unchanged, evaluated left to right (e.g. "a & b & c", "a + b + c")
//     - &, |, ^, +, - are all associative (&, |, ^ are commutative too),
//     so no grouping needs disambiguating;
//   - all identical, and IS one of '<<' '>>' '**': ambiguous even
//     though it's the same operator repeated, because none of these
//     are associative - (a<<b)<<c != a<<(b<<c), (a**b)**c != a**(b**c)
//     - so "a << b << c" is a parse error just like a mix would be;
//   - not all identical, but every operator is one of
//     { +, -, *, /, //, mod, % }: legal, but *regrouped* by standard
//     arithmetic precedence - the multiplicative subset
//     { *, /, //, mod, % } binds tighter than the additive subset
//     { +, - }, left to right within each tier - so "a + b * c" means
//     "a + (b * c)" - SUBJECT TO the multiplicative-run restriction
//     just below applying within each such multiplicative tier-group;
//   - a MULTIPLICATIVE-TIER run (the whole chain, if there's no '+'/'-'
//     at all, or one segment between two additive-tier operators once
//     regrouped) may have at most one operator that isn't '*', and it
//     must be the LAST one in that run: "a * b * ... * c @ d" (@ being
//     any one of *, /, //, mod, %, including '*' itself) is legal, but
//     "a * b / c * d" and even "a / b / c" (the SAME operator, repeated)
//     are not - deliberately stricter than genuine mathematical
//     ambiguity (division/mod chains are perfectly well-defined left to
//     right); a long run of non-'*' operators is simply too easy for a
//     human reader to misread, so parentheses have to make the grouping
//     explicit instead;
//   - otherwise (different operators, at least one outside the
//     standard-arithmetic set, e.g. "a + b >> c" or "a | b + c"):
//     ambiguous - a parse error, since arith_op has no defined relative
//     precedence beyond that standard-arithmetic subset.
// A single arith_op is always fine regardless of which one it is.
arith_expr: expr_rule (arith_op expr_rule)*;

expr_rule
    : SETINTLEVEL expr_rule
    | SAVE expr_rule
    | STOP expr_rule
    | '?' question_operand
    | unary_op expr_rule
    | application
;

application
    : basic_expr
    | application ARROWID
    | application basic_expr
;

// question_operand ::= (NAME | '(' question_operand ')' | '!' expr_rule)
// (ARROWID | basic_expr)* | (INT | BOOL | ATOM | STRING | NONE). The
// parenthesized alternative recurses (so
// nested/redundant parens are fine) and, like the other two, may
// itself be followed by more (ARROWID | basic_expr) chain material -
// that's what lets "?(!p)[x]" below actually parse: the '!p' part is
// wrapped in parens with nothing following it *inside* them, and the
// qualifying "[x]" is only supplied once the parens close.
//
// '?e' (address-of) requires e to name something addressable in the
// first place - a shared/global variable, or a function, or (extending
// something already addressable) an application/indexing/attribute
// chain rooted at one of those: "?a", "?a.foo", "?a[1]", "?a->b",
// "?f(1)", "?f(1)(2)", "?(f())" (parens are just grouping, so
// "(f())" and "f()" mean the same application either way), and
// "?(!p)[x]" are all legal. That last one needs justifying: "!(?e)
// == e" is the defining round-trip identity behind "a = b" meaning
// "!(?a) = b" in the first place, so "?!p" *alone* just hands back p
// with no addressing accomplished - a meaningless no-op - but
// "?(!p)[x]" address-computes through p's own thunk extended by x
// (e.g. matching "?a[x]" when p holds "?a"), which is genuinely
// useful, exactly the way "a[x] = 1" is. This deliberately does NOT
// extend to a '?'-prefixed base ("?(?a)[x]" stays illegal) - '!' and
// '?' cancel as a *pair*, but there's no matching identity for '?'
// composed with itself.
//
// A bare literal CONSTANT - a number, bool, atom, string, or None - is
// also a legal '?'-operand: "?5" and "?True" address that value
// directly (a value is its own address - there's nothing to compute,
// the value IS the constant written down). Unlike the NAME/'('/'!'
// alternatives, none of the five literal alternatives take a trailing
// (ARROWID | basic_expr)* chain: "?5[0]" isn't "index into the
// constant 5's address" - that's not a shape '?' supports - so it
// stays illegal. Collection literals ("?[1, 2]", "?(1, 2)", "?{1}")
// remain illegal too, for now: see harmony_parser.py's
// _is_constant_literal for what full parity would look like (a
// tuple/list/set/dict literal is a constant only when every element
// recursively is) - that needs its own recursive grammar production
// to express correctly and is left as a follow-up rather than folded
// in here.
//
// "?(1, 2)", "?(a, b)" and "??x" are still illegal: neither a genuine
// multi-element parenthesized tuple nor a bracketed collection is one
// of the five literal alternatives above, and there's no '?'-headed
// alternative here (nesting "??x" stays unsupported for the same
// reason collection literals do).
//
// A bare "?!p" (no parens, nothing following the '!p') is *not*
// rejected by this grammar production - notice the '!' alternative
// ends in a plain '*', not '+'. It has to stay permissive here: the
// "something has to follow, in total" restriction is about the whole
// '?'-operand once any wrapping parens are accounted for, not about
// whatever happens to sit immediately after this one '!' fragment
// syntactically - "?(!p)[x]" is exactly a case where nothing follows
// the '!p' fragment itself (that's inside the parens) even though the
// operand as a whole is genuinely useful. A CFG production can't see
// past its own recursive call to make that whole-operand judgment, so
// (matching how harmony_parser.py, the hand-written recursive-descent
// parser, already handles this same family of restriction - see its
// own comment above parse_question_operand) the no-op case is caught
// as a semantic check in Phase 0 instead of being carved out of the
// grammar itself.
question_operand
    : NAME (ARROWID | basic_expr)*
    | OPEN_PAREN question_operand CLOSE_PAREN (ARROWID | basic_expr)*
    | '!' expr_rule (ARROWID | basic_expr)*
    | INT
    | BOOL
    | ATOM
    | STRING
    | NONE
;

expr: nary_expr;

assign_op
    : EQ
    ;

aug_assign_op
    : 'and='
    | 'or='
    | '=>='
    | '&='
    | '|='
    | '^='
    | '-='
    | '+='
    | '*='
    | '/='
    | '//='
    | '%='
    | 'mod='
    | '**='
    | '>>='
    | '<<='
    ;

// A restricted form of tuple_rule for the left-hand side(s) of '=' and
// augmented-assign - and, since "a = b" is shorthand for "!(?a) = b",
// an assign_target and a '?'-operand are the exact same kind of thing
// (an lvalue) and get the exact same restriction: 'application' is
// legal only when it's identifier-headed in question_operand's sense
// above (a bare NAME, an application/indexing/attribute chain rooted
// in one, or one rooted in a dereference with something further after
// it - "(!p)[x]" - all with any purely-grouping parentheses seen
// through). A bare literal or collection is NOT a legal target any
// more ("5 = 5", "[1,2] = x" are both now rejected) - "a value is its
// own address" stopped being the operative reasoning the moment '?'
// itself stopped accepting one.
//
// '!expr_rule' dereferences a thunk and doesn't restrict its operand's
// *shape*: whether "!e" is actually valid depends on what e evaluates
// to, not on syntax.
//
// There's deliberately no '?expr_rule' alternative: "a = b" is
// shorthand for "!(?a) = b" - any target not already of the primitive
// '!...' form gets wrapped in one more '?' before being assigned into
// - so "?e = val" would itself expand to "!(?(?e)) = val", requiring
// "??e". But '?' now requires *its own* operand to start with an
// identifier (see question_operand above), and "?e" never does (it
// starts with '?') - so "??e" can never be legal, for any e, which
// makes "?e = val" always illegal too. Nothing is lost: assigning
// through a thunk you already hold is exactly what the surviving '!'
// alternative is for ("!p = 3").
//
// A parenthesized/bracketed group is a destructuring target-list
// (Python-compatible: "(a, b) = 1, 2" means exactly "a, b = 1, 2" -
// parens are just grouping), never "the address of the tuple
// value" - UNLESS the ')'/']' is immediately followed by more
// application-chain material (another basic_expr, or an ARROWID, with
// no separator), meaning the parenthesized group was only ever the
// *head* of a longer application/indexing chain: "(!p)[x] = 1" indexes
// (!p) by x, it doesn't destructure (!p). A real ANTLR parser resolves
// this ambiguity for free via ordinary lookahead (it only accepts the
// destructuring reading when that lets the whole assign_target_list
// actually parse); a hand-written recursive-descent parser has to
// check for that trailing application material explicitly instead, and
// then validate the re-parsed whole as identifier-headed like any
// other application. A literal *empty* '()'/'[]' also falls through to
// 'application', where it's rejected too - there's nothing to
// destructure, and (unlike before) it no longer gets a pass as "just
// the empty-tuple/list value" either.
assign_target
    : OPEN_PAREN assign_target_list CLOSE_PAREN
    | OPEN_BRACK assign_target_list CLOSE_BRACK
    | '!' expr_rule
    | application
    ;
assign_target_list: assign_target (COMMA assign_target)* COMMA?;

expr_stmt: expr_rule;
assign_stmt: (assign_target_list assign_op)+ tuple_rule;
aug_assign_stmt: assign_target_list aug_assign_op tuple_rule;
const_assign_stmt: CONST bound EQ expr;
assert_stmt: ASSERT expr (COMMA expr)?;
await_stmt: AWAIT expr;
var_stmt: VAR bound EQ tuple_rule
        | VAR NAME (COMMA NAME)*;   // a bare 'var x' (or 'var x, y, ...')
                        // declares each name with no initial value, like
                        // 'global x, y'/'sequential x, y' - only a flat,
                        // parenthesis-free list of plain names may omit
                        // '= tuple_rule' this way; an actual destructuring
                        // bound ('var (x, y)', 'var [x, y]', or one nested
                        // inside an otherwise-flat list) still requires one
trap_stmt: TRAP expr;
return_stmt: RETURN expr;  // not a real Harmony statement - kept as its
                            // own production purely so a Python habit
                            // like "return 3" gets its own recognizable
                            // node and a specific error from the
                            // checker, instead of misparsing or being
                            // silently accepted as a meaningless
                            // expression statement.
pass_stmt: PASS;
break_stmt: BREAK;
continue_stmt: CONTINUE;
finally_stmt: FINALLY expr;
invariant_stmt: INVARIANT expr;  // Asserts an invariant that must hold
del_stmt: DEL expr;
spawn_stmt: SPAWN ETERNAL? expr;
go_stmt: GO expr (COMMA expr)?;  // second expr is the value STOP returns to this go; defaults to None
print_stmt: PRINT expr (COMMA expr)?;
sequential_stmt: SEQUENTIAL sequential_names_seq;
global_stmt: GLOBAL expr (COMMA expr)*;
builtin_stmt: BUILTIN NAME STRING;

sequential_names_seq: NAME (COMMA NAME)*;

// Block-able statements
for_block: iter_parse COLON block;

let_decl: LET bound assign_op tuple_rule NL?;
when_decl: WHEN (EXISTS bound IN expr | expr) NL?;
let_when_decl: (let_decl | when_decl) let_when_decl?;
let_when_block: let_when_decl COLON block;

opt_returns: RETURNS NAME;

method_decl: DEF NAME bound opt_returns? COLON block;
while_block: WHILE expr COLON block;
elif_block: ELIF expr COLON block;
else_block: ELSE COLON block;

if_block: IF expr COLON block elif_block* else_block?;

block_stmts: stmt+;

block
    : normal_block // Normal block
    | one_line_stmt // Single-line block stmt
;

normal_block:
    // handles the case of "dummy blocks"
    INDENT (block_stmts | INDENT block) DEDENT (SEMI_COLON NL)?
;

// Statements that do not introduce a new indentation block
simple_stmt
    : ATOMICALLY? (assign_stmt
    | const_assign_stmt
    | await_stmt
    | var_stmt
    | finally_stmt
    | invariant_stmt
    | del_stmt
    | spawn_stmt
    | trap_stmt
    | go_stmt
    | print_stmt
    | pass_stmt
    | break_stmt
    | continue_stmt
    | return_stmt
    | sequential_stmt
    | global_stmt
    | builtin_stmt
    | assert_stmt
    | aug_assign_stmt
    | expr_stmt
    );

// Statements that may introduce a new indentation block
compound_stmt
    : ATOMICALLY (COLON block
    | if_block
    | while_block
    | for_block
    | let_when_block
    | method_decl
    )
    | if_block
    | while_block
    | for_block
    | let_when_block
    | method_decl
    ;

one_line_stmt
    : simple_stmt (SEMI_COLON? NL | SEMI_COLON one_line_stmt);

label: (NAME COLON)+;
stmt: (((label? | COLON) (
          SEMI_COLON* NL
        | one_line_stmt
        | compound_stmt
        | import_stmt
    )) | ((label | COLON) normal_block)
);

COMMENT_START: '#';
OPEN_MULTI_COMMENT: '(*';
CLOSE_MULTI_COMMENT: '*)';

STAR     : '*';
AS       : 'as';
DOT      : '.';
IMPORT   : 'import';
PRINT    : 'print';
FROM     : 'from';
RANGE    : '..';
SETINTLEVEL : 'setintlevel';
SAVE     : 'save';
STOP     : 'stop';
LAMBDA   : 'lambda';
NOT      : 'not';
COMMA    : ',';
CONST    : 'const';
AWAIT    : 'await';
ASSERT   : 'assert';
VAR      : 'var';
TRAP     : 'trap';
PASS     : 'pass';
RETURN   : 'return';
BREAK    : 'break';
CONTINUE : 'continue';
DEL      : 'del';
SPAWN    : 'spawn';
FINALLY: 'finally';
INVARIANT: 'invariant';
GO     : 'go';
BUILTIN: 'builtin';
SEQUENTIAL: 'sequential';
WHEN    : 'when';
LET     : 'let';
IF      : 'if';
ELIF    : 'elif';
ELSE    : 'else';
AT      : '@';
WHILE   : 'while';
GLOBAL  : 'global';
DEF     : 'def';
RETURNS : 'returns';
EXISTS  : 'exists';
WHERE   : 'where';
EQ      : '=';
FOR     : 'for' {self.opened_for += 1};
IN      : 'in' {
if self.opened_for > 0:
    self.opened_for -= 1
};
COLON   : ':';
NONE    : 'None';
ATOMICALLY: 'atomically';
BOOL    : 'False' | 'True';
ETERNAL: 'eternal';

// STRING  : '"' .*? '"' | '\'' .*? '\'';
INT     : [0-9]+ | '0x' [0-9a-fA-F]+ | '0b' [01]+ | '0o' [0-7]+;
NAME    : [a-zA-Z_][a-zA-Z_0-9]*;
ATOM    : [.] (HEX_INTEGER | NAME);
ARROWID : '->' ' '* NAME;

HEX_INTEGER: '0X' HEX_DIGIT+;
/// hexdigit       ::=  digit | "a"..."f" | "A"..."F"
fragment HEX_DIGIT: [0-9a-fA-F];

OPEN_BRACK : '[' {self.opened += 1};
CLOSE_BRACK : ']' {self.opened -= 1};

OPEN_BRACES : '{' {self.opened += 1};
CLOSE_BRACES : '}' {self.opened -= 1};

OPEN_PAREN : '(' {self.opened += 1};
CLOSE_PAREN : ')' {self.opened -= 1};

SEMI_COLON: ';';

STRING
    : SHORT_STRING
    | LONG_STRING
    ;

/// shortstring     ::=  "'" shortstringitem* "'" | '"' shortstringitem* '"'
/// shortstringitem ::=  shortstringchar | stringescapeseq
/// shortstringchar ::=  <any source character except "\" or newline or the quote>
fragment SHORT_STRING
 : '\'' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f'] )* '\''
 | '"' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f"] )* '"'
 ;

/// longstring      ::=  "'''" longstringitem* "'''" | '"""' longstringitem* '"""'
fragment LONG_STRING
 : '\'\'\'' LONG_STRING_ITEM*? '\'\'\''
 | '"""' LONG_STRING_ITEM*? '"""'
 ;

/// longstringitem  ::=  longstringchar | stringescapeseq
fragment LONG_STRING_ITEM
 : LONG_STRING_CHAR
 | STRING_ESCAPE_SEQ
 ;

 /// longstringchar  ::=  <any source character except "\">
fragment LONG_STRING_CHAR
 : ~'\\'
 ;

/// stringescapeseq ::=  "\" <any source character>
fragment STRING_ESCAPE_SEQ
 : '\\' .
 | '\\' NL
 ;
