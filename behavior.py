import sys
import getopt
import json
from pydot import Dot, Edge, Node
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA

def dfadump(dfa):
    rename = {}
    for i, s in enumerate(dfa.states):
        rename[s] = "{}" if s == "{}" else str(i)
    print("states", { rename[s] for s in dfa.states }, file=sys.stderr)
    for (s, d) in dfa.transitions.items():
        print(rename[s], ":", file=sys.stderr)
        for t, s2 in d.items():
            print("   ", t, ":", rename[s2], file=sys.stderr)

def show_diagram(dfa, path=None):
    graph = Dot(graph_type='digraph', rankdir='LR')
    nodes = {}
    for state in dfa.states:
        if state == "{}":
            continue
        if state == dfa.initial_state:
            # color start state with green
            if state in dfa.final_states:
                initial_state_node = Node(
                    state,
                    style='filled',
                    peripheries=2,
                    fillcolor='#66cc33', label="initial")
            else:
                initial_state_node = Node(
                    state, style='filled', fillcolor='#66cc33', label="initial")
            nodes[state] = initial_state_node
            graph.add_node(initial_state_node)
        else:
            if state in dfa.final_states:
                state_node = Node(state, peripheries=2, label="final")
            else:
                state_node = Node(state, label="")
            nodes[state] = state_node
            graph.add_node(state_node)
    # adding edges
    for from_state, lookup in dfa.transitions.items():
        for to_label, to_state in lookup.items():
            if to_state != '{}' and (from_state != to_state or to_label != ""):
                graph.add_edge(Edge(
                    nodes[from_state],
                    nodes[to_state],
                    label=to_label
                ))
    if path:
        graph.write_png(path)
    return graph

def parse(js, outfmt, minify):
    states = set()
    initial_state = None;
    final_states = set()
    input_symbols = set()
    transitions = {}

    for s in js["nodes"]:
        idx = str(s["idx"])
        transitions[idx] = {}
        if s["type"] == "initial":
            assert initial_state == None
            initial_state = idx;
            val = "__init__"
        elif s["type"] == "terminal":
            final_states.add(idx)
        states.add(idx)

    for edge in js['edges']:
        src = str(edge["src"])
        dst = str(edge["dst"])
        if edge["log"] != "":
            input_symbols.add(edge["log"])
        assert dst != initial_state
        assert src not in final_states
        val = edge["log"]
        if val in transitions[src]:
            transitions[src][val].add(dst)
        else:
            transitions[src][val] = {dst}

    # print("states", states, file=sys.stderr)
    # print("final", final_states, file=sys.stderr)
    # print("symbols", input_symbols, file=sys.stderr)
    # print("transitions", transitions, file=sys.stderr)

    nfa = NFA(
        states=set(states),
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states
    )

    print("NFA -> DFA", file=sys.stderr)
    intermediate = DFA.from_nfa(nfa)  # returns an equivalent DFA
    print("NFA -> DFA done %d"%len(intermediate.states), file=sys.stderr)

    # TODO.  Minifying the DFA can lead to results where not all incoming
    #        edges to a node are labeled the same and other stuff.
    if minify:
        print("minify", file=sys.stderr)
        dfa = intermediate.minify(retain_names = True)
        print("minify done %d"%len(dfa.states), file=sys.stderr)
    else:
        dfa = intermediate

    # dfadump(dfa)

    show_diagram(dfa, path='./dfa1.png')

    if False:
        # Give each state a simple integer name
        names = {}
        values = {}
        for (idx, s) in enumerate(dfa.states):
            names[s] = idx
            values[s] = "???"
        values[dfa.initial_state] = "initial"

        if outfmt == "dot":
            print("digraph {")

            for s in dfa.states:
                if s == "{}":
                    continue
                if s in dfa.final_states:
                    if s == dfa.initial_state:
                        print("  s%s [label=\"%s\",shape=doubleoctagon]"%(names[s], "initial"))
                    else:
                        print("  s%s [label=\"%s\",shape=doublecircle]"%(names[s], "final"))
                elif s == dfa.initial_state:
                    print("  s%s [label=\"%s\",shape=octagon]"%(names[s], "initial"))
                else:
                    print("  s%s [label=\"%s\",shape=circle]"%(names[s], ""))

            for (src, edges) in dfa.transitions.items():
                for (input, dst) in edges.items():
                    if dst != '{}' and (src != dst or input != ""):
                        print("  s%s -> s%s [label=%s]"%(names[src], names[dst], json.dumps(input)))

            print("}")
        else:       # json format, same as input
            assert outfmt == "json"
            print("{")
            print("  \"nodes\": [")

            first = True
            for s in dfa.states:
                if s == "{}":
                    continue
                if first:
                    first = False
                else:
                    print(",")
                print("    {")
                print("      \"idx\": \"%s\","%names[s])
                print("      \"value\": \"%s\","%values[s])
                if s == dfa.initial_state:
                    t = "initial"
                elif s in dfa.final_states:
                    t = "final"
                else:
                    t = "normal"
                print("      \"type\": \"%s\""%t)
                print("    }", end="")
            print()
            print("  ],")

            print("  \"edges\": [")
            first = True
            for (src, edges) in dfa.transitions.items():
                for (input, dst) in edges.items():
                    if dst != '{}' and src != dst:
                        if first:
                            first = False
                        else:
                            print(",")
                        print("    {")
                        print("      \"src\": \"%s\","%names[src])
                        print("      \"dst\": \"%s\""%names[dst])
                        print("    }", end="")
            print()
            print("  ]")

            print("}")

def usage():
    print("Usage: iface [-T type] [-M] file.json", file=sys.stderr)
    sys.exit(1)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "MT:",
                ["type=", "minify", "help"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    outfmt = "dot"
    minify = False
    for o, a in opts:
        if o in [ "-T", "--type"]:
            if a not in [ "dot", "json" ]:
                print("type must be dot or json", file=sys.stderr)
                sys.exit(1)
            outfmt = a
        elif o in [ "-M", "--minify" ]:
            minify = True
        else:
            usage()

    if args == []:
        usage()

    file = args[0]
    with open(file) as f:
        js = json.load(f)
        parse(js, outfmt, minify);

if __name__ == "__main__":
    main()
