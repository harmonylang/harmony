import sys
import os
import getopt
import traceback
import collections
import time
import math

# TODO.  This should not be global ideally
files = {}              # files that have been read already
modules = {}            # modules modified with -m
namestack = []          # stack of module names being compiled
node_uid = 1            # unique node identifier

def load(f, filename, silent):
    if filename in files:
        return
    namestack.append(filename)
    files[filename] = []
    all = ""
    for line in f:
        files[filename] += [line]
        all += line
    tokens = lexer(all, filename, silent)
    namestack.pop()

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

def isreserved(s):
    return s in [
        "and",
        "assert",
        "atLabel",
        "atomic",
        "bagsize",
        "call",
        "cardinality",
        "choose",
        "const",
        "def",
        "del",
        "dict",
        "else",
        "fun",
        "for",
        "go",
        "if",
        "import",
        "in",
        "keys",
        "len",
        "let",
        "max",
        "min",
        "nametag",
        "not",
        "or",
        "pass",
        "spawn",
        "stop",
        "while"
    ]

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

tokens = [ "==", "!=", "<=", ">=", ".." ]

def putchar(c):
    print(c, end="")

constants = { "False", "True", "None", "inf",
    "lock", "unlock", "wait", "notify", "notifyAll", "signal", "P", "V" }

def doimport(module, file):
    for dir in [ os.path.dirname(file), "../../modules", "." ]:
        filename = dir + "/" + module + ".hny"
        if os.path.exists(filename):
            with open(filename) as f:
                load(f, filename, True)

def lexer(s, file, silent):
    result = []
    line = 1
    column = 1
    nextconst = False;
    nextimport = False;
    while s != "":
        if column == 1:
            if line != 1 and not silent: print("\\\\\n")
            if not silent: print("\>{\\tiny %d}\\'\\>"%line, end="")

        # see if it's a blank
        if s[0] in { " ", "\t" }:
            s = s[1:]
            column += 1
            if not silent: putchar("~")
            continue

        if s[0] == "\n":
            s = s[1:]
            line += 1
            column = 1
            continue

        # skip over line comments
        if s.startswith("#"):
            s = s[1:]
            if not silent: print("\\emph{\\#", end="")
            while len(s) > 0 and s[0] != '\n':
                column += 1
                if not silent:
                    if s[0] in ["&", "%", "{", "}", "#", "^", "_"]:
                        print("\\" + s[0], end="")
                    elif s[0] in [ "<", ">" ]:
                        print("$" + s[0] + "$", end="")
                    else:
                        putchar(s[0])
                s = s[1:]
            if not silent: print("}", end="")
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

        # see if it's a multi-character token.  Match with the longest one
        found = ""
        for t in tokens:
            if s.startswith(t) and len(t) > len(found):
                found = t
        if found != "":
            result += [ (found, file, line, column) ]
            if not silent:
                if found in [ "<=", ">=" ]:
                    print("$%s$"%found, end="")
                else:
                    print(found, end="")
            s = s[len(found):]
            column += len(found)
            continue

        # see if a sequence of letters and numbers
        if isnamechar(s[0]):
            i = 0
            while i < len(s) and isnamechar(s[i]):
                i += 1
            found = s[:i].replace("_", "\\_")
            if isreserved(found):
                if not silent: print("\\texttt{\\textbf{%s}}"%found, end="")
                if found in [ "def", "const", "import" ]:
                    nextconst = True
                    if found == "import":
                        nextimport = True
            elif isletter(found[0]):
                if nextconst:
                    constants.add(found)
                    if nextimport:
                        doimport(found, file)
                    if not silent: print("%s"%found, end="")
                elif found in constants:
                    if not silent: print("%s"%found, end="")
                else:
                    if not silent: print("\\textit{%s}"%found, end="")
            else:
                if not silent: print("%s"%found, end="")
            result += [ (s[:i], file, line, column) ]
            s = s[i:]
            column += i
            continue

        # string
        if s[0] == '"':
            if not silent: print("````", end="")
            i = 1
            str = '"'
            while i < len(s) and s[i] != '"':
                if not silent: putchar(s[i])
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
            if not silent: print("''''", end="")
            result += [ (str, file, line, column) ]
            s = s[i:]
            column += i
            continue

        # everything else is a single character token
        result += [ (s[0], file, line, column) ]
        nextconst = False
        nextimport = False

        if s[0] in ["&", "%", "{", "}"]:
            if not silent: print("\\" + s[0], end="")
        elif s[0] == "^":
            if not silent: print("\\^{}", end="")
        else:
            if s[0] in ["@", "."]:
                nextconst = True
            if not silent:
                if s[0] == "-":
                    print("--", end="")
                elif s[0] in [ "<", ">" ]:
                    print("$" + s[0] + "$", end="")
                else:
                    putchar(s[0])
        s = s[1:]
        column += 1
    return result

def doCompile(filenames):
    if filenames == []:
        print("Loading code from standard input...")
        load(sys.stdin, "<stdin>")
    else:
        for fname in filenames:
            with open(fname) as fd:
                load(fd, fname, False)

def usage():
    print("Usage: harmony [options] [harmony-file...]")
    print("  options: ")
    print("    -a: list machine code")
    print("    -b: blocking execution")
    print("    -c name=value: define a constant")
    print("    -h: help")
    print("    -m module=version: select a module version")
    print("    -s: list all states")
    exit(1)

def main():
    # Get options.  First set default values
    consts = []
    mods = []
    printCode = False
    blockflag = False
    printStates = False
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                        "abc:hm:s", ["const=", "help", "module="])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    for o, a in opts:
        if o == "-a":
            printCode = True
        elif o == "-b":
            blockflag = True
        elif o in { "-c", "--const" }:
            consts.append(a)
        elif o in { "-m", "--module" }:
            mods.append(a)
        elif o in { "-h", "--help" }:
            usage()
        elif o  == "-s":
            printStates = True
        else:
            assert False, "unhandled option"

    doCompile(args)

if __name__ == "__main__":
    main()
