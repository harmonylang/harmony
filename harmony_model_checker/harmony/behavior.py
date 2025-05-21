import subprocess
import sys
import json
from typing import Any, Dict, List, Optional, Set, Tuple
from threading import Thread
from harmony_model_checker.harmony.jsonstring import json_string

def python_obj(js):
    type = js["type"]
    assert type in { "bool", "int", "atom", "list", "set", "dict" }, js
    v = js["value"]
    if type in { "bool", "int", "atom" }:
        return v
    if type == "list":
        return [ python_obj(val) for val in v ]
    if type == "set":
        return { python_obj(val) for val in v }
    if type == "dict":
        return { python_obj(js["key"]):python_obj(js["value"]) for js in v }
    assert False

try:
    import pydot  # type: ignore
    got_pydot = True
except Exception as e:
    got_pydot = False

def read_hfa_file(file):
    try:
        with open(file, encoding='utf-8') as fd:
            js = json.load(fd, strict=False)
            initial = js["initial"]
            states = set()
            final = set()
            symbols = set()
            for e in js["edges"]:
                symbol = e["sym"]
                symbols.add(json_string(js["symbols"][symbol]))
            transitions = {}
            for n in js["nodes"]:
                idx: str = n["idx"]
                states.add(idx)
                if n["type"] == "final":
                    final.add(idx)
                transitions[idx] = {}
            for e in js["edges"]:
                symbol = e["sym"]
                x = js["symbols"][symbol]
                transitions[e["src"]][json_string(x)] = (x, e["dst"])
        return (states, symbols, transitions, initial, final)
    except IOError:
        return False

# Modified from automata-lib
def behavior_show_diagram(dfa, path=None):
    (states, symbols, transitions, initial_state, final_states) = dfa
    error_states = set()

    graph = pydot.Dot(graph_type='digraph', rankdir='LR')
    nodes = {}
    rename: Dict[str, int] = {}
    next_idx = 0
    for state in states:
        if state in rename:
            idx = rename[state]
        else:
            rename[state] = idx = next_idx
            next_idx += 1
        if state in error_states:
            continue
        if state == initial_state:
            # color start state with green
            if state in final_states:
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
            if state in final_states:
                state_node = pydot.Node(str(idx), peripheries=2, label="final")
            else:
                state_node = pydot.Node(str(idx), label="")
            nodes[state] = state_node
            graph.add_node(state_node)
    # adding edges
    for from_state, lookup in transitions.items():
        for to_label, (to_sym, to_state) in lookup.items():
            if to_state not in error_states and to_label != "":
                assert to_sym["type"] == "list"
                attrs = python_obj(to_sym["value"][1])
                attrs["src"] = nodes[from_state];
                attrs["dst"] = nodes[to_state];
                attrs["label"] = json_string(to_sym["value"][0])
                graph.add_edge(pydot.Edge(**attrs))
    if path:
        try:
            graph.write_png(path)
        except FileNotFoundError:
            print("install graphviz (www.graphviz.org) to see output DFAs")
    return graph

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

    (dfa_states, dfa_symbols, dfa_transitions, dfa_initial_state, dfa_final_states) = dfa
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
                for (input, (sym, dst)) in edges.items():
                    if dst not in dfa_error_states:
                        assert sym["type"] == "list"
                        label = json_string(sym["value"][0])
                        attrs = python_obj(sym["value"][1])
                        flat = ",".join(["%s=%s"%(k,v) for k,v in attrs.items()])
                        if "color" in attrs:
                            print("  s%s -> s%s [label=%s,%s]"%(names[src], names[dst], json.dumps(label, ensure_ascii=False), flat), file=fd)
                        else:
                            print("  s%s -> s%s [label=%s]"%(names[src], names[dst], json.dumps(label, ensure_ascii=False)), file=fd)
            print("}", file=fd)

    if outputfiles["png"] is not None:
        if len(dfa_states) > 250:
            print("    * output of png file suppressed (too many states)") 
        else:
            if got_pydot:
                behavior_show_diagram(dfa, path=outputfiles["png"])
            else:
                print("    * running dot", len(dfa_states))
                assert outputfiles["gv"] is not None
                try:
                    subprocess.run(["dot", "-Tpng", "-o", outputfiles["png"],
                                    outputfiles["gv"] ])
                except FileNotFoundError:
                    print("install graphviz (www.graphviz.org) to see output DFAs")
