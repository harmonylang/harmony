# Grammar Parser

This documentation details the design and implementation of the Harmony programming language parser.

- [Grammar Parser](#grammar-parser)
  - [Requirements](#requirements)
  - [Generating the Lexer and Parser](#generating-the-lexer-and-parser)
  - [Modifying Harmony.g4](#modifying-harmonyg4)
    - [Statements](#statements)
  - [Modifying `custom_denter.py`](#modifying-custom_denterpy)
  - [Modifying `HarmonyErrorListener.py`](#modifying-harmonyerrorlistenerpy)
  - [Using the Lexer and Parser](#using-the-lexer-and-parser)

## Requirements

To use the `antlr` parser generator, the `Java` runtime must be installed. The committed `antlr-x.y.z-complete.jar` file can then be run to generate the lexer and parser files.

## Generating the Lexer and Parser
The lexer and parser are generated in the `harmony_model_checker/parser` directory by running `make parser`. This creates `HarmonyLexer.py`, `HarmonyParser.py`, and `HarmonyVisitor.py`, which are to be committed for convenience.

## Modifying Harmony.g4

The `Harmony.g4` defines the grammar rules (statements and expressions) for the Harmony programming language written using `ANTLR 4.9.3`.

> **NOTE**: The version of the Python3 antlr4 runtime must match
the parser generator version exactly. That is, if the ANTLR parser generator version is change 
to `ANTLR x.y.z`, then the `antlr4-python3-runtime==x.y.z` pip package has to be set as the
compiler's dependency.

If the `Harmony.g4` is modified, then run `make parser` to generate the updated `HarmonyLexer.py`,
`HarmonyParser.py`, and `HarmonyVisitor.py` files. **Any changes to `HarmonyVisitor.py`, such as new/deleted/modified method headers must be reflected in the HarmonyVisitor implementation `antlr_rule_visitor.py`**.

### Statements

The grammar file defines the `Harmony` language as a sequence of statements, where statements is one of an 1) import statment, 2) a compound statement, or 3) a simple statement. Each statement can optionally begin with a label name followed by a colon. Alternatively, a block of indented statements can follow a label/colon.

## Modifying `custom_denter.py`
The grammar file contains embedded `Python` code that modifies the generated lexer's indentation behavior implemented by `cutom_denter.py`.

The `ModifiedDenterHelper` class implemented in this file extends the `DenterHelper` class of the
`antlr-denter` dependency and overrides the internal behavior. The main behavior of interest is handling
expressions that are broken into separate lines. Without modification, the default `DenterHelper` class would create `INDENT` and `DEDENT` tokens in between expression tokens, which would be difficult to parse using ANTLR 4. The extended implementation adds a check when the current token is a new indent while the previous observed token is an operator, such as `+` or `/`, which would be followed by another expression. If that's the case, then the observed `INDENT` (and the `DEDENT` token that would have also been output) is ignored.

## Modifying `HarmonyErrorListener.py`

This file implements an error handler for syntax errors encountered in the lexer or the parser. The classes override antlr's `ErrorListner` class and its `syntaxError` method. Some of the error messages that are created by `antlr` are replaced by custom error messages that are more suitable and convenient for us.

## Using the Lexer and Parser

In `harmony_model_checker/compile.py`, the lexer and parser are created for us in the `_build_parser` function.

Of note is the `_build_input_stream` function, which takes either a `filename` or `str_value` key argument. If `filename` is given, then it creates a `FileStream` to handle `utf-8`-encoded files (by default, the antlr lexer handles only files that contain ascii). Otherwise if `str_value` is given, then it creates an `InputStream` such that the string is treated as the content of a Harmony program. `FileStream` and `InputStream` are classes provided by the `antlr4` library.
