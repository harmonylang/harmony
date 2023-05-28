import subprocess
import sys
import json
from typing import Any, Dict, List, Optional, Set, Tuple

from harmony_model_checker.harmony.jsonstring import json_string
from harmony_model_checker.iface import Transitions_t

try:
    import pydot  # type: ignore
    got_pydot = True
except Exception as e:
    got_pydot = False

try:
    from automata.fa.nfa import NFA  # type: ignore
    from automata.fa.dfa import DFA  # type: ignore
    got_automata = True
except Exception as e:
    got_automata = False


# an error state is a non-final state all of whose outgoing transitions
# point only to itself
def find_error_states(transitions, final_states):
    error_states = set()
    for s, d in transitions.items():
        if s not in final_states and all(v == s for v in d.values()):
            error_states.add(s)
    return error_states

def is_dfa_equivalent(dfa: DFA, hfa: DFA) -> bool:
    stack: List[Tuple[int, int]] = []

    # Create states, where each state is renamed to an index to make each state unique
    dfa_states = [(k, v) for k, v in enumerate(list(dfa.states))]
    hfa_states = [(len(dfa_states) + k, v) for k, v in enumerate(list(hfa.states))]
    states = dfa_states + hfa_states
    n = len(states)

    # For convenience for mapping between states and indices
    idx_to_states = {k: v for k, v in states}
    dfa_state_to_idx = {v: k for k, v in dfa_states}
    hfa_state_to_idx = {v: k for k, v in hfa_states}

    dfa_final_states = {k: v for k, v in dfa_states if v in dfa.final_states}
    hfa_final_states = {k: v for k, v in hfa_states if v in hfa.final_states}
    # Collection of final states, indexed by state idx
    final_states = {**dfa_final_states, **hfa_final_states}

    # Tree-implementation of sets of states
    parents: List[int] = [0] * n
    rank: List[int] = [0] * n
    def make_set(q: int):
        parents[q] = q
        rank[q] = 0

    # Create a set for each state in the 2 DFAs
    for k, _ in states:
        make_set(k)

    def find_set(x):
        if x != parents[x]:
            parents[x] = find_set(parents[x])
        return parents[x]

    def link(x: int, y: int):
        if rank[x] > rank[y]:
            parents[y] = x
        else:
            parents[x] = y
            if rank[x] == rank[y]:
                rank[y] += 1

    def union(p: int, q: int):
        link(find_set(p), find_set(q))

    # Union the two initial states
    dfa_init_idx = dfa_state_to_idx[dfa.initial_state]
    hfa_init_idx = hfa_state_to_idx[hfa.initial_state]
    union(dfa_init_idx, hfa_init_idx)
    stack.append((dfa_init_idx, hfa_init_idx))

    # Traverse the stack
    while stack:
        k1, k2 = stack.pop()
        q1, q2 = idx_to_states[k1], idx_to_states[k2]
        dfa_t = dfa.transitions[q1]
        hfa_t = hfa.transitions[q2]

        # Check each common transitions
        symbols = set(dfa_t.keys()).intersection(hfa_t.keys())
        for s in symbols:
            p1 = dfa_state_to_idx[dfa_t[s]]
            p2 = hfa_state_to_idx[hfa_t[s]]

            r1 = find_set(p1)
            r2 = find_set(p2)
            # If their sets are not equivalent, then combine them
            if r1 != r2:
                union(p1, p2)
                stack.append((p1, p2))

    # Create sets of sets of states
    sets: Dict[int, set] = dict()
    for k, p in enumerate(parents):
        if p in sets:
            sets[p].add(k)
        else:
            sets[p] = {k}

    # Check condition for DFA equivalence
    return all(
        all(q in final_states for q in s) or all(q not in final_states for q in s)
        for s in sets.values()
    )


def read_hfa(file, dfa, nfa):
    with open(file, encoding='utf-8') as fd:
        js = json.load(fd, strict=False)
        initial = js["initial"]
        states = { "{}" }
        final = set()
        symbols = set()
        for e in js["edges"]:
            symbol = e["sym"]
            symbols.add(json_string(js["symbols"][symbol]))
        transitions = { "{}": { s: "{}" for s in symbols } }
        for n in js["nodes"]:
            idx: str = n["idx"]
            states.add(idx)
            if n["type"] == "final":
                final.add(idx)
            transitions[idx] = { s: "{}" for s in symbols }
        for e in js["edges"]:
            symbol = e["sym"]
            transitions[e["src"]][json_string(js["symbols"][symbol])] = e["dst"]

    hfa = DFA(
        states=states,
        input_symbols=symbols,
        transitions=transitions,
        initial_state=initial,
        final_states=final
    )

    print("Phase 7: comparing behaviors", len(dfa.states), len(hfa.states))
    if len(dfa.states) == len(hfa.states):      # HACK
        return                                  # HACK
    if len(dfa.states) > 100 or len(hfa.states) > 100:
        print("  warning: this could take a while")

    assert dfa.input_symbols <= hfa.input_symbols
    if dfa.input_symbols < hfa.input_symbols:
        print("behavior warning: symbols missing from behavior:",
            hfa.input_symbols - dfa.input_symbols)
        return

    if not is_dfa_equivalent(dfa, hfa):
        print("behavior warning: subset of specified behavior")
        diff = hfa - dfa
        behavior_show_diagram(diff, "diff.png")

# Modified from automata-lib
def behavior_show_diagram(dfa: DFA, path=None):
    graph = pydot.Dot(graph_type='digraph', rankdir='LR')
    nodes = {}
    rename: Dict[str, int] = {}
    next_idx = 0
    error_states = find_error_states(dfa.transitions, dfa.final_states)
    for state in dfa.states:
        if state in rename:
            idx = rename[state]
        else:
            rename[state] = idx = next_idx
            next_idx += 1
        if state in error_states:
            continue
        if state == dfa.initial_state:
            # color start state with green
            if state in dfa.final_states:
                initial_state_node = pydot.Node(
                    str(idx),
                    style='filled',
                    peripheries=2,
                    fillcolor='#66cc33', label="initial")
            else:
                initial_state_node = pydot.Node(
                    str(idx), style='filled', fillcolor='#66cc33', label="initial")
            nodes[state] = initial_state_node
            graph.add_node(initial_state_node)
        else:
            if state in dfa.final_states:
                state_node = pydot.Node(str(idx), peripheries=2, label="final")
            else:
                state_node = pydot.Node(str(idx), label="")
            nodes[state] = state_node
            graph.add_node(state_node)
    # adding edges
    for from_state, lookup in dfa.transitions.items():
        for to_label, to_state in lookup.items():
            if to_state not in error_states and to_label != "":
                graph.add_edge(pydot.Edge(
                    nodes[from_state],
                    nodes[to_state],
                    label=to_label
                ))
    if path:
        try:
            graph.write_png(path)
        except FileNotFoundError:
            print("install graphviz (www.graphviz.org) to see output DFAs")
    return graph

def eps_closure_rec(states: Set[str], transitions: Transitions_t, current: str, output: Set[str]):
    if current in output:
        return
    output.add(current)
    t = transitions[current]
    if '' in t:
        for s in t['']:
            eps_closure_rec(states, transitions, s, output)

def eps_closure(states: Set[str], transitions: Transitions_t, current: str):
    x: Set[str] = set()
    eps_closure_rec(states, transitions, current, x)
    return frozenset(x)

def behavior_parse(js, minify, outputfiles, behavior):
    if outputfiles["hfa"] is None and outputfiles["png"] is None and outputfiles["gv"] is None and behavior is None:
        return
    minify = outputfiles["png"] is not None or outputfiles["gv"] is not None

    states: Set[str] = set()
    initial_state = None
    final_states = set()
    transitions: Transitions_t = {}
    labels = {}

    for s in js["nodes"]:
        idx = str(s["idx"])
        transitions[idx] = {}
        if s["type"] == "initial":
            assert initial_state is None
            initial_state = idx
            val = "__init__"
        elif s["type"] == "terminal":
            final_states.add(idx)
        states.add(idx)
    assert initial_state is not None
    if len(final_states) == 0:
        final_states = { initial_state }

    def add_edge(src, val, dst):
        assert dst != initial_state
        # assert src not in final_states
        if val in transitions[src]:
            transitions[src][val].add(dst)
        else:
            transitions[src][val] = {dst}

    intermediate = 0
    symbols = js['symbols']
    input_symbols = { json_string(v) for v in symbols.values() }
    labels = { json_string(v):v for v in symbols.values() }
    for s in js['nodes']:
        for [path, dsts] in s["transitions"]:
            for dest_node in dsts:
                src = str(s["idx"])
                dst = str(dest_node)
                if path == []:
                    add_edge(src, "", dst)
                else:
                    for e in path[:-1]:
                        symbol = json_string(symbols[str(e)])
                        inter = "s%d"%intermediate
                        intermediate += 1
                        states.add(inter)
                        transitions[inter] = {}
                        add_edge(src, symbol, inter)
                        src = inter
                    e = path[-1]
                    symbol = json_string(symbols[str(e)])
                    add_edge(src, symbol, dst)

    # print("states", states)
    # print("initial", initial_state)
    # print("final", final_states)
    # print("symbols", input_symbols)
    # print("transitions", transitions)

    if len(states) > 1:
        print("Phase 6: convert NFA (%d states) to DFA"%len(states))

    if got_automata:
        nfa = NFA(
            states=states,
            input_symbols=input_symbols,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states
        )
        intermediate_dfa = DFA.from_nfa(nfa)  # returns an equivalent DFA
        if minify and len(final_states) != 0:
            if len(intermediate_dfa.states) > 1: 
                print("minify #states=%d"%len(intermediate_dfa.states))
            dfa = intermediate_dfa.minify(retain_names = True)
            if len(dfa.states) > 1: 
                print("minify done #states=%d"%len(dfa.states))
        else:
            dfa = intermediate_dfa
        dfa_states = dfa.states
        (dfa_transitions,) = dfa.transitions,
        dfa_initial_state = dfa.initial_state
        dfa_final_states = dfa.final_states
    else:
        # Compute the epsilon closure for each state
        eps_closures = { s:eps_closure(states, transitions, s) for s in states }

        # Convert the NFA into a DFA
        dfa_transitions = {}
        dfa_initial_state = eps_closures[initial_state]
        q = [dfa_initial_state]       # queue of states to handle
        while q != []:
            current = q.pop()
            if current in dfa_transitions:
                continue
            dfa_transitions[current] = {}
            for symbol in input_symbols:
                ec = set()
                for nfa_state in current:
                    if symbol in transitions[nfa_state]:
                        for next in transitions[nfa_state][symbol]:
                            ec |= eps_closures[next]
                n = dfa_transitions[current][symbol] = frozenset(ec)
                q.append(n)
        dfa_states = set(dfa_transitions.keys())
        dfa_final_states = set()
        for dfa_state in dfa_states:
            for nfa_state in dfa_state:
                if nfa_state in final_states:
                    dfa_final_states.add(dfa_state)
        print("conversion done")
    dfa_error_states = find_error_states(dfa_transitions, dfa_final_states)

    if outputfiles["hfa"] is not None:
        with open(outputfiles["hfa"], "w", encoding='utf-8') as fd:
            names = {}
            for (i, s) in enumerate(dfa_states):
                names[s] = i
            print("{", file=fd)
            print("  \"initial\": \"%s\","%names[dfa_initial_state], file=fd)
            print("  \"nodes\": [", file=fd)
            first = True
            for s in dfa_states:
                if s in dfa_error_states:
                    continue
                if first:
                    first = False
                else:
                    print(",", file=fd)
                print("    {", file=fd, end="")
                print(" \"idx\": \"%s\","%names[s], file=fd, end="")
                if s in dfa_final_states:
                    t = "final"
                else:
                    t = "normal"
                print(" \"type\": \"%s\""%t, file=fd, end="")
                print(" }", end="", file=fd)
            print(file=fd)
            print("  ],", file=fd)

            # Assign a small integer to each symbol
            sym2index = {}
            index2sym = {}
            for i, v in enumerate(labels):
                sym2index[v] = i
                index2sym[i] = v

            first = True
            print("  \"symbols\": [", file=fd)
            for i in range(len(index2sym)):
                if first:
                    first = False
                else:
                    print(",", file=fd)
                print("    %s"%json.dumps(labels[index2sym[i]], ensure_ascii=False), file=fd, end="")
            print(file=fd)
            print("  ],", file=fd)

            print("  \"edges\": [", file=fd)
            first = True
            for (src, edges) in dfa_transitions.items():
                for (input, dst) in edges.items():
                    if dst not in dfa_error_states:
                        if first:
                            first = False
                        else:
                            print(",", file=fd)
                        print("    {", file=fd, end="")
                        print(" \"src\": \"%s\","%names[src], file=fd, end="")
                        print(" \"dst\": \"%s\","%names[dst], file=fd, end="")
                        print(" \"sym\": %d"%sym2index[input], file=fd, end="")
                        print(" }", end="", file=fd)
            print(file=fd)
            print("  ]", file=fd)

            print("}", file=fd)

    if outputfiles["gv"] is not None:
        with open(outputfiles["gv"], "w", encoding='utf-8') as fd:
            names = {}
            for (i, s) in enumerate(dfa_states):
                names[s] = i
            print("digraph {", file=fd)
            print("  rankdir = \"LR\"", file=fd)
            for s in dfa_states:
                if s in dfa_error_states:
                    continue
                if s == dfa_initial_state:
                    if s in dfa_final_states:
                        print("  s%s [label=\"initial\",style=filled,peripheries=2,fillcolor=\"#66cc33\"]"%names[s], file=fd)
                    else:
                        print("  s%s [label=\"initial\",style=filled,fillcolor=\"#66cc33\"]"%names[s], file=fd)
                else:
                    if s in dfa_final_states:
                        print("  s%s [peripheries=2,label=\"final\"]"%names[s], file=fd)
                    else:
                        print("  s%s [label=\"\"]"%names[s], file=fd)

            for (src, edges) in dfa_transitions.items():
                for (input, dst) in edges.items():
                    if dst not in dfa_error_states:
                        print("  s%s -> s%s [label=%s]"%(names[src], names[dst], json.dumps(input, ensure_ascii=False)), file=fd)
            print("}", file=fd)

    if outputfiles["png"] is not None:
        if got_pydot and got_automata:
            behavior_show_diagram(dfa, path=outputfiles["png"])
        else:
            assert outputfiles["gv"] is not None
            try:
                subprocess.run(["dot", "-Tpng", "-o", outputfiles["png"],
                                outputfiles["gv"] ])
            except FileNotFoundError:
                print("install graphviz (www.graphviz.org) to see output DFAs")

    if behavior is not None:
        if got_automata:
            read_hfa(behavior, dfa, nfa)
        else:
            print("Can't check behavior subset because automata-lib is not available")
