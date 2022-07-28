# Grammar Parser

This documentation details the design and implementation of the Harmony programming language parser.

- [Grammar Parser](#grammar-parser)
  - [Modifying Harmony.g4](#modifying-harmonyg4)
    - [Expressions](#expressions)
    - [Statements](#statements)
    - [Embedded Python Code in `Harmony.g4`](#embedded-python-code-in-harmonyg4)
  - [Modifying `custom_denter.py`](#modifying-custom_denterpy)

## Modifying Harmony.g4

The `Harmony.g4` defines the grammar rules (statements and expressions) for the Harmony programming
language written using `ANTLR 4.9.3`.

> **NOTE**: The version of the Python3 antlr4 runtime must match
the parser generator version exactly. That is, if the ANTLR parser generator version is change 
to `ANTLR x.y.z`, then the `antlr4-python3-runtime==x.y.z` pip package has to be set as the
compiler's dependency.

If the `Harmony.g4` is modified, then run `make parser` to generate the updated `HarmonyLexer.py`,
`HarmonyParser.py`, and `HarmonyVisitor.py` files. **Any changes to `HarmonyVisitor.py`, such as new/deleted/modified method headers must be reflected in the HarmonyVisitor implementation `antlr_rule_visitor.py`**.

### Expressions

### Statements

### Embedded Python Code in `Harmony.g4`

## Modifying `custom_denter.py`

The `ModifiedDenterHelper` class implemented in this file extends the `DenterHelper` class of the
`antlr-denter` dependency and overrides the internal behavior. The main behavior of interest is handling
expressions that are broken into separate lines. Without modification, the default `DenterHelper` class would create `INDENT` and `DEDENT` tokens in between expression tokens, which would be difficult to parse using ANTLR 4. The extended implementation adds a check when the current token is a new indent while the previous observed token is an operator, such as `+` or `/`, which would be followed by another expression. If that's the case, then the observed `INDENT` (and the `DEDENT` token that would have also been output) is ignored.

