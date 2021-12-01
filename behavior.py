import sys
import getopt
import json
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

def parse(js, outfmt, minify):
    states = {}
    initial_state = None;
    final_states = set()
    input_symbols = { "__term__" }
    transitions = {}

    for s in js["nodes"]:
        idx = str(s["idx"])
        val = str(s["value"])
        transitions[idx] = {}
        if s["type"] == "initial":
            assert initial_state == None
            initial_state = idx;
            val = "__init__"
        elif s["type"] == "terminal":
            final_states.add(idx)
        states[idx] = val

    for edge in js['edges']:
        src = str(edge["src"])
        dst = str(edge["dst"])
        input_symbols.add(edge["log"])
        assert dst != initial_state
        assert src not in final_states
        if src != dst:
            if dst in final_states:
                val = "__term__"
            else:
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
        states=set(states.keys()),
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states
    )

    intermediate = DFA.from_nfa(nfa)  # returns an equivalent DFA

    # TODO.  Minifying the DFA can lead to results where not all incoming
    #        edges to a node are labeled the same and other stuff.
    if minify:
        dfa = intermediate.minify()
    else:
        dfa = intermediate

    # dfadump(dfa)
    # sys.exit(0)

    # dfa.show_diagram(path='./dfa1.png')
    # sys.exit(0)

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
            if s == dfa.initial_state:
                print("  s%s [label=\"%s\",shape=octagon]"%(names[s], names[s]))
            elif s in dfa.final_states:
                print("  s%s [label=\"%s\",shape=doubleoctagon]"%(names[s], names[s]))
            else:
                print("  s%s [label=\"%s\",shape=box]"%(names[s], names[s]))

        for (src, edges) in dfa.transitions.items():
            for (input, dst) in edges.items():
                if dst != '{}':
                    print("  s%s -> s%s [label=\"%s\"]"%(names[src], names[dst], input))

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
