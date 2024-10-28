import subprocess
import sys
import json
from typing import Any, Dict, List, Optional, Set, Tuple
from threading import Thread

from harmony_model_checker.harmony.jsonstring import json_string
from harmony_model_checker.iface import Transitions_t

try:
    import pydot  # type: ignore
    got_pydot = True
except Exception as e:
    got_pydot = False

try:
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

def read_hfa_file(file):
    try:
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
        return DFA(
            states=states,
            input_symbols=symbols,
            transitions=transitions,
            initial_state=initial,
            final_states=final
        )
    except IOError:
        return False

def compare_behaviors(file, dfa):
    # TODO.  The following code can use read_hfa_file() I believe
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

# minified_dfa = None
#
# def do_minify(intermediate_dfa):
#     global minified_dfa
#     minified_dfa = intermediate_dfa.minify(retain_names = True)

def behavior_parse(js, minify, outputfiles, behavior):
    if outputfiles["hfa"] is None and outputfiles["png"] is None and outputfiles["gv"] is None and behavior is None:
        return

    if "dfasize" in js and js["dfasize"] > 1024:
        print("    * too many states for post-analysis") 
        if outputfiles["png"] is not None:
            print("    * png output file suppressed") 
        elif outputfiles["gv"] is not None:
            print("    * gv output file suppressed") 
        return

    # minify = outputfiles["png"] is not None or outputfiles["gv"] is not None

    # Read the hfa file
    # TODO: only do this if there are not too many nodes
    if outputfiles["hfa"] is None:
        return
    dfa = read_hfa_file(outputfiles["hfa"])
    if not dfa:
        return

    """
    if got_automata and minify:
        intermediate_dfa = dfa
        if True or len(intermediate_dfa.states) > 100: 
            print("    * minify #states=%d"%len(intermediate_dfa.states))
        thread = Thread(target=do_minify, args=(intermediate_dfa,))
        thread.start()
        thread.join(15)
        if thread.is_alive():
            print("    * minify: taking too long and giving up (not fatal)")
        else:
            global minified_dfa
            dfa = minified_dfa
            if True or len(intermediate_dfa.states) > 100: 
                print("    * minify done #states=%d"%len(dfa.states))
    """
    dfa_states = dfa.states
    (dfa_transitions,) = dfa.transitions,
    dfa_initial_state = dfa.initial_state
    dfa_final_states = dfa.final_states
    dfa_error_states = set()

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
        if len(dfa.states) > 250:
            print("    * output of png file suppressed (too many states)") 
        else:
            if got_pydot and got_automata:
                behavior_show_diagram(dfa, path=outputfiles["png"])
            else:
                print("    * running dot", len(dfa.states))
                assert outputfiles["gv"] is not None
                try:
                    subprocess.run(["dot", "-Tpng", "-o", outputfiles["png"],
                                    outputfiles["gv"] ])
                except FileNotFoundError:
                    print("install graphviz (www.graphviz.org) to see output DFAs")

    if behavior is not None:
        if got_automata:
            if "suppressed" in js:
                print("behavior subset checking suppressed; use -b flag to enable")
            else:
                compare_behaviors(behavior, dfa)
        else:
            print("Can't check behavior subset because automata-lib is not available")
