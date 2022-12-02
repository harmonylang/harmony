import sys
import os
import getopt
import traceback
import collections
import time
import math

nametypes = {}

def islower(c):
    return c in "abcdefghijklmnopqrstuvwxyz"

def isupper(c):
    return c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def isletter(c):
    return islower(c) or isupper(c)

def isnumeral(c):
    return c in "0123456789"

def isalnum(c):
    return isletter(c) or isnumeral(c)

def isnamechar(c):
    return isalnum(c) or c == "_"

def isnumber(s):
    return all(isnumeral(c) for c in s)

reserved = {
    "all",
    "and",
    "any",
    "as",
    "assert",
    "atLabel",
    "atomic",
    "atomically",
    "await",
    "bag",
    "choose",
    "const",
    "countLabel",
    "def",
    "del",
    "dict",
    "elif",
    "else",
    "end",
    "eternal",
    "exists",
    "from",
    "False",
    "for",
    "go",
    "hash",
    "if",
    "import",
    "in",
    "inf",
    "invariant",
    "keys",
    "lambda",
    "len",
    "let",
    "max",
    "min",
    "None",
    "not",
    "or",
    "pass",
    "print",
    "returns",
    "save",
    "select",
    "sequential",
    "setintlevel",
    "spawn",
    "stop",
    "str",
    "this",
    "trap",
    "True",
    "type",
    "var",
    "when",
    "where",
    "while"
}

def isname(s):
    return (not isreserved(s)) and (isletter(s[0]) or s[0] == "_") and \
                    all(isnamechar(c) for c in s)

def isunaryop(s):
    return s in [ "^", "-", "atLabel", "bagsize", "cardinality",
            "min", "max", "nametag", "not", "keys", "len", "processes" ]

def isbinaryop(s):
    return s in [
        "==", "!=", "..", "in", "and", "or",
        "-", "+", "*", "/", "%", "<", "<=", ">", ">="
    ];

tokens = [ "==", "!=", "<=", ">=", "..", "->", "[]" ]

def putchar(c, fd):
    print(c, end="", file=fd)

def capitalize(s):
    return "".join([ x[0].upper() + x[1:] for x in s.split("-")])

def nextLine(s, fd, pmap):
    while s != "":
        # skip over line comments
        if s.startswith("#"):
            s = s[1:]
            print("\\emph{\\#", end="", file=fd)
            while len(s) > 0 and s[0] != '\n':
                if s[0] in ["&", "%", "{", "}", "#", "^", "_"]:
                    print("\\" + s[0], end="", file=fd)
                elif s[0] in [ "<", ">", "-" ]:
                    print("$" + s[0] + "$", end="", file=fd)
                else:
                    putchar(s[0], fd)
                s = s[1:]
            print("}", end="", file=fd)
            continue

        # see if it's a multi-character token.  Match with the longest one
        found = ""
        for t in tokens:
            if s.startswith(t) and len(t) > len(found):
                found = t
        if found != "":
            if found in [ "<=", ">=" ]:
                print("$%s$"%found, end="", file=fd)
            elif found == "->":
                print("$\\rightarrow$", end="", file=fd)
            elif found == "[]":
                print("[\,]", end="", file=fd)
            else:
                print(found, end="", file=fd)
            s = s[len(found):]
            continue

        # see if a sequence of letters and numbers
        if isnamechar(s[0]):
            i = 0
            while i < len(s) and isnamechar(s[i]):
                i += 1
            found = s[:i]
            if found in reserved:
                nt = "reserved"
            elif isnumeral(found[0]):
                nt = "number"
            elif found in pmap:
                (nt, _) = pmap[found]
            else:
                nt = "var"
            found = found.replace("_", "\\_")
            print("\\hny%s{%s}"%(capitalize(nt),found), end="", file=fd)
            s = s[i:]
            continue

        # string
        if s[0] == '"':
            print('\\texttt{"}', end="", file=fd)
            i = 1
            while i < len(s) and s[i] != '"':
                if s[i] in ["&", "%", "{", "}", "#", "^", "_"]:
                    print("\\" + s[i], end="", file=fd)
                elif s[i] in [ "<", ">", "-" ]:
                    print("$" + s[i] + "$", end="", file=fd)
                else:
                    putchar(s[i], fd)
                i += 1
            if i < len(s):
                i += 1
            print('\\texttt{"}', end="", file=fd)
            s = s[i:]
            continue

        if s[0] in ["&", "%", "{", "}"]:
            print("\\" + s[0], end="", file=fd)
        elif s[0] == "~":
            print("\\string~", end="", file=fd)
        elif s[0] == "^":
            print("\\^{}", end="", file=fd)
        elif s[0] == "|":
            print("$\\vert$", end="", file=fd)
        else:
            if s[0] == "-":
                print("--", end="", file=fd)
            elif s[0] in [ "<", ">" ]:
                print("$" + s[0] + "$", end="", file=fd)
            else:
                putchar(s[0], fd)
        s = s[1:]

def lexer(s, file, fd, pmap):
    line = 1
    column = 1
    while s != "":
        if column == 1:
            if line != 1: print("\\\\\n", file=fd)
            print("\\>\\hnyLine{%d}\\>"%line, end="", file=fd)

        # see if it's a blank
        if s[0] in { " ", "\t" }:
            s = s[1:]
            column += 1
            putchar("~", fd)
            continue

        # skip over nested comments
        if s.startswith("(*"):
            count = 1
            s = s[2:]
            column += 2
            while count != 0 and s != "":
                if s.startswith("(*"):
                    count += 1
                    s = s[2:]
                    column += 2
                elif s.startswith("*)"):
                    count -= 1
                    s = s[2:]
                    column += 2
                elif s[0] == "\n":
                    s = s[1:]
                    line += 1
                    column = 1
                else:
                    s = s[1:]
                    column += 1
            continue

        # Find the end of the line, if any
        i = s.find("\n")
        if i < 0:
            nextLine(s, fd, pmap)
            s = ""
        else:
            nextLine(s[:i], fd, pmap)
            s = s[i+1:]
            line += 1
            column = 1

# TODO.  Can this be done efficiently in Python with just read()?
def loadAll(filename):
    all = ""
    with open(filename) as fd:
        for line in fd:
            all += line
    return all

def doProcess(filename, fd, pmap):
    all = loadAll(filename)
    print("% \\documentclass{article}", file=fd)
    print("% \\begin{document}", file=fd)
    print("\\providecommand{\\hnyLine}[1]{{\\tiny #1}\\'}", file=fd)
    print("\\providecommand{\\hnyReserved}[1]{\\textbf{#1}}", file=fd)
    print("\\providecommand{\\hnyModule}[1]{\\texttt{#1}}", file=fd)
    print("\\providecommand{\\hnyConstant}[1]{\\texttt{#1}}", file=fd)
    print("\\providecommand{\\hnyGlobal}[1]{\\textit{#1}}", file=fd)
    print("\\providecommand{\\hnyLocalConst}[1]{\\textit{#1}}", file=fd)
    print("\\providecommand{\\hnyLocalVar}[1]{\\textit{#1}}", file=fd)
    print("\\providecommand{\\hnyNumber}[1]{#1}", file=fd)
    print("\\begin{tabbing}", file=fd)
    print("X\\=XX\\=XXX\\kill", file=fd)
    lexer(all, filename, fd, pmap)
    print("\\end{tabbing}", file=fd)
    print("% \\end{document}", file=fd)

def tex_main(f, code, scope):
    doProcess(scope.file, f, scope.pmap)
