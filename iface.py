import sys
import json
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA

INITIAL = 0
NORMAL = 1
FINAL = 2

def parse(js):
    states = {}
    final_states = set()
    input_symbols = { "__start__", "__init__", "__term__" }
    transitions = { "__initial__": { "__start__": set() } }

    # Since an NFA and DFA are only allowed to have a single initial
    # state, I have created an initial state __initial__.  From that
    # initial state, there is a transition to each of the Harmony
    # initial states, labeled by the label of the initial state.
    # From each Harmony initial state there is a transition labeled
    # "__init__" to the first state after that initial state.  There
    # is a "__term__" transition to each final state.

    for s in js["nodes"]:
        idx = str(s["idx"])
        val = str(s["value"])
        input_symbols.add(val)
        transitions[idx] = {}
        if s["type"] == "initial":
            transitions["__initial__"][val] = {idx}
            transitions[idx]["__init__"] = set()
            states[idx] = (INITIAL, val)
        elif s["type"] == "terminal":
            final_states.add(idx)
            states[idx] = (FINAL, val)
        else:
            states[idx] = (NORMAL, val)

    for edge in js['edges']:
        src = str(edge["src"])
        dst = str(edge["dst"])
        (srctype, _) = states[src]
        (dsttype, val) = states[dst]
        if srctype == INITIAL:
            transitions[src]["__init__"].add(dst)
            label = "__init__"
        elif dsttype == FINAL:
            label = "__term__"
        else:
            label = val
        if (label in transitions[src]):
            transitions[src][label].add(dst)
        else:
            transitions[src][label] = {dst}

    # print("states", states)
    # print("final", final_states)
    # print("symbols", input_symbols)
    # print("transitions", transitions)

    nfa = NFA(
        states=states.keys() | { "__initial__" },
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state='__initial__',
        final_states=final_states
    )

    dfa = DFA.from_nfa(nfa)  # returns an equivalent DFA

    # dfa.show_diagram(path='./dfa1.png')

    print()

    # Give each state a simple integer name
    names = {}
    values = {}
    for (idx, s) in enumerate(dfa.states):
        names[s] = idx
        values[s] = "???"

    # Figure out the value of each of the states
    for (src, edges) in dfa.transitions.items():
        for (input, dst) in edges.items():
            if dst != '{}' and src != dst:
                values[dst] = input

    print("digraph {")

    # Find Harmony initial states
    initial_states = set()
    for (lab, dst) in dfa.transitions[dfa.initial_state].items():
        if dst != "{}":
            initial_states.add(dst)

    final_states = set()
    for final in dfa.final_states:
        final_states.add(final)

    for s in dfa.states:
        if s == dfa.initial_state or s == "{}":
            continue
        if s in initial_states:
            print("  s%s [label=\"%s\",shape=octagon]"%(names[s], values[s]))
        elif s in final_states:
            print("  s%s [label=\"%s\",shape=doubleoctagon]"%(names[s], values[s]))
        else:
            print("  s%s [label=\"%s\",shape=box]"%(names[s], values[s]))

    for (src, edges) in dfa.transitions.items():
        if src != dfa.initial_state:
            for (input, dst) in edges.items():
                if dst != '{}' and src != dst:
                    print("  s%s -> s%s"%(names[src], names[dst]))

    print("}")

def main():
    file = sys.argv[1]
    with open(file) as f:
        js = json.load(f)
        parse(js);

if __name__ == "__main__":
    main()
