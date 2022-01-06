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

def isprint(c):
    return isinstance(c, str) and len(c) == 1 and (
        isalnum(c) or c in " ~`!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?")

def isnumber(s):
    return all(isnumeral(c) for c in s)

def allcaps(s):
    return all(isupper(c) or isnumeral(c) or c == '_' for c in s)

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
    "get_context",
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
    "select",
    "sequential",
    "setintlevel",
    "spawn",
    "stop",
    "str",
    "this",
    "trap",
    "True",
    "var",
    "when",
    "where",
    "while"
}

constants = {
    "False",
    "True",
    "None",
    "inf",
    "synch",
    "synchS",
    "barrier",
    "queue",
    "list",
    "bag",
    "alloc",
    "Lock",
    "acquire",
    "release",
    "wait",
    "notify",
    "notifyAll",
    "signal",
    "P",
    "V",
    "malloc",
    "free",
    "Queue",
    "put",
    "get"
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

def putchar(c):
    print(c, end="")

def nextLine(s):
    while s != "":
        # skip over line comments
        if s.startswith("#"):
            s = s[1:]
            print("\\emph{\\#", end="")
            while len(s) > 0 and s[0] != '\n':
                if s[0] in ["&", "%", "{", "}", "#", "^", "_"]:
                    print("\\" + s[0], end="")
                elif s[0] in [ "<", ">", "-" ]:
                    print("$" + s[0] + "$", end="")
                else:
                    putchar(s[0])
                s = s[1:]
            print("}", end="")
            continue

        # see if it's a multi-character token.  Match with the longest one
        found = ""
        for t in tokens:
            if s.startswith(t) and len(t) > len(found):
                found = t
        if found != "":
            if found in [ "<=", ">=" ]:
                print("$%s$"%found, end="")
            elif found == "->":
                print("$\\rightarrow$", end="")
            elif found == "[]":
                print("[\,]", end="")
            else:
                print(found, end="")
            s = s[len(found):]
            continue

        # see if a sequence of letters and numbers
        if isnamechar(s[0]):
            i = 0
            while i < len(s) and isnamechar(s[i]):
                i += 1
            found = s[:i]
            if found in nametypes:
                nt = nametypes[found]
            elif isnumeral(found[0]):
                nt = "number"
            elif allcaps(found):
                nt = "const"
            else:
                nt = "var"
            found = found.replace("_", "\\_")
            if nt == "number":
                print(found, end="")
            elif nt == "var":
                print("\\textit{%s}"%found, end="")
            elif nt == "reserved":
                print("\\textbf{%s}"%found, end="")
            elif nt in { "const", "module" }:
                print("\\texttt{%s}"%found, end="")
            else:
                assert False, (found, nt)
            s = s[i:]
            continue

        # string
        if s[0] == '"':
            print('\\texttt{"}', end="")
            i = 1
            str = '"'
            while i < len(s) and s[i] != '"':
                putchar(s[i])
                if s[i] == '\\':
                    i += 1
                    if i == len(s):
                        break
                    if s[i] == '"':
                        str += '"'
                    elif s[i] == '\\':
                        str += '\\'
                    elif s[i] == 't':
                        str += '\t'
                    elif s[i] == 'n':
                        str += '\n'
                    elif s[i] == 'f':
                        str += '\f'
                    elif s[i] == 'r':
                        str += '\r'
                    else:
                        str += s[i]
                else:
                    str += s[i]
                i += 1
            if i < len(s):
                i += 1
            str += '"'
            print('\\texttt{"}', end="")
            s = s[i:]
            continue

        if s[0] in ["&", "%", "{", "}"]:
            print("\\" + s[0], end="")
        elif s[0] == "~":
            print("\\string~", end="")
        elif s[0] == "^":
            print("\\^{}", end="")
        elif s[0] == "|":
            print("$\\vert$", end="")
        else:
            if s[0] == "-":
                print("--", end="")
            elif s[0] in [ "<", ">" ]:
                print("$" + s[0] + "$", end="")
            else:
                putchar(s[0])
        s = s[1:]

def lexer(s, file):
    line = 1
    column = 1
    while s != "":
        if column == 1:
            if line != 1: print("\\\\\n")
            print("\>{\\tiny %d}\\'\\>"%line, end="")

        # see if it's a blank
        if s[0] in { " ", "\t" }:
            s = s[1:]
            column += 1
            putchar("~")
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
            nextLine(s)
            s = ""
        else:
            nextLine(s[:i])
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

def doInline(s, filename):
    print("\\begin{tabbing}")
    print("X\\=XX\\=XXX\\kill")
    lexer(s, filename)
    print("\\end{tabbing}")

def doInput(filename):
    doInline(loadAll(filename), filename)

def parse(s, filename):
    if s == "":
        return
    if s[0] == ":":
        s = s[1:]
        i = s.index(":")
        key = s[:i].strip()
        value = s[i+1:].strip()
        if key == "input":
            doInput(value)
        elif key in { "const", "var", "module" }:
            nametypes[value] = key
        else:
            assert False, key
    else:
        nextLine(s)

def doProcess(filename):
    all = loadAll(filename)
    while True:
        i = all.find("<{")
        if i < 0:
            print(all, end="")
            break
        print(all[:i], end="")
        all = all[i+2:]
        j = all.index("}>")
        cmd = all[:j]
        all = all[j+2:]
        if cmd == ":inline:":
            if all[0] == "\n":
                all = all[1:]
            end = all.index("<{:end:}>")
            doInline(all[:end], filename)
            all = all[end+9:]
        else:
            parse(cmd, filename)

def main():
    for k in reserved:
        nametypes[k] = "reserved"
    for k in constants:
        nametypes[k] = "const"
    for f in sys.argv[1:]:
        doProcess(f)

if __name__ == "__main__":
    main()
