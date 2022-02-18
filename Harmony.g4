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

arith_op
    : 'and'
    | 'or'
    | '=>'
    | '&'
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

comp_op
    : '=='
    | '!='
    | '<'
    | '<='
    | '>'
    | '>='
    ;

unary_op
    : '-'
    | '~'
    | 'not'
    | 'abs'
    | 'atLabel'
    | 'countLabel'
    | 'get_context'
    | 'contexts'
    | 'isEmpty'
    | 'min'
    | 'max'
    | 'len'
    | 'str'
    | 'any'
    | 'all'
    | 'keys'
    | 'hash'
    | 'choose'
    ;

basic_expr
    : INT                    #int
    | BOOL                   #bool
    | ATOM                   #atom
    | NAME                   #name
    | STRING                 #str
    | NONE                   #none
    | OPEN_BRACES set_rule? CLOSE_BRACES #set_rule_1
    | OPEN_PAREN tuple_rule? CLOSE_PAREN  #paren_tuple
    | OPEN_BRACK tuple_rule? CLOSE_BRACK  #bracket_tuple
    | ADDRESS_OF expr_rule        #address
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
    : for_parse (for_parse | where_parse)*
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
    : expr_rule (
          NOT? IN expr_rule
        | (comp_op expr_rule)*
        | IF nary_expr ELSE expr_rule
        | (arith_op expr_rule)*
    )
;

expr_rule
    : LAMBDA bound COLON nary_expr 'end'
    | SETINTLEVEL expr_rule
    | SAVE expr_rule
    | STOP expr_rule
    | POINTER_OF expr_rule
    | unary_op expr_rule
    | application
;

application
    : basic_expr
    | application ARROW NAME
    | application basic_expr
;

expr: nary_expr;

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
    ;

expr_stmt: tuple_rule;
assign_stmt: (tuple_rule EQ)+ tuple_rule;
aug_assign_stmt: tuple_rule aug_assign_op tuple_rule;
const_assign_stmt: CONST bound EQ expr;
assert_stmt: ASSERT expr (COMMA expr)?;
await_stmt: AWAIT expr;
var_stmt: VAR bound EQ tuple_rule;
trap_stmt: TRAP expr;
pass_stmt: PASS;
invariant_stmt: INVARIANT expr;  // Asserts an invariant that must hold
del_stmt: DEL expr;
spawn_stmt: SPAWN ETERNAL? expr;
go_stmt: GO expr expr;
print_stmt: PRINT expr;
sequential_stmt: SEQUENTIAL expr (COMMA expr)*;

// Block-able statements
atomic_block: ATOMICALLY COLON block;
for_block: iter_parse COLON block;

let_decl: LET bound EQ tuple_rule NL?;
when_decl: WHEN (EXISTS bound IN expr | expr) NL?;
let_when_decl: (let_decl | when_decl) let_when_decl?;
let_when_block: let_when_decl COLON block;

method_decl: DEF NAME bound COLON block;
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
    | invariant_stmt
    | del_stmt
    | spawn_stmt
    | trap_stmt
    | go_stmt
    | print_stmt
    | pass_stmt
    | sequential_stmt
    | assert_stmt
    | aug_assign_stmt
    | expr_stmt
    );

// Statements that may introduce a new indentation block
compound_stmt
    : ATOMICALLY? (if_block
    | while_block
    | for_block
    | let_when_block
    | atomic_block
    | method_decl
    );

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

POINTER_OF: '!';
STAR     : '*';
AS       : 'as';
DOT      : '.';
IMPORT   : 'import';
PRINT    : 'print';
FROM     : 'from';
RANGE    : '..';
SETINTLEVEL : 'setintlevel';
ARROW    : '->';
SAVE     : 'save';
STOP     : 'stop';
LAMBDA   : 'lambda';
ADDRESS_OF : '?';
NOT      : 'not';
COMMA    : ',';
CONST    : 'const';
AWAIT    : 'await';
ASSERT   : 'assert';
VAR     : 'var';
TRAP   : 'trap';
POSSIBLY: 'possibly';
PASS     : 'pass';
DEL      : 'del';
SPAWN    : 'spawn';
INVARIANT: 'invariant';
GO     : 'go';
SEQUENTIAL: 'sequential';
WHEN    : 'when';
LET     : 'let';
IF      : 'if';
ELIF    : 'elif';
ELSE    : 'else';
AT      : '@';
WHILE   : 'while';
DEF     : 'def';
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
INT     : [0-9]+ | 'inf';
NAME    : [a-zA-Z_][a-zA-Z_0-9]*;
ATOM    : [.] (HEX_INTEGER | NAME);

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
