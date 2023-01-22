"""
	This is the Harmony compiler.

    Copyright (C) 2020, 2021, 2022  Robbert van Renesse

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:

    1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

    2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

    3. Neither the name of the copyright holder nor the names of its
    contributors may be used to endorse or promote products derived
    from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
"""

import collections
import getopt
import html
import pathlib
import sys
import os
import math
import functools
import json
import time
import traceback
import webbrowser

from harmony_model_checker.harmony.tex import *
from harmony_model_checker.harmony.jsonstring import *
from harmony_model_checker.harmony.brief import *
from harmony_model_checker.harmony.genhtml import *
from harmony_model_checker.harmony.behavior import *
from harmony_model_checker.harmony.value import *
from harmony_model_checker.harmony.ast import *
from harmony_model_checker.harmony.code import *
from harmony_model_checker.harmony.scope import *
from harmony_model_checker.harmony.state import *
from harmony_model_checker.harmony.ops import *
from harmony_model_checker.harmony.bag_util import *
from harmony_model_checker.exception import HarmonyCompilerError
from harmony_model_checker import __version__


# TODO.  These should not be global ideally
files = {}              # files that have been read already
modules = {}            # modules modified with -m
# used_modules = set()  # modules modified and used
namestack = []          # stack of module names being compiled
node_uid = 1            # unique node identifier
silent = False          # not printing periodic status updates
lasttime = 0            # last time status update was printed


class Node:
    def __init__(self, state, uid, parent, before, after, steps, len):
        self.state = state      # State associated with this node
        self.uid = uid          # index into 'nodes' array
        self.parent = parent    # next hop on way to initial state
        self.len = len          # length of path to initial state
        self.before = before    # the context that made the hop from the parent state
        self.after = after      # the resulting context
        self.steps = steps      # list of microsteps

        # if state.choosing, maps choice, else context
        self.edges = {}         # map to <nextNode, nextContext, steps>

        self.sources = set()    # backward edges
        self.expanded = False   # lazy deletion
        self.issues = set()     # set of problems with this state
        self.cid = 0            # strongly connected component id
        self.blocked = {}       # map of context -> boolean

    def __hash__(self):
        return self.uid

    def __eq__(self, other):
        return isinstance(other, Node) and other.uid == self.uid

    def rec_isblocked(self, ctx, vars, seen):
        if self.uid in seen:
            return True
        seen.add(self.uid)
        if ctx in self.blocked:
            return self.blocked[ctx]
        s = self.state
        if s.choosing == ctx:
            for (choice, next) in self.edges.items():
                (nn, nc, steps) = next
                ns = nn.state
                if ns.vars != vars or not nn.rec_isblocked(nc, vars, seen):
                    self.blocked[ctx] = False
                    return False
        elif ctx in self.edges:
            next = self.edges[ctx]
            (nn, nc, steps) = next
            ns = nn.state
            if ns.vars != vars or not nn.rec_isblocked(nc, vars, seen):
                self.blocked[ctx] = False
                return False
        else:
            self.blocked[ctx] = False
            return False
        self.blocked[ctx] = True
        return True

    # See if the given process is "blocked", i.e., it cannot change
    # the shared state (the state variables), terminate, or stop unless
    # some other process changes the shared state first
    def isblocked(self, ctx):
        return self.rec_isblocked(ctx, self.state.vars, set())

def strsteps(steps):
    if steps == None:
        return "[]"
    result = ""
    i = 0
    while i < len(steps):
        if result != "":
            result += ","
        (pc, choice) = steps[i]
        if pc == None:
            result += "Interrupt"
        else:
            result += str(pc)
        j = i + 1
        if choice != None:
            result += "(choose %s)"%strValue(choice)
        else:
            while j < len(steps):
                (pc2, choice2) = steps[j]
                if pc == None or pc2 != pc + 1 or choice2 != None:
                    break
                (pc, choice) = (pc2, choice2)
                j += 1
            if j > i + 1:
                result += "-%d"%pc
        i = j
    return "[" + result + "]"

def find_shortest(bad):
    best_node = None
    best_len = 0
    for node in bad:
        if best_node == None or node.len < best_len:
            best_node = node
            best_len = node.len
    return best_node

def varvisit(d, vars, name, r):
    if isinstance(d, dict):
        for k in sorted(d.keys()):
            if isinstance(k, str):
                nn = name + "." + k
            else:
                nn = name + "[" + strValue(k) + "]"
            if k in vars.d:
                varvisit(d[k], vars.d[k], nn, r)
            else:
                r.append("%s: ---"%nn)
    else:
        r.append("%s: %s"%(name, strValue(vars)))

def strvars(d, vars):
    r = []
    for k in sorted(d.keys()):
        varvisit(d[k], vars.d[k], k, r)
    return "{ " + ", ".join(r) + " }"

def varmerge(d, vars):
    assert isinstance(d, dict)
    assert isinstance(vars, DictValue)
    for (k, v) in vars.d.items():
        if k in d and isinstance(d[k], dict) and isinstance(v, DictValue):
            varmerge(d[k], v)
        elif k not in d and isinstance(v, DictValue):
            d[k] = {}
            varmerge(d[k], v)
        elif k not in d:
            d[k] = {v}
        elif isinstance(d[k], set):
            d[k] |= {v}
        else:
            assert isinstance(d[k], dict)
            d[k] = { v }

def vartrim(d):
    pairs = list(d.items())
    for (k, v) in pairs:
        if v == {}:
            del d[k]
        elif isinstance(d[k], dict):
            vartrim(d[k])

def pathvars(path):
    d = {}
    for (fctx, ctx, steps, states, vars) in path:
        varmerge(d, vars)
    vartrim(d)
    return d

def print_path(bad_node):
    path = genpath(bad_node)
    d = pathvars(path)
    pids = []
    for (fctx, ctx, steps, states, vars) in path:
        try:
            pid = pids.index(fctx)
            pids[pid] = ctx
        except ValueError:
            pids.append(ctx)
            pid = len(pids) - 1
        print("T%d:"%pid, ctx.nametag(), strsteps(steps), ctx.pc, strvars(d, vars))
    if len(path) > 0:
        (fctx, ctx, steps, states, vars) = path[-1]
        if ctx.failure != None:
            print(">>>", ctx.failure)

def optjump(code, pc):
    while pc < len(code.labeled_ops):
        op = code.labeled_ops[pc].op
        if not isinstance(op, JumpOp):
            break
        pc = op.pc
    return pc

# Jump chaining
def optimize(code):
    for i in range(len(code.labeled_ops)):
        op = code.labeled_ops[i].op
        if isinstance(op, JumpOp):
            code.labeled_ops[i].op = JumpOp(optjump(code, op.pc), reason=op.reason)
        elif isinstance(op, JumpCondOp):
            code.labeled_ops[i].op = JumpCondOp(op.cond, optjump(code, op.pc), reason=op.reason)

def invcheck(state, inv):
    assert isinstance(state.code[inv], InvariantOp)
    op = state.code[inv]
    ctx = ContextValue(("__invariant__", None, None, None), 0, emptytuple, emptydict)
    ctx.atomic = ctx.readonly = 1
    ctx.pc = inv + 1
    while ctx.pc != inv + op.cnt:
        old = ctx.pc
        state.code[ctx.pc].eval(state, ctx)
        assert ctx.pc != old, old
    assert len(ctx.stack) == 1
    assert isinstance(ctx.stack[0], bool)
    return ctx.stack[0]

class Pad:
    def __init__(self, descr):
        self.descr = descr
        self.value = ""
        self.lastlen = 0
    
    def __repr__(self):
        return self.descr + " = " + self.value

    def pad(self, v):
        if len(v) < len(self.value):
            self.value = " " * (len(self.value) - len(v))
        else:
            self.value = ""
        self.value += v

p_ctx = Pad("ctx")
p_pc  = Pad("pc")
p_ns  = Pad("#states")
p_dia = Pad("diameter")
p_ql  = Pad("#queue")

# Have context ctx make one (macro) step in the given state
def onestep(node, ctx, choice, interrupt, nodes, visited, todo):
    assert ctx.failure == None, ctx.failure

    # Keep track of whether this is the same context as the parent context
    samectx = ctx == node.after

    # Copy the state before modifying it
    sc = node.state.copy()   # sc is "state copy"
    sc.choosing = None

    # Make a copy of the context before modifying it (cc is "context copy")
    cc = ctx.copy()

    # Copy the choice as well
    choice_copy = choice

    steps = []

    if interrupt:
        assert not cc.interruptLevel
        (method, arg) = ctx.trap
        cc.push(PcValue(cc.pc))
        cc.push("interrupt")
        cc.push(arg)
        cc.pc = method.pc
        cc.trap = None
        cc.interruptLevel = True
        steps.append((None, None))      # indicates an interrupt

    localStates = set() # used to detect infinite loops
    loopcnt = 0         # only check for infinite loops after a while
    while cc.phase != "end":
        # execute one microstep
        steps.append((cc.pc, choice_copy))

        # print status update
        global lasttime, silent
        if not silent and time.time() - lasttime > 0.3:
            p_ctx.pad(cc.nametag())
            p_pc.pad(str(cc.pc))
            p_ns.pad(str(len(visited)))
            p_dia.pad(str(node.len))
            p_ql.pad(str(len(todo)))
            print(p_ctx, p_pc, p_ns, p_dia, p_ql, len(localStates), end="\r")
            lasttime = time.time()

        # If the current instruction is a "choose" instruction,
        # make the specified choice
        if isinstance(sc.code[cc.pc], ChooseOp):
            assert choice_copy != None
            cc.stack[-1] = choice_copy
            cc.pc += 1
            choice_copy = None
        else:
            assert choice_copy == None
            if type(sc.code[cc.pc]) in { LoadOp, StoreOp, AtomicIncOp }:
                assert cc.phase != "end"
                cc.phase = "middle"
            try:
                sc.code[cc.pc].eval(sc, cc)
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
                cc.failure = "Python assertion failed"

        if cc.failure != None or cc.stopped:
            break

        # See if this process is making a nondeterministic choice.
        # If so, we break out of the microstep loop.  However, only
        # this process is scheduled from this state.
        if isinstance(sc.code[cc.pc], ChooseOp):
            v = cc.stack[-1]
            if (not isinstance(v, SetValue)) or v.s == set():
                # TODO.  Need the location of the choose operation in the file
                cc.failure = "pc = " + str(cc.pc) + \
                    ": Error: choose can only be applied to non-empty sets"
                break

            # if there is only one choice, we can just keep on going
            if len(v.s) > 1:
                sc.choosing = cc
                break
            else:
                choice_copy = list(v.s)[0]

        # if we're about to access shared state, let other processes
        # go first assuming there are other processes and we're not
        # in "atomic" mode
        # TODO.  IS THIS CHECK RIGHT?
        if cc.phase != "start" and cc.atomic == 0 and type(sc.code[cc.pc]) in { LoadOp, StoreOp }: # TODO  and len(sc.ctxbag) > 1:
            break
        # TODO.  WHY NOT HAVE THE SAME CHECK HERE?
        if cc.phase != "start" and cc.atomic == 0 and type(sc.code[cc.pc]) in { AtomicIncOp }:
            break

        # ContinueOp always causes a break
        if isinstance(sc.code[cc.pc], ContinueOp):
            break

        # Detect infinite loops if there's a suspicion
        loopcnt += 1
        if loopcnt > 200:
            if (sc, cc) in localStates:
                cc.failure = "infinite loop"
                break
            localStates.add((sc.copy(), cc.copy()))

    # Remove original context from bag
    bag_remove(sc.ctxbag, ctx)

    # Put the resulting context into the bag unless it's done
    if cc.phase == "end":
        sc.initializing = False     # initializing ends when __init__ finishes
        bag_add(sc.termbag, cc)
    elif not cc.stopped:
        bag_add(sc.ctxbag, cc)

    length = node.len if samectx else (node.len + 1)
    next = visited.get(sc)
    if next == None:
        next = Node(sc, len(nodes), node, ctx, cc, steps, length)
        nodes.append(next)
        visited[sc] = next
        if samectx:
            todo.insert(0, next)
        else:
            todo.append(next)
    elif next.len > length:
        assert length == node.len and next.len == node.len + 1 and not next.expanded, (node.len, length, next.len, next.expanded)
        # assert not next.expanded, (node.len, length, next.len, next.expanded)
        next.len = length
        next.parent = node
        next.before = ctx
        next.after = cc
        next.steps = steps
        todo.insert(0, next)
    node.edges[choice if node.state.choosing else ctx] = (next, cc, steps)
    next.sources.add(node)
    if cc.failure != None:
        next.issues.add("Thread Failure")


def kosaraju1(nodes, stack):
    seen = set()
    for node in nodes:
        if node.uid in seen:
            continue
        seen.add(node.uid)
        S = [node]
        while S:
            u = S[-1]
            done = True
            for (nn, nc, steps) in u.edges.values():
                if nn.uid not in seen:
                    seen.add(nn.uid)
                    done = False
                    S.append(nn)
                    break
            if done:
                S.pop()
                stack.append(u)

def kosaraju2(nodes, node, seen, scc):
    stack2 = [node]
    while stack2 != []:
        node = stack2.pop()
        if node.uid in seen:
            continue
        seen.add(node.uid)
        node.cid = scc.cid
        scc.nodes.add(node)
        for nn in node.sources:
            if nn.uid not in seen:
                stack2.append(nn)

class SCC:
    def __init__(self, cid):
        self.cid = cid
        self.nodes = set()      # set of nodes in this component
        self.edges = set()      # edges to other components
        self.good = False

# Find strongly connected components using Kosaraju's algorithm
def find_scc(nodes):
    stack = []
    kosaraju1(nodes, stack)
    seen = set()
    components = []
    while stack != []:
        next = stack.pop()
        if next.uid not in seen:
            scc = SCC(len(components))
            components.append(scc)
            kosaraju2(nodes, next, seen, scc)
    return components

def run(code, labels, blockflag):
    state = State(code, labels)
    ctx = ContextValue(("__init__", None, None, None), 0, emptytuple, emptydict)
    ctx.atomic = 1
    ctx.push("process")
    ctx.push(emptytuple)
    bag_add(state.ctxbag, ctx)
    node = Node(state, 0, None, None, None, [], 0)

    nodes = [node]

    # For traversing Kripke graph
    visited = { state: node }
    todo = collections.deque([node])
    bad = set()

    faultyState = False
    maxdiameter = 0
    while todo:
        node = todo.popleft()

        # check the invariants
        if len(node.issues) == 0 and node.state.choosing == None:
            for inv in node.state.invariants:
                if not invcheck(node.state, inv):
                    (lexeme, file, line, column) = code[inv].token
                    node.issues.add("Invariant file=%s line=%d failed"%(file, line))

        if len(node.issues) > 0:
            bad.add(node)
            faultyState = True
            break

        if node.expanded:
            continue
        node.expanded = True
        if node.len > maxdiameter:
            maxdiameter = node.len

        if node.state.choosing != None:
            ctx = node.state.choosing
            assert ctx in node.state.ctxbag, ctx
            choices = ctx.stack[-1]
            assert isinstance(choices, SetValue), choices
            assert len(choices.s) > 0
            for choice in choices.s:
                onestep(node, ctx, choice, False, nodes, visited, todo)
        else:
            for (ctx, _) in node.state.ctxbag.items():
                onestep(node, ctx, None, False, nodes, visited, todo)
                if ctx.trap != None and not ctx.interruptLevel:
                    onestep(node, ctx, None, True, nodes, visited, todo)

    if not silent:
        print("#states =", len(visited), "diameter =", maxdiameter,
                                " "*100 + "\b"*100)

    todump = set()

    # See if there has been a safety violation
    issues_found = False
    if len(bad) > 0:
        print("==== Safety violation ====")
        bad_node = find_shortest(bad)
        print_path(bad_node)
        todump.add(bad_node)
        for issue in bad_node.issues:
            print(issue)
        issues_found = True

    if not faultyState:
        # Determine the strongly connected components
        components = find_scc(nodes)
        if not silent:
            print("#components:", len(components))

        # Figure out which strongly connected components are "good".
        # These are non-sink components or components that have
        # a terminated state.
        bad = set()
        for (s, n) in visited.items():
            if len(s.ctxbag) == 0 and len(s.stopbag) == 0:
                assert len(n.edges) == 0
                components[n.cid].good = True
                if blockflag:
                    bad.add(n)
                    n.issues.add("Terminating State")
            else:
                # assert len(n.edges) != 0, n.edges         TODO
                for (nn, nc, steps) in n.edges.values():
                    if nn.cid != n.cid:
                        components[n.cid].edges.add(nn.cid)
                    if nn.cid != n.cid:
                        components[n.cid].good = True
                        break

        nbadc = sum(not scc.good for scc in components)
        if nbadc != 0:
            if not blockflag:
                print("#bad components:", nbadc)
            for n in nodes:
                if components[n.cid].good:
                    continue
                if blockflag:
                    # see if all processes are blocked or stopped
                    s = n.state
                    for ctx in s.ctxbag.keys():
                        assert isinstance(ctx, ContextValue)
                        if not n.isblocked(ctx):
                            n.issues.add("Non-terminating State")
                            bad.add(n)
                            break
                else:
                    n.issues.add("Non-terminating State")
                    bad.add(n)

        if len(bad) > 0:
            bad_node = find_shortest(bad)
            issues = ""
            for issue in bad_node.issues:
                if issues != "":
                    issues += ", "
                issues += issue
            print("====", issues, "===")
            print_path(bad_node)
            todump.add(bad_node)
            issues_found = True

            # See which processes are blocked
            assert not bad_node.state.choosing
            running = 0
            blocked = 0
            stopped = 0
            for ctx in bad_node.state.ctxbag.keys():
                assert isinstance(ctx, ContextValue)
                if bad_node.isblocked(ctx):
                    blocked += 1
                    print("blocked process:", ctx.nametag(), "pc =", ctx.pc)
                else:
                    running += 1
                    print("running process:", ctx.nametag(), "pc =", ctx.pc)
            for ctx in bad_node.state.stopbag.keys():
                print("stopped process:", ctx.nametag(), "pc =", ctx.pc)
                stopped += 1
            print("#blocked:", blocked, "#stopped:", stopped, "#running:", running)

    if not issues_found:
        print("no issues found")
        n = None
    else:
        n = find_shortest(todump)
    return (nodes, n)

def htmlstrsteps(steps):
    if steps == None:
        return "[]"
    result = ""
    i = 0
    while i < len(steps):
        if result != "":
            result += " "
        (pc, choice) = steps[i]
        j = i + 1
        if pc == None:
            result += "Interrupt"
        else:
            result += "<a href='#P%d'>%d"%(pc, pc)
        if choice != None:
            result += "</a>(choose %s)"%strValue(choice)
        else:
            while j < len(steps):
                (pc2, choice2) = steps[j]
                if pc == None or pc2 != pc + 1 or choice2 != None:
                    break
                (pc, choice) = (pc2, choice2)
                j += 1
            if j > i + 1:
                result += "-%d"%pc
            result += "</a>"
        i = j
    return result

def genpath(n):
    # Extract the path to node n
    path = []
    while n != None:
        if n.after == None:
            break
        path = [n] + path
        n = n.parent

    # Now compress the path, combining macrosteps by the same context
    path2 = []
    lastctx = firstctx = None
    laststeps = []
    laststates = []
    lastvars = DictValue({})
    for n in path:
        if firstctx == None:
            firstctx = n.before
        if lastctx == None or lastctx == n.before:
            laststeps += n.steps
            lastctx = n.after
            laststates.append(n.uid)
            lastvars = n.state.vars
            continue
        path2.append((firstctx, lastctx, laststeps, laststates, lastvars))
        firstctx = n.before
        lastctx = n.after
        laststeps = n.steps.copy()
        laststates = [n.uid]
        lastvars = n.state.vars
    path2.append((firstctx, lastctx, laststeps, laststates, lastvars))
    return path2

def vardim(d):
    totalwidth = 0
    maxheight = 0
    if isinstance(d, dict):
        for k in sorted(d.keys()):
            (w, h) = vardim(d[k])
            totalwidth += w
            if h + 1 > maxheight:
                maxheight = h + 1
    else:
        return (1, 0)
    return (totalwidth, maxheight)

def varhdr(d, name, nrows, f):
    q = queue.Queue()
    level = 0
    q.put((d, level))
    while not q.empty():
        (nd, nl) = q.get()
        if nl > level:
            print("</tr><tr>", file=f)
            level = nl
        if isinstance(nd, dict):
            for k in sorted(nd.keys()):
                (w,h) = vardim(nd[k])
                if h == 0:
                    print("<td align='center' style='font-style: italic' colspan=%d rowspan=%d>%s</td>"%(w,nrows-nl,k), file=f)
                else:
                    print("<td align='center' style='font-style: italic' colspan=%d>%s</td>"%(w,k), file=f)
                q.put((nd[k], nl+1))

def vardump_rec(d, vars, f):
    if isinstance(d, dict):
        for k in sorted(d.keys()):
            if vars != None and k in vars.d:
                vardump_rec(d[k], vars.d[k], f)
            else:
                vardump_rec(d[k], None, f)
    elif vars == None:
        print("<td></td>", file=f)
    else:
        print("<td align='center'>%s</td>"%strValue(vars), file=f)

def vardump(d, vars, f):
    for k in sorted(d.keys()):
        vardump_rec(d[k], vars.d[k], f)

def htmlpath(n, color, f):
    # Generate a label for the path table
    issues = n.issues
    if len(issues) == 0:
        issues = { "no issues" }
    label = ""
    for issue in issues:
        if label != "":
            label += ", "
        label += issue
    label = "Issue: " + label
    # keys = sorted(n.state.vars.d.keys(), key=keyValue)
    path = genpath(n)
    d = pathvars(path)
    (width, height) = vardim(d)
    print("<table id='issuestbl' border='1' width='100%%'><tr><th colspan='2' align='left' style='color: %s'>%s</th><th></th>"%(color, html.escape(label)), file=f)
    if width == 1:
        print("<th>Shared Variable</th>", file=f)
    else:
        print("<th colspan='%d'>Shared Variables</th>"%width, file=f)
    print("<col style='width:15%'>", file=f)
    print("<tr><th rowspan=%d>Process</th><th rowspan=%d>Steps</th><th rowspan=%d></th>"%(height, height, height), file=f)
    varhdr(d, "", height, f)
    print("</tr><tr><td></td></tr>", file=f)
    row = height + 1
    pids = []
    for (fctx, ctx, steps, states, vars) in path:
        row += 1
        if len(states) > 0:
            sid = states[-1]
        else:
            sid = n.uid
        try:
            pid = pids.index(fctx)
            pids[pid] = ctx
        except ValueError:
            pids.append(ctx)
            pid = len(pids) - 1
        print("<tr><td>T%d: <a href='javascript:rowshow(%d,%d)'>%s</a></td>"%(pid, row, sid, ctx.nametag()), file=f)
        print("<td>%s</td><td></td>"%htmlstrsteps(steps), file=f)
        vardump(d, vars, f)
        print("</tr>", file=f)
    print("</table>", file=f)
    return height

def htmlloc(code, scope, ctx, traceid, f):
    pc = ctx.pc
    fp = ctx.fp
    print("<table id='loc%d' border='1' width='100%%'>"%traceid, file=f)
    trace = []
    while True:
        trace += [(pc, fp)]
        if fp < 5:
            break
        pc = ctx.stack[fp - 5]
        assert isinstance(pc, PcValue)
        pc = pc.pc
        fp = ctx.stack[fp - 1]
    trace.reverse()
    row = 0
    for (pc, fp) in trace:
        if row == 0:
            print("<tr style='background-color: #A5FF33'>", file=f)
        else:
            print("<tr>", file=f)
        print("<td>", file=f)
        print("<a href='#P%d'>%d</a> "%(pc, pc), file=f)
        print("<a href='javascript:setrow(%d,%d)'>"%(traceid,row), file=f)
        origpc = pc
        while pc >= 0 and pc not in scope.locations:
            pc -= 1
        if pc in scope.locations:
            (file, line) = scope.locations[pc]
        else:
            (file, line) = ("NOFILE", 0)
        # TODO.  Should skip over nested methods
        while pc >= 0 and not isinstance(code[pc], FrameOp):
            pc -= 1
        if fp >= 3:
            arg = ctx.stack[fp-3]
            if arg == emptytuple:
                print("%s()"%(code[pc].name[0]), end="", file=f)
            else:
                print("%s(%s)"%(code[pc].name[0], strValue(arg)), end="", file=f)
        print("</a>:", file=f)
        lines = files[file]
        if lines is not None and line <= len(lines):
            print(html.escape(lines[line - 1]), file=f)
        print("</td></tr>", file=f)
        row += 1

    if ctx.failure != None:
        print("<tr style='color: red'><td>%s</td></tr>"%ctx.failure, file=f)
    print("</table>", file=f)

def htmlvars(vars, id, row, f):
    assert(isinstance(vars, DictValue))
    display = "block" if row == 0 else "none"
    print("<div id='vars%d_%d' style='display:%s'>"%(traceid, row, display), file=f)
    if len(vars.d) > 0:
        print("<table>", file=f)
        for (key, value) in vars.d.items():
            print("<tr>", file=f)
            print("<td>%s = %s</td>"%(strValue(key)[1:], strValue(value)), file=f)
            print("</tr>", file=f)
        print("</table>", file=f)
    print("</div>", file=f)

# print the variables on the stack
def htmltrace(code, scope, ctx, traceid, f):
    pc = ctx.pc
    fp = ctx.fp
    trace = [ctx.vars]
    while True:
        if fp < 5:
            break
        trace.append(ctx.stack[fp - 2])
        fp = ctx.stack[fp - 1]
    trace.reverse()
    for i in range(len(trace)):
        htmlvars(trace[i], traceid, i, f)

traceid = 0

def htmlrow(ctx, bag, node, code, scope, f, verbose):
    global traceid
    traceid += 1

    print("<tr>", file=f)
    if bag[ctx] > 1:
        print("<td>%s [%d copies]</td>"%(ctx.nametag(), bag[ctx]), file=f)
    else:
        print("<td>%s</td>"%ctx.nametag(), file=f)
    if ctx.stopped:
        print("<td>stopped</td>", file=f)
    else:
        if node.state.choosing:
            print("<td>choosing</td>", file=f)
        else:
            if ctx in node.edges:
                if node.isblocked(ctx):
                    print("<td>blocked</td>", file=f)
                else:
                    print("<td>running</td>", file=f)
            else:
                print("<td>failed</td>", file=f)

    print("<td>", file=f)
    htmlloc(code, scope, ctx, traceid, f)
    print("</td>", file=f)

    # print variables
    print("<td>", file=f)
    htmltrace(code, scope, ctx, traceid, f)
    print("</td>", file=f)

    # print stack
    if verbose:
        print("<td>%d</td>"%ctx.fp, file=f)
        print("<td align='center'>", file=f)
        print("<table border='1'>", file=f)
        for v in ctx.stack:
            print("<tr><td align='center'>", file=f)
            if isinstance(v, PcValue):
                print("<a href='#P%d'>"%v.pc, file=f)
                print("%s"%strValue(v), file=f)
                print("</a>", file=f)
            else:
                print("%s"%strValue(v), file=f)
            print("</td></tr>", file=f)
        print("</table>", file=f)
        print("</td>", file=f)
        assert not s.choosing
        if ctx in n.edges:
            (nn, nc, steps) = n.edges[ctx]
            print("<td>%s</td>"%htmlstrsteps(steps), file=f)
            print("<td><a href='javascript:show(%d)'>"%nn.uid, file=f)
            print("%d</a></td>"%nn.uid, file=f)
        else:
            print("<td>no steps</td>", file=f)
            print("<td></td>", file=f)
    print("</tr>", file=f)

def htmlstate(f):
    print("<table border='1' width='90%'>", file=f)
    print("<col style='width:20%'>", file=f)
    print("<col style='width:80%'>", file=f)

    print("<tr><td>state id</td><td>%d</td></tr>"%n.uid, file=f)
    # if s.failure != None:
    #     print("<tr><td>status</td><td>failure</td></tr>", file=f)
    if s.initializing:
        print("<tr><td>status</td><td>initializing</td></tr>", file=f)
    elif len(s.ctxbag) == 0:
        if len(s.stopbag) == 0:
            print("<tr><td>status</td><td>terminal</td></tr>", file=f)
        else:
            print("<tr><td>status</td><td>stopped</td></tr>", file=f)
    else:
        print("<tr><td>status</td><td>normal</td></tr>", file=f)

    if verbose:
        print("<tr><td>from</td>", file=f)
        print("<td><table><tr>", file=f)
        for src in sorted(n.sources, key=lambda x: (x.len, x.uid)):
            print("<td><a href='javascript:show(%d)'>%d</td>"%(src.uid, src.uid), file=f)
        print("</tr></table></td></tr>", file=f)

    if s.choosing != None:
        print("<tr><td>choosing</td><td>%s</td></tr>"%s.choosing.nametag(), file=f)

    print("</table>", file=f)

def htmlnode(n, code, scope, f, verbose):
    print("<div id='div%d' style='display:none'>"%n.uid, file=f)
    print("<div class='container'>", file=f)

    print("<a name='N%d'/>"%n.uid, file=f)

    if verbose:
        print("<td>", file=f)
        height = htmlpath(n, "black", f)
        print("</td>", file=f)

    # if n.state.failure != None:
    #     print("<table border='1' style='color: red'><tr><td>Failure:</td>", file=f)
    #     print("<td>%s</td>"%n.state.failure, file=f)
    #     print("</tr></table>", file=f)

    print("<table border='1'>", file=f)
    print("<tr><th>Process</th><th>Status</th><th>Stack Trace</th><th>Variables</th>", file=f)
    if verbose:
        print("<th>FP</th><th>Stack</th>", file=f)
        print("<th>Steps</th><th>Next State</th></tr>", file=f)
    else:
        print("</tr>", file=f)
        print("<tr><td></td><td></td><td></td><td></td></tr>", file=f)
    for ctx in sorted(n.state.ctxbag.keys(), key=lambda x: x.nametag()):
        htmlrow(ctx, n.state.ctxbag, n, code, scope, f, verbose)
    for ctx in sorted(n.state.stopbag.keys(), key=lambda x: x.nametag()):
        htmlrow(ctx, n.state.stopbag, n, code, scope, f, verbose)

    print("</table>", file=f)
    print("</div>", file=f)
    print("</div>", file=f)

def htmlcode(code, scope, f):
    assert False
    print("<div id='table-wrapper'>", file=f)
    print("<div id='table-scroll'>", file=f)
    print("<table border='1'>", file=f)
    print("<tbody>", file=f)
    lastloc = None
    for pc in range(len(code)):
        print("<tr>", file=f)
        if scope.locations.get(pc) != None:
            (file, line) = scope.locations[pc]
            if (file, line) != lastloc:
                lines = files.get(file)
                if lines != None and line <= len(lines):
                    print("<th colspan='3' align='left' style='background-color: yellow'>%s:%d"%(html.escape(os.path.basename(file)), line),
                        html.escape(lines[line - 1]), "</th>", file=f)
                else:
                    print("<th colspan='2' align='left'>Line", line, "</th>", file=f)
                print("</tr><tr>", file=f)
            lastloc = (file, line)
        print("<td><a name='P%d'>"%pc, pc, "</a></td><td>", file=f)
        print("<span title='%s'>"%html.escape(code[pc].explain()), file=f)
        if isinstance(code[pc], JumpOp) or isinstance(code[pc], JumpCondOp):
            print("<a href='#P%d'>"%code[pc].pc, code[pc], "</a>", file=f)
        elif isinstance(code[pc], PushOp) and isinstance(code[pc].constant[0], PcValue):
            print("Push <a href='#P%d'>"%code[pc].constant[0].pc, strValue(code[pc].constant[0]), "</a>", file=f)
        else:
            print(html.escape(str(code[pc])), file=f)
        print("</span></td></tr>", file=f)
    print("</tbody>", file=f)
    print("</table>", file=f)
    print("</div>", file=f)
    print("</div>", file=f)

def htmldump(nodes, code, scope, node, fulldump, verbose):
    with open("harmony.html", "w", encoding='utf-8') as f:
        print("""
<html>
  <head>
    <style>
#table-wrapper {
  position:relative;
}
#table-scroll {
  height:200px;
  overflow:auto;  
}
#table-wrapper table {
  width:100%;
}
#table-wrapper table * {
  color:black;
}
#table-wrapper table thead th .text {
  position:absolute;   
  top:-20px;
  z-index:2;
  height:20px;
  width:35%;
  border:1px solid red;
}
table {
    border-collapse: collapse;
    border-style: hidden;
}
table td, table th {
    border: 1px solid black;
}
    </style>
  </head>
  <body>
        """, file=f)

        print("<table>", file=f)
        print("<col style='width:50%'>", file=f)
        print("<col style='width:50%'>", file=f)

        if node != None:
            print("<tr><td colspan='2'>", file=f)
            height = htmlpath(node, "red", f)
            print("</td></tr>", file=f)
            print("<tr><td></td></tr>", file=f)

        print("<tr>", file=f)

        print("<td valign='top'>", file=f)
        htmlcode(code, scope, f)
        print("</td>", file=f)

        print("<td valign='top'>", file=f)
        if fulldump:
            for n in nodes:
                htmlnode(n, code, scope, f, verbose)
        else:
            if node == None:
                cnt = 0
                for n in nodes:
                    htmlnode(n, code, scope, f, verbose)
                    cnt += 1
                    if not fulldump and cnt > 100:
                        break
            else:
                n = node
                while n != None:
                    htmlnode(n, code, scope, f, verbose)
                    n = n.parent
        print("</td>", file=f)
        print("</tr>", file=f)
        print("</table>", file=f)

        if node == None:
            row = 0
            sid = 1
        else:
            row = node.len + height + 1
            sid = node.uid
        print(
            """
                <div id='divNone' style='display:none';>
                  <div class='container'>
                    <p>
                        State information not available.
                        Use harmony -d for a complete htmldump.
                    </p>
                  </div>
                </div>

                <script>
                  var current = 1;

                  function show(id) {
                      x = document.getElementById('div' + current);
                      if (x == null) {
                          x = document.getElementById('divNone')
                      }
                      x.style.display = 'none';
                      x = document.getElementById('div' + id)
                      if (x == null) {
                          x = document.getElementById('divNone')
                      }
                      x.style.display = 'block';
                      current = id;
                  }

                  function rowshow(row, id) {
                    show(id);
                    var tbl = document.getElementById("issuestbl");
                    for (var i = 1; i < tbl.rows.length; i++) {
                        if (i == row + 1) {
                            tbl.rows[i].style.backgroundColor = "#A5FF33";
                        }
                        else {
                            tbl.rows[i].style.backgroundColor = "";
                        }
                    }
                  }

                  function setrow(tblid, row) {
                    var tbl = document.getElementById('loc' + tblid);
                    for (var i = 0; i < tbl.rows.length; i++) {
                        var div = document.getElementById('vars' + tblid + '_' + i);
                        if (i == row) {
                            tbl.rows[i].style.backgroundColor = "#A5FF33";
                            div.style.display = 'block';
                        }
                        else {
                            tbl.rows[i].style.backgroundColor = "";
                            div.style.display = 'none';
                        }
                    }
                  }

                  rowshow(%d, %d)
                </script>
            """%(row, sid), file=f)
        print("</body>", file=f)
        print("</html>", file=f)
    print("open file://" + os.getcwd() + "/harmony.html for more information")

def explanation(lop):
    return lop.op.explain()

def dumpModule(name, scope, f, last):
    print('    "%s": {'%name, file=f)
    print('      "file": "%s",'%scope.file, file=f)
    print('      "lines": [', file=f)
    with open(scope.file, encoding='utf-8') as fdx:
        lines = fdx.read().splitlines()
        first = True
        for line in lines:
            if first:
                first = False
            else:
                print(",", file=f)
            print('        %s'%json.dumps(line), end="", file=f)
    print(file=f)
    print('      ],', file=f)
    print('      "identifiers": {', file=f)
    for k,(t,_) in scope.pmap.items():
        print('        "%s": "%s",'%(k,t), file=f)
    print('        "___": "___"', file=f)
    print('      }', file=f)
    if last:
        print('    }', file=f)
    else:
        print('    },', file=f)

def dumpCode(printCode, code, scope, f=sys.stdout):
    lastloc = None
    if printCode == "json":
        print("{", file=f)
        print('  "labels": {', file=f)
        if True:
            for (k, v) in scope.labels.items():
                print('    "%s": "%d",'%(k, v), file=f)
        else:
            for pc, lop in enumerate(code.labeled_ops):
                for label in lop.labels:
                    if label.module == None:
                        print('    "%s": %d,'%(label.label, pc), file=f)
                    else:
                        print('    "%s$%s": %d,'%(label.module, label.label, pc), file=f)
        print('    "__end__": %d'%len(code.labeled_ops), file=f)
        print('  },', file=f)
        print('  "modules": {', file=f);
        imported = getImported()
        for m, s in imported.items():
            dumpModule(m, s, f, False)
        dumpModule("__main__", scope, f, True)
        print('  },', file=f)
        print('  "code": [', file=f)
    for pc in range(len(code.labeled_ops)):
        if printCode == "verbose":
            lop = code.labeled_ops[pc]
            file, line = code.curFile, code.curLine
            if file != None and (file, line) != lastloc:
                lines = files.get(file)
                if lines != None and line <= len(lines):
                    print("%s:%d"%(file, line), lines[line - 1], file=f)
                else:
                    print(file, ":", line, file=f)
                lastloc = (file, line)
            # for label in code.labeled_ops[pc].labels:
            #     if label.module == None:
            #         print("%s:"%label.label)
            #     else:
            #         print("%s.%s"%(label.module, label.label))
            print("  ", pc, code.labeled_ops[pc].op, file=f)
        elif printCode == "json":
            if pc < len(code.labeled_ops) - 1:
                print("    %s,"%code.labeled_ops[pc].op.jdump(), file=f)
            else:
                print("    %s"%code.labeled_ops[pc].op.jdump(), file=f)
        else:
            print(code.labeled_ops[pc].op, file=f)
    if printCode == "json":
        print("  ],", file=f)
        print('  "pretty": [', file=f)
        for pc in range(len(code.labeled_ops)):
            if pc < len(code.labeled_ops) - 1:
                print('    [%s,%s],'%(json.dumps(str(code.labeled_ops[pc].op), ensure_ascii=False), json.dumps(explanation(code.labeled_ops[pc]), ensure_ascii=False)), file=f)
            else:
                print('    [%s,%s]'%(json.dumps(str(code.labeled_ops[pc].op), ensure_ascii=False), json.dumps(explanation(code.labeled_ops[pc]), ensure_ascii=False)), file=f)
        print("  ],", file=f)
        print("  \"locs\": [", file=f, end="")
        firstTime = True
        for pc in range(len(code.labeled_ops)):
            lop = code.labeled_ops[pc]
            (_, file, line, column) = lop.start
            (endlexeme, _, endline, endcolumn) = lop.stop
            endcolumn += len(endlexeme) - 1
            if lop.stmt == None:
                line1 = line
                column1 = column
                line2 = endline
                column2 = endcolumn
            else:
                (line1, column1, line2, column2) = lop.stmt
            if (line, column) < (line1, column1):
                line = line1
                column = column1
            if (line, column) > (line2, column2):
                line = line2
                column = column2
            if (endline, endcolumn) > (line2, column2):
                endline = line2
                endcolumn = column2
            if (endline, endcolumn) < (line1, column1):
                endline = line1
                endcolumn = column1
            assert line <= endline
            assert (line < endline) or (column <= endcolumn), (module, line, endline, column, endcolumn, lop.start, lop.stop, lop.stmt)
            if False:        # TODO: debugging
                line = line1
                column = column1
                endline = line2
                endcolumn = column2
            if file != None:
                if firstTime:
                    firstTime = False
                    print(file=f)
                else:
                    print(",", file=f)
                if endlexeme in { "indent", "dedent" }:     # Hack...
                    endlexeme = endlexeme[0]
                if lop.module == None:
                    module = "__None__"
                else:
                    module = lop.module
                print("    { \"module\": \"%s\", \"line\": %d, \"column\": %d, \"endline\": %d, \"endcolumn\": %d, \"stmt\": [%d,%d,%d,%d] }"%(module, line, column, endline, endcolumn, line1, column1, line2, column2), file=f, end="")
        print(file=f)
        print("  ]", file=f)
        if False:
            print("  \"locations\": {", file=f, end="")
            firstTime = True
            for pc in range(len(code.labeled_ops)):
                lop = code.labeled_ops[pc]
                (_, file, line, column) = lop.start
                (endlexeme, _, endline, endcolumn) = lop.stop
                endcolumn += len(endlexeme) - 1
                if lop.stmt == None:
                    line1 = line
                    column1 = column
                    line2 = endline
                    column2 = endcolumn
                else:
                    (line1, column1, line2, column2) = lop.stmt
                if (line, column) < (line1, column1):
                    line = line1
                    column = column1
                if (line, column) > (line2, column2):
                    line = line2
                    column = column2
                if (endline, endcolumn) > (line2, column2):
                    endline = line2
                    endcolumn = column2
                if (endline, endcolumn) < (line1, column1):
                    endline = line1
                    endcolumn = column1
                if False:        # TODO: debugging
                    line = line1
                    column = column1
                    endline = line2
                    endcolumn = column2
                if file != None:
                    if firstTime:
                        firstTime = False
                        print(file=f)
                    else:
                        print(",", file=f)
                    if endlexeme in { "indent", "dedent" }:     # Hack...
                        endlexeme = endlexeme[0]
                    if lop.module == None:
                        module = "__None__"
                    else:
                        module = lop.module
                    print("    \"%d\": { \"module\": \"%s\", \"file\": %s, \"line\": %d, \"column\": %d, \"endline\": %d, \"endcolumn\": %d, \"stmt\": [%d,%d,%d,%d], \"code\": %s }"%(pc, module, json.dumps(file, ensure_ascii=False), line, column, endline, endcolumn, line1, column1, line2, column2, json.dumps(files[file][line-1], ensure_ascii=False)), file=f, end="")
            print(file=f)
            print("  }", file=f)
        print("}", file=f)

tladefs = """-------- MODULE Harmony --------
EXTENDS Integers, FiniteSets, Bags, Sequences, TLC

\* This is the Harmony TLA+ module.  All the Harmony virtual machine
\* instructions are defined below.  Mostly, if the Harmony VM instruction
\* is called X, then its definition below is under the name OpX.  There
\* are some cases where there is an extension.  For example, the Store
\* instruction has two versions: OpStore and OpStoreInd, depending on
\* whether the variable is directly specified or its address is on the
\* stack of the current thread.

\* There are three variables:
\*  active: a set of the currently active contexts
\*  ctxbag: a multiset of all contexts
\*  shared: a map of variable names to Harmony values
\*
\* A context is the state of a thread.  A context may be atomic or not.
\* There can be at most one atomic context.  If there is an atomic context,
\* it and only it is in the active set.  If there is no atomic context,
\* then the active set is the domain of the ctxbag.
VARIABLE active, ctxbag, shared
allvars == << active, ctxbag, shared >>

\* The variable "shared" is a Harmony dict type
SharedInvariant == shared.ctype = "dict"

TypeInvariant == SharedInvariant

\* Harmony values are represented by a ctype tag that contains the name of
\* their Harmony type and a cval that contains their TLA+ representation
HBool(x)    == [ ctype |-> "bool",    cval |-> x ]
HInt(x)     == [ ctype |-> "int",     cval |-> x ]
HStr(x)     == [ ctype |-> "str",     cval |-> x ]
HPc(x)      == [ ctype |-> "pc",      cval |-> x ]
HList(x)    == [ ctype |-> "list",    cval |-> x ]
HDict(x)    == [ ctype |-> "dict",    cval |-> x ]
HSet(x)     == [ ctype |-> "set",     cval |-> x ]
HAddress(x) == [ ctype |-> "address", cval |-> x ]
HContext(x) == [ ctype |-> "context", cval |-> x ]

\* Defining the Harmony constant (), which is an empty dict
EmptyFunc == [x \in {} |-> TRUE]
EmptyDict == HDict(EmptyFunc)

\* Flatten a sequence of sequences
Flatten(seq) ==
    LET F[i \\in 0..Len(seq)] == IF i = 0 THEN <<>> ELSE F[i-1] \\o seq[i]
    IN F[Len(seq)]

\* Harmony values are ordered first by their type
HRank(x) ==
    CASE x.ctype = "bool"    -> 0
    []   x.ctype = "int"     -> 1
    []   x.ctype = "str"     -> 2
    []   x.ctype = "pc"      -> 3
    []   x.ctype = "list"    -> 4
    []   x.ctype = "dict"    -> 5
    []   x.ctype = "set"     -> 6
    []   x.ctype = "address" -> 7
    []   x.ctype = "context" -> 8

\* TLA+ does not seem to have a direct way to compare characters in a
\* string, so...  Note that this only contains the printable ASCII
\* characters and excludes the backquote and double quote characters
\* as well as the backslash
CRank(c) ==
    CASE c=" "->32[]c="!"->33[]c="#"->35[]c="$"->36[]c="%"->37[]c="&"->38
    []c="'"->39[]c="("->40[]c=")"->41[]c="*"->42[]c="+"->43[]c=","->44
    []c="-"->45[]c="."->46[]c="/"->47[]c="0"->48[]c="1"->49[]c="2"->50
    []c="3"->51[]c="4"->52[]c="5"->53[]c="6"->54[]c="7"->55[]c="8"->56
    []c="9"->57[]c=":"->58[]c=";"->59[]c="<"->60[]c="="->61[]c=">"->62
    []c="?"->63[]c="@"->64[]c="A"->65[]c="B"->66[]c="C"->67[]c="D"->68
    []c="E"->69[]c="F"->70[]c="G"->71[]c="H"->72[]c="I"->73[]c="J"->74
    []c="K"->75[]c="L"->76[]c="M"->77[]c="N"->78[]c="O"->79[]c="P"->80
    []c="Q"->81[]c="R"->82[]c="S"->83[]c="T"->84[]c="U"->85[]c="V"->86
    []c="W"->87[]c="X"->88[]c="Y"->89[]c="Z"->90[]c="["->91[]c="]"->93
    []c="^"->94[]c="_"->95[]c="a"->97[]c="b"->98[]c="c"->99
    []c="d"->100[]c="e"->101[]c="f"->102[]c="g"->103[]c="h"->104
    []c="i"->105[]c="j"->106[]c="k"->107[]c="l"->108[]c="m"->109
    []c="n"->110[]c="o"->111[]c="p"->112[]c="q"->113[]c="r"->114
    []c="s"->115[]c="t"->116[]c="u"->117[]c="v"->118[]c="w"->119
    []c="x"->120[]c="y"->121[]c="z"->122[]c="{"->123[]c="|"->124
    []c="}"->125[]c="~"->126

\* Comparing two TLA+ strings
RECURSIVE StrCmp(_,_)
StrCmp(x, y) ==
    IF x = y
    THEN
        0
    ELSE
        CASE Len(x) = 0 ->  1
        []   Len(y) = 0 -> -1
        [] OTHER ->
            LET rx == CRank(Head(x))
                ry == CRank(Head(y))
            IN
                CASE rx < ry -> -1
                []   rx > ry ->  1
                [] OTHER -> StrCmp(Tail(x), Tail(y))

\* Setting up to compare two arbitrary Harmony values
RECURSIVE SeqCmp(_,_)
RECURSIVE HCmp(_,_)
RECURSIVE HSort(_)
RECURSIVE DictSeq(_)

\* Given a Harmony dictionary, return a sequence of its key, value
\* pairs sorted by the corresponding key.
DictSeq(dict) ==
    LET dom == HSort(DOMAIN dict)
    IN [ x \in 1..Len(dom) |-> << dom[x], dict[dom[x]] >> ]

\* Two dictionaries are ordered by their sequence of (key, value) pairs
\* Equivalently, we can flatten the sequence of (key, value) pairs first
\* into a single sequence of alternating keys and values.  Then we
\* compare the two sequences.
DictCmp(x, y) == SeqCmp(Flatten(DictSeq(x)), Flatten(DictSeq(y)))

\* Lexicographically compare two sequences of Harmony values
SeqCmp(x, y) ==
    IF x = y
    THEN
        0
    ELSE
        CASE Len(x) = 0 ->  1
        []   Len(y) = 0 -> -1
        [] OTHER ->
            LET c == HCmp(Head(x), Head(y))
            IN
                CASE c < 0 -> -1
                []   c > 0 ->  1
                [] OTHER -> SeqCmp(Tail(x), Tail(y))

\* Compare two contexts.  Essentially done lexicographically
CtxCmp(x, y) ==
    IF x = y THEN 0
    ELSE IF x.pc # y.pc THEN x.pc - y.pc
    ELSE IF x.apc # y.apc THEN x.apc - y.apc
    ELSE IF x.atomic # y.atomic THEN x.atomic - y.atomic
    ELSE IF x.vs # y.vs THEN DictCmp(x.vs, y.vs)
    ELSE IF x.stack # y.stack THEN SeqCmp(x.stack.cval, y.stack.cal)
    ELSE IF x.interruptLevel # y.interruptLevel THEN
             IF x.interruptLevel THEN -1 ELSE 1
    ELSE IF x.trap # y.trap THEN SeqCmp(x.trap, y.trap)
    ELSE IF x.readonly # y.readonly THEN x.readonly - y.readonly
    ELSE Assert(FALSE, "CtxCmp: this should not happen")

\* Compare two Harmony values as specified in the book
\* Return negative if x < y, 0 if x = y, and positive if x > y
HCmp(x, y) ==
    IF x = y
    THEN
        0
    ELSE
        IF x.ctype = y.ctype
        THEN 
            CASE x.ctype = "bool"    -> IF x.cval THEN 1 ELSE -1
            []   x.ctype = "int"     -> x.cval - y.cval
            []   x.ctype = "str"     -> StrCmp(x.cval, y.cval)
            []   x.ctype = "pc"      -> x.cval - y.cval
            []   x.ctype = "list"    -> SeqCmp(x.cval, y.cval)
            []   x.ctype = "set"     -> SeqCmp(HSort(x.cval), HSort(y.cval))
            []   x.ctype = "dict"    -> DictCmp(x.cval, y.cval)
            []   x.ctype = "address" -> SeqCmp(x.cval, y.cval)
            []   x.ctype = "context" -> CtxCmp(x.cval, y.cval)
        ELSE
            HRank(x) - HRank(y)

\* The minimum and maximum Harmony value in a set
HMin(s) == CHOOSE x \in s: \A y \in s: HCmp(x, y) <= 0
HMax(s) == CHOOSE x \in s: \A y \in s: HCmp(x, y) >= 0

\* Sort a set of Harmony values into a sequence
HSort(s) ==
    IF s = {}
    THEN
        <<>>
    ELSE
        LET min == HMin(s) IN << min >> \\o HSort(s \\ {min})

\* This is to represent "variable name hierarchies" used in expressions
\* such as (x, (y, z)) = (1, (2, 3))
VName(name) == [ vtype |-> "var", vname |-> name ]
VList(list) == [ vtype |-> "tup", vlist |-> list ]

\* An address has a function and a list of argument, each of which are
\* Harmony values
Address(f, a) == HAddress([ func |-> f, args |-> a ])

\* Defining the Harmony constant None
None      == Address(EmptyFunc, <<>>)

\* Representation of a context (the state of a thread).  It includes
\* the following fields:
\*  pc:     the program counter (location in the code)
\*  apc:    if atomic, the location in the code where the thread became atomic
\*  atomic: a counter: 0 means not atomic, larger than 0 is atomic
\*  vs:     a Harmony dictionary containing the variables of this thread
\*  stack:  a sequence of Harmony values
\*  interruptLevel: false if enabled, true if disabled
\*  trap:   either <<>> or a tuple containing the trap method and argument
\*  readonly: larger than 0 means not allowed to modify shared state
Context(pc, atomic, vs, stack, interruptLevel, trap, readonly) ==
    [
        pc             |-> pc,
        apc            |-> pc,
        atomic         |-> atomic,
        vs             |-> vs,
        stack          |-> stack,
        interruptLevel |-> interruptLevel,
        trap           |-> trap,
        readonly       |-> readonly
    ]

\* An initial context of a thread.  arg is the argument given when the thread
\* thread was spawned.  "process" is used by the OpReturn operator.
InitContext(pc, atomic, arg) ==
    Context(pc, atomic, EmptyDict, << arg, "process" >>, FALSE, <<>>, 0)

\* Update the given map with a new key -> value mapping
UpdateMap(map, key, value) ==
    [ x \\in (DOMAIN map) \\union {key} |-> IF x = key THEN value ELSE map[x] ]

\* Update a Harmony dictionary with a new key -> value mapping
UpdateDict(dict, key, value) ==
    HDict(UpdateMap(dict.cval, key, value))

\* The initial state of the Harmony module consists of a single thread starting
\* at pc = 0 and an empty set of shared variables
Init ==
    LET ctx == InitContext(0, 1, EmptyDict)
    IN /\\ active = { ctx }
       /\\ ctxbag = SetToBag(active)
       /\\ shared = EmptyDict

\* The state of the current thread goes from 'self' to 'next'.  Update
\* both the context bag and the active set
UpdateContext(self, next) ==
    /\\ active' = (active \\ { self }) \\union { next }
    /\\ ctxbag' = (ctxbag (-) SetToBag({self})) (+) SetToBag({next})

\* Remove context from the active set and context bag.  Make all contexts
\* in the context bag active
RemoveContext(self) ==
    /\\ ctxbag' = ctxbag (-) SetToBag({self})
    /\\ active' = BagToSet(ctxbag')

\* A Harmony address is essentially a sequence of Harmony values
\* These compute the head (the first element) and the remaining tail
AddrHead(addr) == Head(addr.cval)
AddrTail(addr) == HAddress(Tail(addr.cval))

\* Given a non-negative integer, return a sequence of bits starting
\* with least significant one
RECURSIVE Int2BitsHelp(_)
Int2BitsHelp(x) ==
    IF x = 0
    THEN <<>>
    ELSE <<x % 2 = 1>> \o Int2BitsHelp(x \\div 2)

\* Convert an integer to a bit sequence, lsb first. neg indicates if the
\* value is negative.
Int2Bits(x) ==
    IF x < 0
    THEN [ neg |-> TRUE,  bits |-> Int2BitsHelp(-x-1) ]
    ELSE [ neg |-> FALSE, bits |-> Int2BitsHelp(x)    ]

\* Convert a bit sequence (lsb first) to a non-negative integer
RECURSIVE Bits2IntHelp(_)
Bits2IntHelp(x) == 
    IF x = <<>>
    THEN 0
    ELSE (IF Head(x) THEN 1 ELSE 0) + 2 * Bits2IntHelp(Tail(x))

\* Convert a bit sequence to an integer.
Bits2Int(b) ==
    IF b.neg
    THEN -Bits2IntHelp(b.bits) - 1
    ELSE Bits2IntHelp(b.bits)

\* Compute the bitwise negation of a bit sequence
BitsNegate(b) == [ neg |-> ~b.neg, bits |-> b.bits ]

\* Compute b >> n
BitsShiftRight(b, n) ==
    IF n >= Len(b.bits)
    THEN [ neg |-> b.neg, bits |-> <<>> ]
    ELSE [ neg |-> b.neg, bits |-> SubSeq(b.bits, n + 1, Len(b.bits)) ]

\* Compute b << n
BitsShiftLeft(b, n) ==
    [ neg |-> b.neg, bits |-> [ x \in 1..n |-> b.neg ] \o b.bits ]

\* Helper functions for BitsXOR
RECURSIVE BitsXORhelp(_,_)
BitsXORhelp(x, y) ==
    CASE x = <<>> -> y
    []   y = <<>> -> x
    [] OTHER -> << Head(x) # Head (y) >> \o BitsXORhelp(Tail(x), Tail(y))

\* Compute x XOR y
BitsXOR(x, y) ==
    [ neg |-> x.neg # y.neg, bits |-> BitsXORhelp(x.bits, y.bits) ]

\* Helper function for BitsOr
RECURSIVE BitsOrHelp(_,_)
BitsOrHelp(x, y) ==
    CASE x.bits = <<>> -> IF x.neg THEN <<>> ELSE y.bits
    []   y.bits = <<>> -> IF y.neg THEN <<>> ELSE x.bits
    [] OTHER -> << (x.neg \\/ y.neg) #
            ((Head(x.bits) # x.neg) \\/ (Head(y.bits) # y.neg)) >> \o
            BitsOrHelp(
                [ neg |-> x.neg, bits |-> Tail(x.bits) ],
                [ neg |-> y.neg, bits |-> Tail(y.bits) ])

\* Compute x OR y
BitsOr(x, y) ==
    [ neg  |-> x.neg \\/ y.neg, bits |-> BitsOrHelp(x, y) ]

\* Helper function for BitsAnd
RECURSIVE BitsAndHelp(_,_)
BitsAndHelp(x, y) ==
    CASE x.bits = <<>> -> IF x.neg THEN y.bits ELSE <<>>
    []   y.bits = <<>> -> IF y.neg THEN x.bits ELSE <<>>
    [] OTHER -> << (x.neg /\\ y.neg) #
            ((Head(x.bits) # x.neg) /\\ (Head(y.bits) # y.neg)) >> \o
            BitsAndHelp(
                [ neg |-> x.neg, bits |-> Tail(x.bits) ],
                [ neg |-> y.neg, bits |-> Tail(y.bits) ])

\* Compute x AND y
BitsAnd(x, y) ==
    [ neg  |-> x.neg /\\ y.neg, bits |-> BitsAndHelp(x, y) ]

\* This is to implement del !addr, where addr is a Harmony address
\* (a sequence of Harmony values representing a path in dir, a directory.
\* It is a recursive operator that returns the new directory.
RECURSIVE RemoveDirAddr(_, _)
RemoveDirAddr(dir, addr) ==
    LET next == AddrHead(addr) IN
        CASE dir.ctype = "dict" ->
            HDict(
                IF Len(addr.cval) = 1
                THEN
                    [ x \\in (DOMAIN dir.cval) \\ {next} |-> dir.cval[x] ]
                ELSE
                    [ x \\in (DOMAIN dir.cval) |->
                        IF x = next
                        THEN
                            RemoveDirAddr(dir.cval[x], AddrTail(addr))
                        ELSE
                            dir.cval[x]
                    ]
            )
        [] dir.ctype = "list" ->
            HList(
                CASE next.ctype = "int" /\ 0 <= next.cval /\ next.cval < Len(dir.cval) ->
                    IF Len(addr.cval) = 1
                    THEN
                        SubSeq(dir.cval, 1, next.cval) \\o
                        SubSeq(dir.cval, next.cval + 2, Len(dir.cval))
                    ELSE
                        [ x \\in (DOMAIN dir.cval) |->
                            IF x = next.cval + 1
                            THEN
                                RemoveDirAddr(dir.cval[x], AddrTail(addr))
                            ELSE
                                dir.cval[x]
                        ]
            )

\* This is to implement !addr = value, where addr is a Harmony address
\* (a sequence of Harmony values representing a path in dir, a directory
\* (tree where the internal nodes are dictionaries or lists), and value
\* is the new value.  It is a recursive operator that returns the new directory.
RECURSIVE UpdateDirAddr(_, _, _)
UpdateDirAddr(dir, addr, value) ==
    IF addr = <<>>
    THEN
        value
    ELSE
        LET next == Head(addr)
        IN
            CASE dir.ctype = "dict" ->
                HDict(
                    [ x \\in (DOMAIN dir.cval) \\union {next} |->
                        IF x = next
                        THEN
                            UpdateDirAddr(dir.cval[x], Tail(addr), value)
                        ELSE
                            dir.cval[x]
                    ]
                )
            [] dir.ctype = "list" ->
                HList(
                    CASE next.ctype = "int" /\ 0 <= next.cval /\ next.cval <= Len(dir.cval) ->
                        [ x \\in (DOMAIN dir.cval) \\union {next.cval + 1} |->
                            IF x = next.cval + 1
                            THEN
                                UpdateDirAddr(dir.cval[x], Tail(addr), value)
                            ELSE
                                dir.cval[x]
                        ]
                )

\* This is to compute the value of !addr in dir, which is a simple
\* recursive function
RECURSIVE LoadDirAddr(_, _)
LoadDirAddr(dir, addr) ==
    IF addr.cval = <<>>
    THEN
        dir
    ELSE
        LET next == AddrHead(addr)
        IN
            CASE dir.ctype = "dict" ->
                LoadDirAddr(dir.cval[next], AddrTail(addr))
            [] dir.ctype = "list" ->
                CASE next.ctype = "int" ->
                    LoadDirAddr(dir.cval[next.cval + 1], AddrTail(addr))

\* This is a helper operator for UpdateVars.
\* Harmony allows statements of the form: x,(y,z) = v.  For example,
\* if v = (1, (2, 3)), then this assigns 1 to x, 2 to y, and 3 to z.
\* For this operator, args is a tree describing the lefthand side,
\* while value is the righthand side of the equation above.  The
\* operator creates a sequence of (variable, value) records.  In the
\* example, the sequence would be << (x,1), (y,2), (z,3) >> essentially.
RECURSIVE CollectVars(_, _)
CollectVars(args, value) ==
    IF args.vtype = "var"
    THEN << [ var |-> HStr(args.vname), val |-> value ] >>
    ELSE
        Flatten([ i \\in DOMAIN args.vlist |->
            CollectVars(args.vlist[i], value.cval[i])
        ])

\* Another helper operator for UpdateVars.  dict is a Harmony dictionary,
\* cv is a sequence as returned by CollectVars, and index is an index into
\* this sequence.  Fold returns an updated dictionary.
RECURSIVE Fold(_, _, _)
Fold(dict, cv, index) ==
    IF index = 0
    THEN dict
    ELSE
        LET elt == cv[index]
        IN Fold(UpdateDict(dict, elt.var, elt.val), cv, index - 1)

\* As explained in CollectVars, args is a tree of variable names that
\* appears on the lefthandside of a Harmony assignment operation.  value
\* is the value of the righthandside.  The vs are the variables of the
\* context that need to be updated.
UpdateVars(vs, args, value) ==
    LET cv == CollectVars(args, value)
    IN Fold(vs, cv, Len(cv))

\* A no-op
OpContinue(self) ==
    /\\ UpdateContext(self, [self EXCEPT !.pc = @ + 1])
    /\\ UNCHANGED shared

\* Pop the new interrupt level and push the old one
OpSetIntLevel(self) ==
    LET nl   == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.interruptLevel = nl.cval,
            !.stack = << HBool(self.interruptLevel) >> \\o Tail(@)]
    IN
        /\\ nl.ctype = "bool"
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Increment the readonly counter (counter because of nesting)
OpReadonlyInc(self) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.readonly = @ + 1]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Decrement the readonly counter
OpReadonlyDec(self) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.readonly = @ - 1]
    IN
        /\\ self.readonly > 0
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* This is used temporarily for Harmony VM instructions that have not yet
\* been implemented
Skip(self, what) == OpContinue(self)

\* First instruction of every method.  Saves the current variables on the stack,
\* Assigns the top of the stack to args (see UpdateVars) and initializes variable
\* result to None.
OpFrame(self, name, args) ==
    LET next == [
        self EXCEPT !.pc = @ + 1,
        !.stack = << self.vs >> \\o Tail(@),
        !.vs = UpdateVars(EmptyDict, args, Head(self.stack))
    ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Remove one element from the stack
OpPop(self) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Remove key from the given map
DictCut(dict, key) == [ x \in (DOMAIN dict) \ { key } |-> dict[x] ]

\* v contains the name of a local variable.  v can be a "variable tree"
\* (see UpdateVars).  The stack contains an index on top with an iterable
\* value below it.  OpCut should assign the value at that index to v.
\* If the index is valid, OpCut should also increment the index on top
\* of the stack (leaving the iterable value) and push True.  If not,
\* OpCut should pop both the index and the iterable value and push False.
OpCut(self, v) ==
    LET index    == self.stack[1]
        iterable == self.stack[2]
    IN
        /\\ CASE iterable.ctype = "list" ->
                IF index.cval < Len(iterable.cval)
                THEN
                    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(TRUE), HInt(index.cval + 1) >> \\o Tail(@), !.vs = UpdateVars(@, v, iterable.cval[index.cval + 1])]
                    IN UpdateContext(self, next)
                ELSE
                    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(FALSE) >> \\o Tail(Tail(@))]
                    IN UpdateContext(self, next)
            [] iterable.ctype = "str" ->
                IF index.cval < Len(iterable.cval)
                THEN
                    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(TRUE), HInt(index.cval + 1) >> \\o Tail(@), !.vs = UpdateVars(@, v, HStr(SubSeq(iterable.cval, index.cval + 1, index.cval + 1)))]
                    IN UpdateContext(self, next)
                ELSE
                    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(FALSE) >> \\o Tail(Tail(@))]
                    IN UpdateContext(self, next)
            [] iterable.ctype = "set" ->
                IF index.cval < Cardinality(iterable.cval)
                THEN
                    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(TRUE), HInt(index.cval + 1) >> \\o Tail(@), !.vs = UpdateVars(@, v, HSort(iterable.cval)[index.cval + 1])]
                    IN UpdateContext(self, next)
                ELSE
                    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(FALSE) >> \\o Tail(Tail(@))]
                    IN UpdateContext(self, next)
            [] iterable.ctype = "dict" ->
                IF index.cval < Cardinality(DOMAIN iterable.cval)
                THEN
                    LET items == DictSeq(iterable.cval)
                        next  == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(TRUE), HInt(index.cval + 1) >> \\o Tail(@), !.vs = UpdateVars(@, v, items[index.cval + 1][1])]
                    IN UpdateContext(self, next)
                ELSE
                    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(FALSE) >> \\o Tail(Tail(@))]
                    IN UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Much like OpCut, but there are two variables that must be assigned: the key k
\* and the value v.
OpCut2(self, v, k) ==
    LET index    == self.stack[1]
        iterable == self.stack[2]
    IN
        /\\ CASE iterable.ctype = "list" ->
                IF index.cval < Len(iterable.cval)
                THEN
                    LET intm == UpdateVars(self.vs, k, index)
                        next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(TRUE), HInt(index.cval + 1) >> \\o Tail(@), !.vs = UpdateVars(intm, v, iterable.cval[index.cval + 1])]
                    IN UpdateContext(self, next)
                ELSE
                    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(FALSE) >> \\o Tail(Tail(@))]
                    IN UpdateContext(self, next)
            [] iterable.ctype = "str" ->
                IF index.cval < Len(iterable.cval)
                THEN
                    LET intm == UpdateVars(self.vs, k, index)
                        next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(TRUE), HInt(index.cval + 1) >> \\o Tail(@), !.vs = UpdateVars(intm, v, HStr(SubSeq(iterable.cval, index.cval + 1, index.cval + 1)))]
                    IN UpdateContext(self, next)
                ELSE
                    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(FALSE) >> \\o Tail(Tail(@))]
                    IN UpdateContext(self, next)
            [] iterable.ctype = "set" ->
                IF index.cval < Cardinality(iterable.cval)
                THEN
                    LET intm == UpdateVars(self.vs, k, index)
                        next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(TRUE), HInt(index.cval + 1) >> \\o Tail(@), !.vs = UpdateVars(intm, v, HSort(iterable.cval)[index.cval + 1])]
                    IN UpdateContext(self, next)
                ELSE
                    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(FALSE) >> \\o Tail(Tail(@))]
                    IN UpdateContext(self, next)
            [] iterable.ctype = "dict" ->
                IF index.cval < Cardinality(DOMAIN iterable.cval)
                THEN
                    LET items == DictSeq(iterable.cval)
                        intm  == UpdateVars(self.vs, k, items[index.cval + 1][1])
                        next  == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(TRUE), HInt(index.cval + 1) >> \\o Tail(@), !.vs = UpdateVars(intm, v, items[index.cval + 1][2])]
                    IN UpdateContext(self, next)
                ELSE
                    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << HBool(FALSE) >> \\o Tail(Tail(@))]
                    IN UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Delete the shared variable pointed to be v.  v is a sequence of Harmony
\* values acting as an address (path in hierarchy of dicts)
OpDel(self, v) ==
    /\\ Assert(self.readonly = 0, "Del in readonly mode")
    /\\ UpdateContext(self, [self EXCEPT !.pc = @ + 1])
    /\\ shared' = RemoveDirAddr(shared, HAddress(v))

\* Delete the shared variable whose address is pushed on the stack
OpDelInd(self) ==
    LET addr == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
    IN
        /\\ UpdateContext(self, next)
        /\\ shared' = RemoveDirAddr(shared, addr)

\* Delete the given local variable
OpDelVar(self, v) ==
    LET next == [self EXCEPT !.pc = @ + 1,
        !.vs = HDict([ x \in (DOMAIN @.cval) \\ { HStr(v.vname) } |-> @.cval[x] ]) ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Delete the local variable whose address is pushed on the stack
OpDelVarInd(self) ==
    LET addr == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@),
                                    !.vs = RemoveDirAddr(@, addr)]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Increment the given local variable
OpIncVar(self, v) ==
    LET var  == HStr(v.vname)
        next == [self EXCEPT !.pc = @ + 1,
                    !.vs = UpdateDict(@, var, HInt(@.cval[var].cval + 1)) ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Assign the top of the stack to a local variable
OpStoreVar(self, v) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@), !.vs = UpdateVars(@, v, Head(self.stack))]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Push the value of the given variable onto the stack
OpLoadVar(self, v) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << self.vs.cval[HStr(v.vname)] >> \\o @ ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Increment the atomic counter for this thread.  If it was 0, boot every other
\* context out of the set of active contexts.
OpAtomicInc(self) ==
    IF self.atomic = 0
    THEN
        LET next == [self EXCEPT !.pc = @ + 1, !.apc = self.pc, !.atomic = 1]
        IN
            /\\ active' = { next }
            /\\ ctxbag' = (ctxbag (-) SetToBag({self})) (+) SetToBag({next})
            /\\ UNCHANGED shared
    ELSE
        LET next == [self EXCEPT !.pc = @ + 1, !.atomic = @ + 1]
        IN
            /\\ UpdateContext(self, next)
            /\\ UNCHANGED shared

\* Decrement the atomic counter.  If it becomes 0, let all other contexts
\* back into the active set.
OpAtomicDec(self) ==
    IF self.atomic = 1
    THEN
        LET next == [self EXCEPT !.pc = @ + 1, !.apc = 0, !.atomic = 0]
        IN
            /\\ ctxbag' = (ctxbag (-) SetToBag({self})) (+) SetToBag({next})
            /\\ active' = DOMAIN ctxbag'
            /\\ UNCHANGED shared
    ELSE
        LET next == [self EXCEPT !.pc = @ + 1, !.atomic = @ - 1]
        IN
            /\\ UpdateContext(self, next)
            /\\ UNCHANGED shared

\* Pop the top of stack and check if it is True.  If not, stop and print the
\* message.
OpAssert(self, msg) ==
    LET cond == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
    IN
        /\\ cond.ctype = "bool"
        /\\ Assert(cond.cval, msg)
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* The top of the stack contains an expression to be printed along with the
\* message if the next element on the stack is FALSE.
OpAssert2(self, msg) ==
    LET data == self.stack[1]
        cond == self.stack[2]
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(Tail(@))]
    IN
        /\\ cond.ctype = "bool"
        /\\ Assert(cond.cval, << msg, data >>)
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Print what is on top of the stack (and pop it)
OpPrint(self) ==
    LET msg == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
    IN
        /\\ PrintT(msg)
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Pop the top of the stack, which must be a set.  Then select one of the
\* elements and push it back onto the stack.
OpChoose(self) ==
    LET choices == Head(self.stack)
    IN
        \\E v \\in choices.cval:
            LET next == [self EXCEPT !.pc = @ + 1, !.stack = <<v>> \\o Tail(@)]
            IN
                /\\ choices.ctype = "set"
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared

\* "sequential" pops the address of a variable and indicates to the model
\* checker that the variable is assumed to have sequential consistency.
\* This turns off race condition checking for the variable.  For here, it can
\* just be considered a no-op.
OpSequential(self) == OpPop(self)

\* "invariant" is essentially a no-op.  Just skip over the code for the
\* invariant.
OpInvariant(self, end) ==
    /\\ UpdateContext(self, [self EXCEPT !.pc = end + 1])
    /\\ UNCHANGED shared

\* This is the general form of unary operators that replace the top of the
\* stack with a function computed over that value
OpUna(self, op(_)) ==
    LET e    == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = << op(e) >> \\o Tail(@)]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Similar to OpUna but replaces two values on the stack with a single one.
OpBin(self, op(_,_)) ==
    LET e1   == self.stack[1]
        e2   == self.stack[2]
        next == [self EXCEPT !.pc = @ + 1,
            !.stack = << op(e2, e1) >> \\o Tail(Tail(@))]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Apply binary operation op to first and the top of the stack n times
RECURSIVE StackFold(_,_,_,_)
StackFold(first, stack, op(_,_), n) ==
    IF n = 0
    THEN
        <<first>> \o stack
    ELSE
        StackFold(op(Head(stack), first), Tail(stack), op, n - 1)

\* Like OpBin, but perform for top n elements of the stack
OpNary(self, op(_,_), n) ==
    LET e1   == Head(self.stack)
        ns   == StackFold(e1, Tail(self.stack), op, n - 1)
        next == [self EXCEPT !.pc = @ + 1, !.stack = ns ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Turn a Harmony list/tuple into a (reversed) sequence
List2Seq(list) ==
    LET n == Cardinality(DOMAIN list)
    IN [ i \in 1..n |-> list[HInt(n - i)] ]

\* Pop a tuple of the stack and push each of its n components
OpSplit(self, n) ==
    LET ns   == List2Seq(Head(self.stack).cval) \o Tail(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = ns ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Move the stack element at position offset to the top
OpMove(self, offset) ==
    LET part1 == SubSeq(self.stack, 1, offset - 1)
        part2 == SubSeq(self.stack, offset, offset)
        part3 == SubSeq(self.stack, offset + 1, Len(self.stack))
        next  == [self EXCEPT !.pc = @ + 1, !.stack = part2 \o part1 \o part3 ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Duplicate the top of the stack
OpDup(self) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.stack = <<Head(@)>> \o @]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* The official "pc" of a thread depends on whether it is operating in
\* atomic mode or not.  If not, the pc is simply the current location
\* in the code.  However, if in atomic mode, the pc is the location where
\* the thread became atomic.
Location(ctx) == IF ctx.atomic > 0 THEN ctx.apc ELSE ctx.pc

\* Compute how many threads are currently at the given location
FunCountLabel(label) ==
    LET fdom == { c \\in DOMAIN ctxbag: Location(c) = label.cval }
        fbag == [ c \\in fdom |-> ctxbag[c] ]
    IN
        HInt(BagCardinality(fbag))

\* Convert the given integer into a string
RECURSIVE Int2Str(_)
Int2Str(x) ==
    IF x < 10
    THEN
        SubSeq("0123456789", x+1, x+1)
    ELSE
        LET rem == x % 10
        IN Int2Str(x \\div 10) \o SubSeq("0123456789", rem+1, rem+1)

\* Bunch of value to string conversion functions coming up
RECURSIVE Val2Str(_)
RECURSIVE Seq2Str(_)
RECURSIVE Addr2Str(_)
RECURSIVE Dict2StrHelp(_,_)

\* Convert a non-empty sequence of values to a string separated by commas
Seq2Str(x) ==
    IF Len(x) = 1
    THEN Val2Str(Head(x))
    ELSE Val2Str(Head(x)) \o ", " \o Seq2Str(Tail(x))

\* Convert a sequence of values of an address
Addr2Str(x) ==
    IF x = <<>>
    THEN ""
    ELSE "[" \o Val2Str(Head(x)) \o "]" \o Addr2Str(Tail(x))

\* Convert a non-empty dictionary to a string
Dict2StrHelp(keys, dict) ==
    LET first ==
        LET k == Head(keys) IN Val2Str(k) \o ": " \o Val2Str(dict[k])
    IN
        IF Len(keys) = 1
        THEN
            first
        ELSE
            first \o ", " \o Dict2StrHelp(Tail(keys), dict)

Dict2Str(x) == Dict2StrHelp(HSort(DOMAIN x), x)

\* Convert Harmony value x into a string
Val2Str(x) ==
    CASE x.ctype = "bool"    -> IF x.cval THEN "True" ELSE "False"
    []   x.ctype = "str"     -> "'" \o x.cval \o "'"
    []   x.ctype = "int"     -> Int2Str(x.cval)
    []   x.ctype = "pc"      -> "PC(" \o Int2Str(x.cval) \o ")"
    []   x.ctype = "list"     ->
            IF x.cval = {} THEN "[]" ELSE "[ " \o Seq2Str(HSort(x.cval)) \o " ]"
    []   x.ctype = "dict"    ->
            IF DOMAIN x.cval = {} THEN "{:}" ELSE "{ " \o Dict2Str(x.cval) \o " }"
    []   x.ctype = "set"     ->
            IF x.cval = {} THEN "{}" ELSE "{ " \o Seq2Str(HSort(x.cval)) \o " }"
    []   x.ctype = "address" -> "?" \o Head(x.cval).cval \o Addr2Str(Tail(x.cval))

\* Compute the cardinality of a set of dict, or the length of a string
FunLen(s) ==
    CASE s.ctype = "set"  -> HInt(Cardinality(s.cval))
    []   s.ctype = "list" -> HInt(Cardinality(DOMAIN s.cval))
    []   s.ctype = "dict" -> HInt(Cardinality(DOMAIN s.cval))
    []   s.ctype = "str"  -> HInt(Len(s.cval))

\* Add two integers, or concatenate two sequences or strings
FunAdd(x, y) ==
    CASE x.ctype = "int"  /\\ y.ctype = "int"  -> HInt(x.cval + y.cval)
    []   x.ctype = "list" /\\ y.ctype = "list" -> HList(x.cval \o y.cval)
    []   x.ctype = "str"  /\\ y.ctype = "str"  -> HStr(x.cval \o y.cval)

\* Check to see if x is the empty set, dict, or string
\* OBSOLETE
FunIsEmpty(x) ==
    CASE x.ctype = "set"  -> HBool(x.cval = {})
    []   x.ctype = "list" -> HBool(x.cval = <<>>)
    []   x.ctype = "dict" -> HBool((DOMAIN x.cval) = {})
    []   x.ctype = "str"  -> HBool(Len(x.cval) = 0)

\* Get the range of a dict (i.e., the values, not the keys)
Range(dict) == { dict[x] : x \in DOMAIN dict }

\* Get the minimum of a set or list
FunMin(x) ==
    CASE x.ctype = "set"  -> HMin(x.cval)
    []   x.ctype = "list" -> HMin(Range(x.cval))

\* Get the maximum of a set or list
FunMax(x) ==
    CASE x.ctype = "set"  -> HMax(x.cval)
    []   x.ctype = "list" -> HMax(Range(x.cval))

\* See if any element in the set or list is true
FunAny(x) ==
    CASE x.ctype = "set"  -> HBool(HBool(TRUE) \in x.cval)
    []   x.ctype = "list" -> HBool(HBool(TRUE) \in Range(x.cval))

\* See if all elements in the set of list are true
FunAll(x) ==
    CASE x.ctype = "set"  -> HBool(x.cval = { HBool(TRUE) })
    []   x.ctype = "list" -> HBool(HBool(FALSE) \\notin Range(x.cval))

\* Can be applied to integers or sets
FunSubtract(x, y) ==
    CASE x.ctype = "int" /\\ y.ctype = "int" -> HInt(x.cval - y.cval)
    []   x.ctype = "set" /\\ y.ctype = "set" -> HSet(x.cval \\ y.cval)

\* The following are self-explanatory
FunStr(v)           == HStr(Val2Str(v))
FunMinus(v)         == HInt(-v.cval)
FunNegate(v)        == HInt(Bits2Int(BitsNegate(Int2Bits(v.cval))))
FunAbs(v)           == HInt(IF v.cval < 0 THEN -v.cval ELSE v.cval)
FunNot(v)           == HBool(~v.cval)
FunKeys(x)          == HSet(DOMAIN x.cval)
FunRange(x, y)      == HSet({ HInt(i) : i \in x.cval .. y.cval })
FunEquals(x, y)     == HBool(x = y)
FunNotEquals(x, y)  == HBool(x /= y)
FunLT(x, y)         == HBool(HCmp(x, y) < 0)
FunLE(x, y)         == HBool(HCmp(x, y) <= 0)
FunGT(x, y)         == HBool(HCmp(x, y) > 0)
FunGE(x, y)         == HBool(HCmp(x, y) >= 0)
FunDiv(x, y)        == HInt(x.cval \\div y.cval)
FunMod(x, y)        == HInt(x.cval % y.cval)
FunPower(x, y)      == HInt(x.cval ^ y.cval)
FunSetAdd(x, y)     == HSet(x.cval \\union {y})
FunShiftRight(x, y) == HInt(Bits2Int(BitsShiftRight(Int2Bits(x.cval), y.cval)))
FunShiftLeft(x, y)  == HInt(Bits2Int(BitsShiftLeft(Int2Bits(x.cval), y.cval)))

\* Functions to create and extend addresses
FunClosure(x, y)    == Address(x, <<y>>)
FunAddArg(x, y)     == Address(x.cval.func, x.cval.args \o <<y>>)

\* Compute either XOR of two ints or the union minus the intersection
\* of two sets
FunExclusion(x, y) ==
    CASE x.ctype = "set" /\\ y.ctype = "set" ->
        HSet((x.cval \\union y.cval) \\ (x.cval \\intersect y.cval))
    [] x.ctype = "int" /\\ y.ctype = "int" ->
        HInt(Bits2Int(BitsXOR(Int2Bits(x.cval), Int2Bits(y.cval))))

\* Merge two dictionaries.  If two keys conflict, use the minimum value
MergeDictMin(x, y) ==
    [ k \in DOMAIN x \\union DOMAIN y |->
        CASE k \\notin DOMAIN x -> y[k]
        []   k \\notin DOMAIN y -> x[k]
        [] OTHER -> IF HCmp(x[k], y[k]) < 0 THEN x[k] ELSE y[k]
    ]

\* Merge two dictionaries.  If two keys conflict, use the maximum value
MergeDictMax(x, y) ==
    [ k \in DOMAIN x \\union DOMAIN y |->
        CASE k \\notin DOMAIN x -> y[k]
        []   k \\notin DOMAIN y -> x[k]
        [] OTHER -> IF HCmp(x[k], y[k]) > 0 THEN x[k] ELSE y[k]
    ]

\* Union of two sets or dictionaries
FunUnion(x, y) ==
    CASE x.ctype = "set" /\\ y.ctype = "set" ->
        HSet(x.cval \\union y.cval)
    [] x.ctype = "dict" /\\ y.ctype = "dict" ->
        HDict(MergeDictMax(x.cval, y.cval))
    [] x.ctype = "int" /\\ y.ctype = "int" ->
        HInt(Bits2Int(BitsOr(Int2Bits(x.cval), Int2Bits(y.cval))))

\* Intersection of two sets or dictionaries
FunIntersect(x, y) ==
    CASE x.ctype = "set" /\\ y.ctype = "set" ->
        HSet(x.cval \\intersect y.cval)
    [] x.ctype = "dict" /\\ y.ctype = "dict" ->
        HDict(MergeDictMin(x.cval, y.cval))
    [] x.ctype = "int" /\\ y.ctype = "int" ->
        HInt(Bits2Int(BitsAnd(Int2Bits(x.cval), Int2Bits(y.cval))))

\* See if x is in y, where y is a set, a dict, or a string. In case of
\* a string, check if x is a substring of y
FunIn(x, y) ==
    CASE y.ctype = "set"  -> HBool(x \in y.cval)
    []   y.ctype = "list" -> HBool(\E k \in DOMAIN y.cval: y.cval[k] = x)
    []   y.ctype = "dict" -> HBool(x \in DOMAIN y.cval)
    []   y.ctype = "str"  ->
            LET xn == Len(x.cval)
                yn == Len(y.cval)
            IN
                HBool(\E i \in 0..(yn - xn): 
                    x.cval = SubSeq(y.cval, i+1, i+xn))

\* Concatenate n copies of list
ListTimes(list, n) ==
    LET card == Len(list.cval)
    IN
        HList([ x \\in 1..(n.cval * card) |-> list.cval[((x - 1) % card) + 1] ])

\* Multiply two integers, or concatenate copies of a list
FunMult(e1, e2) ==
    CASE e1.ctype = "int" /\\ e2.ctype = "int" ->
        HInt(e2.cval * e1.cval)
    [] e1.ctype = "int" /\\ e2.ctype = "list" ->
        ListTimes(e2, e1)
    [] e1.ctype = "list" /\\ e2.ctype = "int" ->
        ListTimes(e1, e2)

\* By Harmony rules, if there are two conflicting key->value1 and key->value2
\* mappings, the higher values wins.
InsertMap(map, key, value) ==
    [ x \\in (DOMAIN map) \\union {key} |->
        IF x = key
        THEN
            IF x \\in DOMAIN map
            THEN
                IF HCmp(value, map[x]) > 0
                THEN
                    value
                ELSE
                    map[x]
            ELSE
                value
        ELSE
            map[x]
    ]

\* Push the current context onto the stack.  Pop the top "()" of the stack first.
OpGetContext(self) == 
    LET next  == [self EXCEPT !.pc = @ + 1,
                        !.stack = << HContext(self) >> \\o Tail(@)]
    IN
        /\\ Head(self.stack) = EmptyDict
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Pops a value, a key, and a dict, and pushes the dict updated to
\* reflect key->value.
OpDictAdd(self) ==
    LET value == self.stack[1]
        key   == self.stack[2]
        dict  == self.stack[3]
        newd  == HDict(InsertMap(dict.cval, key, value))
        next  == [self EXCEPT !.pc = @ + 1,
            !.stack = << newd >> \\o Tail(Tail(Tail(@)))]
    IN
        /\\ dict.ctype = "dict"
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Pop a value and a list, and a dict, and pushes a new list with the
\* value appended.
OpListAdd(self) ==
    LET value == self.stack[1]
        list  == self.stack[2]
        newl  == HList(Append(list.cval, value))
        next  == [self EXCEPT !.pc = @ + 1,
            !.stack = << newl >> \\o Tail(Tail(@))]
    IN
        /\\ list.ctype = "list"
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Push Harmony constant c onto the stack.
OpPush(self, c) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.stack = << c >> \\o @]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Pop the top of the stack and store in the shared variable pointed to
\* by the sequence v of Harmony values that acts as an address
OpStore(self, v) ==
    LET next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
    IN
        /\\ Assert(self.readonly = 0, "Store in readonly mode")
        /\\ UpdateContext(self, next)
        /\\ shared' = UpdateDirAddr(shared, v, Head(self.stack))

\* Pop a value and an address and store the value at the given address
OpStoreInd(self) ==
    LET val  == self.stack[1]
        addr == self.stack[2]
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(Tail(@))]
    IN
        /\\ Assert(self.readonly = 0, "StoreInd in readonly mode")
        /\\ addr.ctype = "address"
        /\\ addr.cval.func = HPc(-1)
        /\\ UpdateContext(self, next)
        /\\ shared' = UpdateDirAddr(shared, addr.cval.args, val)

\* Pop a value and an address and store the *local* value at the given address
OpStoreVarInd(self) ==
    LET val  == self.stack[1]
        addr == self.stack[2]
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(Tail(@)),
                                    !.vs = UpdateDirAddr(@, addr.cval.args, val)]
    IN
        /\\ addr.ctype = "address"
        /\\ addr.cval.func = HPc(-2)
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Call method pc.
OpApply(self, pc) ==
    LET arg  == self.stack[1]
        next == [self EXCEPT !.pc = pc, !.stack = <<
                arg,
                "apply",
                self.pc,
                <<>>
            >> \\o Tail(@)]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Pop an address.  If the arguments are empty, push the function and
\* continue to the next instruction.  If not, push the arguments except
\* the first and evaluate the function with the first argument.
OpLoadInd(self) ==
    LET addr == Head(self.stack).cval
        func == CASE addr.func = HPc(-1) -> shared
               []   addr.func = HPc(-2) -> self.vs
               []   OTHER               -> addr.func
        args == addr.args
    IN
        IF args = <<>>
        THEN
            LET next == [self EXCEPT !.pc = @ + 1, !.stack = <<func>> \\o Tail(@)]
            IN
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared
        ELSE
            LET arg == Head(args) IN
            CASE func.ctype = "pc" ->
                LET next == [self EXCEPT !.pc = func.cval, !.stack = <<
                            arg,
                            "normal",
                            self.pc,
                            Tail(args)
                        >> \\o Tail(@)]
                IN
                    /\\ UpdateContext(self, next)
                    /\\ UNCHANGED shared
            [] func.ctype = "list" ->
                LET next == [self EXCEPT !.stack =
                        << Address(func.cval[arg.cval+1], Tail(args)) >> \\o Tail(@)]
                IN
                    /\\ arg.ctype = "int"
                    /\\ UpdateContext(self, next)
                    /\\ UNCHANGED shared
            [] func.ctype = "dict" ->
                LET next == [self EXCEPT !.stack =
                        << Address(func.cval[arg], Tail(args)) >> \\o Tail(@)]
                IN
                    /\\ UpdateContext(self, next)
                    /\\ UNCHANGED shared
            [] func.ctype = "str" ->
                LET char == SubSeq(func.cval, arg.cval+1, arg.cval+1)
                    next == [self EXCEPT !.stack =
                        << Address(HStr(char), Tail(args)) >> \\o Tail(@)]
                IN
                    /\\ arg.ctype = "int"
                    /\\ UpdateContext(self, next)
                    /\\ UNCHANGED shared

\* Pop an address and push the value of the addressed local variable onto the stack
\* TODO.  THIS IS OBSOLETE
OpLoadVarInd(self) ==
    LET
        addr == Head(self.stack)
        val  == LoadDirAddr(self.vs, addr)
        next == [self EXCEPT !.pc = @ + 1, !.stack = <<val>> \\o Tail(@)]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Push the value of shared variable v onto the stack.
OpLoad(self, v) ==
    LET next == [ self EXCEPT !.pc = @ + 1, !.stack = << shared.cval[v] >> \o @ ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Return the context and the given parameter
OpSave(self) ==
    LET valu == Head(self.stack)
        intm == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
        m1   == InsertMap(EmptyFunc, HInt(0), valu)
        m2   == InsertMap(m1, HInt(1), intm)
        next == [intm EXCEPT !.stack = << HDict(m2) >> \\o @]
    IN
        /\\ self.atomic > 0
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Store the context at the pushed address (unless it is None or ()) and
\* remove it from the  context bag and active set.  Make all contexts in
\* the context bag
OpStopInd(self) ==
    LET addr == Head(self.stack)
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(@)]
    IN
        /\\ addr.ctype = "address"
        /\\ addr.cval.func = HPc(-1)
        /\\ self.atomic > 0
        /\\ RemoveContext(self)
        /\\ IF addr = None \\/ addr = EmptyDict
            THEN
                UNCHANGED shared
            ELSE
                shared' = UpdateDirAddr(shared, addr.cval.args, HContext(next))

\* What Return should do depends on whether the methods was spawned,
\* called as an ordinary method, or as an interrupt handler.  To indicate
\* this, Spawn pushes the string "process" on the stack, OpLoadInd pushes
\* the string "normal", and an interrupt pushes the string "interrupt".
\* The Frame operation also pushed the saved variables which must be restored.
OpReturnVar(self, var) ==
    LET savedvars == self.stack[1]
        calltype  == self.stack[2]
    IN
        CASE calltype = "normal" ->
            LET raddr  == self.stack[3]
                args   == self.stack[4]
                result == self.vs.cval[HStr(var)]
                next == [ self EXCEPT
                            !.pc = raddr,
                            !.vs = savedvars,
                            !.stack = << Address(result, args) >> \\o Tail(Tail(Tail(Tail(@))))
                        ]
                IN
                    /\\ UpdateContext(self, next)
                    /\\ UNCHANGED shared
        [] calltype = "apply" ->
            LET raddr  == self.stack[3]
                args   == self.stack[4]
                result == self.vs.cval[HStr(var)]
                next == [ self EXCEPT
                            !.pc = raddr + 1,
                            !.vs = savedvars,
                            !.stack = << result >> \o Tail(Tail(Tail(Tail(@))))
                        ]
                IN
                    /\ args = <<>>
                    /\ UpdateContext(self, next)
                    /\ UNCHANGED shared
        [] calltype = "interrupt" ->
            LET raddr == self.stack[3]
                next == [ self EXCEPT
                            !.pc = raddr,
                            !.interruptLevel = FALSE,
                            !.vs = savedvars,
                            !.stack = Tail(Tail(Tail(@)))
                        ]
            IN
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared
        [] calltype = "process" ->
            /\\ ctxbag' = ctxbag (-) SetToBag({self})
            /\\ IF self.atomic > 0
               THEN active' = DOMAIN ctxbag'
               ELSE active' = active \\ { self }
            /\\ UNCHANGED shared

\* Version of OpReturnVar where result is on stack instead of in variable
OpReturn(self) ==
    LET result    == self.stack[1]
        savedvars == self.stack[2]
        calltype  == self.stack[3]
    IN
        CASE calltype = "normal" ->
            LET raddr  == self.stack[4]
                args   == self.stack[5]
                next == [ self EXCEPT
                            !.pc = raddr,
                            !.vs = savedvars,
                            !.stack = << Address(result, args) >> \\o Tail(Tail(Tail(Tail(Tail(@)))))
                        ]
                IN
                    /\\ UpdateContext(self, next)
                    /\\ UNCHANGED shared
        [] calltype = "apply" ->
            LET raddr  == self.stack[4]
                args   == self.stack[5]
                next == [ self EXCEPT
                            !.pc = raddr + 1,
                            !.vs = savedvars,
                            !.stack = << result >> \o Tail(Tail(Tail(Tail(Tail(@)))))
                        ]
                IN
                    /\ args = <<>>
                    /\ UpdateContext(self, next)
                    /\ UNCHANGED shared
        [] calltype = "interrupt" ->
            LET raddr == self.stack[4]
                next == [ self EXCEPT
                            !.pc = raddr,
                            !.interruptLevel = FALSE,
                            !.vs = savedvars,
                            !.stack = Tail(Tail(Tail(Tail(@))))
                        ]
            IN
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared
        [] calltype = "process" ->
            /\\ ctxbag' = ctxbag (-) SetToBag({self})
            /\\ IF self.atomic > 0
               THEN active' = DOMAIN ctxbag'
               ELSE active' = active \\ { self }
            /\\ UNCHANGED shared

\* Version of OpReturnVar with a default value
OpReturnVarDefault(self, var, deflt) ==
    LET savedvars == self.stack[1]
        calltype  == self.stack[2]
    IN
        CASE calltype = "normal" ->
            LET raddr  == self.stack[3]
                args   == self.stack[4]
                result == IF HStr(var) \\in DOMAIN self.vs.cval THEN self.vs.cval[HStr(var)] ELSE deflt
                next == [ self EXCEPT
                            !.pc = raddr,
                            !.vs = savedvars,
                            !.stack = << Address(result, args) >> \\o Tail(Tail(Tail(Tail(@))))
                        ]
                IN
                    /\\ UpdateContext(self, next)
                    /\\ UNCHANGED shared
        [] calltype = "apply" ->
            LET raddr  == self.stack[3]
                args   == self.stack[4]
                result == IF HStr(var) \\in DOMAIN self.vs.cval THEN self.vs.cval[HStr(var)] ELSE deflt
                next == [ self EXCEPT
                            !.pc = raddr + 1,
                            !.vs = savedvars,
                            !.stack = << result >> \o Tail(Tail(Tail(Tail(@))))
                        ]
                IN
                    /\ args = <<>>
                    /\ UpdateContext(self, next)
                    /\ UNCHANGED shared
        [] calltype = "interrupt" ->
            LET raddr == self.stack[3]
                next == [ self EXCEPT
                            !.pc = raddr,
                            !.interruptLevel = FALSE,
                            !.vs = savedvars,
                            !.stack = Tail(Tail(Tail(@)))
                        ]
            IN
                /\\ UpdateContext(self, next)
                /\\ UNCHANGED shared
        [] calltype = "process" ->
            /\\ ctxbag' = ctxbag (-) SetToBag({self})
            /\\ IF self.atomic > 0
               THEN active' = DOMAIN ctxbag'
               ELSE active' = active \\ { self }
            /\\ UNCHANGED shared

\* Set the program counter pc to the given value
OpJump(self, pc) ==
    LET next == [ self EXCEPT !.pc = pc ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Pop a value of the stack.  If it equals cond, set the pc to the
\* given value.
OpJumpCond(self, pc, cond) ==
    LET next == [ self EXCEPT !.pc = IF Head(self.stack) = cond
                    THEN pc ELSE (@ + 1), !.stack = Tail(@) ]
    IN
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Spawn a new thread.  If the current thread is not atomic, the
\* thread goes into the active set as well.
OpSpawn(self) ==
    LET local == self.stack[1]
        arg   == self.stack[2]
        entry == self.stack[3]
        next  == [self EXCEPT !.pc = @ + 1, !.stack = Tail(Tail(Tail(@)))]
        newc  == InitContext(entry.cval, 0, arg)
    IN
        /\\ entry.ctype = "pc"
        /\\ IF self.atomic > 0
           THEN active' = (active \\ { self }) \\union { next }
           ELSE active' = (active \\ { self }) \\union { next, newc }
        /\\ ctxbag' = (ctxbag (-) SetToBag({self})) (+) SetToBag({next,newc})
        /\\ UNCHANGED shared

\* Operation to set a trap.
OpTrap(self) ==
    LET entry == self.stack[1]
        arg   == self.stack[2]
        next  == [self EXCEPT !.pc = @ + 1, !.stack = Tail(Tail(@)),
                                        !.trap = << entry.cval, arg >>]
    IN
        /\\ entry.ctype = "pc"
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

\* Restore a context that is pushed on the stack.  Also push the argument
\* onto the restored context's stack
\* TODO.  Currently arg and ctx are in the wrong order
OpGo(self) ==
    LET ctx  == self.stack[1]
        arg  == self.stack[2]
        next == [self EXCEPT !.pc = @ + 1, !.stack = Tail(Tail(@))]
        newc == [ctx.cval EXCEPT !.stack = << arg >> \o @]
    IN
        /\\ IF self.atomic > 0
            THEN active' = (active \\ { self }) \\union { next }
            ELSE active' = (active \\ { self }) \\union { next,newc }
        /\\ ctxbag' = (ctxbag (-) SetToBag({self})) (+) SetToBag({next,newc})
        /\\ UNCHANGED shared

\* When there are no threads left, the Idle action kicks in
Idle ==
    /\\ active = {}
    /\\ UNCHANGED allvars
"""

def tla_translate(f, code, scope):
    print(tladefs, file=f)
    first = True
    for pc in range(len(code.labeled_ops)):
        if first:
            print("Step(self) == ", end="", file=f)
            first = False
        else:
            print("              ", end="", file=f)
        print("\\/ self.pc = %d /\\ "%pc, end="", file=f)
        print(code.labeled_ops[pc].op.tladump(), file=f)
    print("""
Interrupt(self) ==
    LET next == [ self EXCEPT !.pc = self.trap[1],
                    !.stack = << self.trap[2], "interrupt", self.pc >> \o @,
                    !.interruptLevel = TRUE, !.trap = <<>> ]
    IN
        /\\ self.trap # <<>>
        /\\ ~self.interruptLevel
        /\\ UpdateContext(self, next)
        /\\ UNCHANGED shared

Next == (\\E self \\in active: Step(self) \\/ Interrupt(self)) \\/ Idle
Spec == Init /\\ [][Next]_allvars

THEOREM Spec => []TypeInvariant
THEOREM Spec => [](active \subseteq (DOMAIN ctxbag))
THEOREM Spec => ((active = {}) => [](active = {}))
\* THEOREM Spec => []<>(active = {})
================""", file=f)

def tex_output(f, code, scope):
    tex_main(f, code, scope)
