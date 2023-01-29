import sys
import getopt
import json
from typing import Dict, Optional, Set
from automata.fa.nfa import NFA # type: ignore
from automata.fa.dfa import DFA # type: ignore

# Helper type aliases
Transitions = Dict[str, Dict[str, Set[str]]]

def dfadump(dfa):
    rename = {}
    for i, s in enumerate(dfa.states):
        rename[s] = "{}" if s == "{}" else str(i)
    print("states", { rename[s] for s in dfa.states }, file=sys.stderr)
    for (s, d) in dfa.transitions.items():
        print(rename[s], ":", file=sys.stderr)
        for t, s2 in d.items():
            print("   ", t, ":", rename[s2], file=sys.stderr)

# Get rid of choose states
def dechoose(states, transitions, choose_states):
    print("dechoose", file=sys.stderr)
    for (k, v) in states.items():
        if k in choose_states:
            # See what incoming nodes k has
            incoming = set()
            for k2 in states:
                if v in transitions[k2] and k in transitions[k2][v]:
                    incoming.add(k2)
            for k2 in incoming:
                # remove the existing transition from the incoming node
                transitions[k2][v].remove(k)
                if transitions[k2][v] == set():
                    del transitions[k2][v]

                # distribute each outgoing edge among the incoming node
                for (v2, s) in transitions[k].items():
                    for out in s:
                        if k2 != out:
                            if v2 in transitions[k2]:
                                transitions[k2][v2].add(out)
                            else:
                                transitions[k2][v2] = { out }

    for k in choose_states:
        del states[k]
        del transitions[k]

# Get rid of stutter transitions
def destutter(states: Dict[str, str], transitions: Transitions):
    print("destutter", len(states), file=sys.stderr)

    # figure out for each state what other states point to it
    pointsto: Dict[str, Set[str]] = { k:set() for k in states }
    for src in states:
        for (v, s) in transitions[src].items():
            for dst in s:
                pointsto[dst].add(src)

    updated = set()
    for (k, v) in states.items():
        # See if state k has an outgoing edge with its value
        if v in transitions[k]:
            # See what incoming nodes k has
            incoming = set()
            for k2 in pointsto[k]:
                if v in transitions[k2]:
                    assert k in transitions[k2][v]
                    incoming.add(k2)
            # distribute each outgoing edge among the incoming nodes
            for out in transitions[k][v]:
                for k2 in incoming:
                    if k2 != out:
                        transitions[k2][v].add(out)
                        pointsto[k].add(k2)

            # remove the outgoing edges
            del transitions[k][v]

            updated.add(k)

    if updated == set():
        return False

    # Remove states with no outgoing edges
    for src in states:
        for v in transitions[src]:
            toremove = set()
            for dst in transitions[src][v]:
                if transitions[dst] == {}:
                    toremove.add(dst)
            if toremove != set():
                transitions[src][v] -= toremove
    for k in updated:
        if transitions[k] == {}:
            del states[k]
            del transitions[k]

    return True

def parse(js, outfmt, minify):
    states: Dict[str, str] = {}
    initial_state: Optional[str] = None
    final_states: Set[str] = set()
    choose_states: Set[str] = set()
    input_symbols = { "__term__" }
    transitions: Transitions = {}

    for s in js["nodes"]:
        idx = str(s["idx"])
        val = str(s["value"])
        input_symbols.add(val)
        transitions[idx] = {}
        if s["type"] == "initial":
            assert initial_state is None
            initial_state = idx
            val = "__init__"
        elif s["type"] == "terminal":
            final_states.add(idx)
        elif s["type"] == "choose" and int(s["choosing_atomic_level"]) > 0:
            choose_states.add(idx)
        states[idx] = val

    for edge in js['edges']:
        src = str(edge["src"])
        dst = str(edge["dst"])
        assert dst != initial_state
        assert src not in final_states
        if src != dst:
            if dst in final_states:
                val = "__term__"
            else:
                val = states[dst]
            if val in transitions[src]:
                transitions[src][val].add(dst)
            else:
                transitions[src][val] = {dst}

    dechoose(states, transitions, choose_states)

    while destutter(states, transitions):
        pass

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
    for (i, s) in enumerate(dfa.states):
        names[s] = i
        values[s] = "???"
    values[dfa.initial_state] = "initial"

    # Figure out the value of each of the states
    for (src, edges) in dfa.transitions.items():
        for (input, dst) in edges.items():
            if dst != '{}' and src != dst:
                values[dst] = input

    if outfmt == "dot":
        print("digraph {")

        for s in dfa.states:
            if s == "{}":
                continue
            if s == dfa.initial_state:
                print("  s%s [label=\"%s\",shape=octagon]"%(names[s], values[s]))
            elif s in dfa.final_states:
                print("  s%s [label=\"%s\",shape=doubleoctagon]"%(names[s], values[s]))
            else:
                print("  s%s [label=\"%s\",shape=box]"%(names[s], values[s]))

        for (src, edges) in dfa.transitions.items():
            for (input, dst) in edges.items():
                if dst != '{}' and src != dst:
                    print("  s%s -> s%s"%(names[src], names[dst]))

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
    with open(file, encoding='utf-8') as f:
        js = json.load(f)
        parse(js, outfmt, minify);

if __name__ == "__main__":
    main()
