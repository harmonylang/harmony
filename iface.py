import sys
import json
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA

def parse(js):
    states = {}
    initial_state = None;
    final_states = set()
    input_symbols = { "__term__" }
    transitions = {}

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
            initial_state = idx;
        elif s["type"] == "terminal":
            final_states.add(idx)
        states[idx] = val

    for edge in js['edges']:
        src = str(edge["src"])
        dst = str(edge["dst"])
        if dst in final_states:
            val = "__term__"
        else:
            val = states[dst]
        if (val in transitions[src]):
            transitions[src][val].add(dst)
        else:
            transitions[src][val] = {dst}

    # print("states", states)
    # print("final", final_states)
    # print("symbols", input_symbols)
    # print("transitions", transitions)

    nfa = NFA(
        states=set(states.keys()),
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states
    )

    dfa = DFA.from_nfa(nfa)  # returns an equivalent DFA

    # dfa.show_diagram(path='./dfa1.png')
    # sys.exit(0)

    print()

    # Give each state a simple integer name
    names = {}
    values = {}
    for (idx, s) in enumerate(dfa.states):
        names[s] = idx
        values[s] = "???"
    values[dfa.initial_state] = "initial"

    # Figure out the value of each of the states
    for (src, edges) in dfa.transitions.items():
        for (input, dst) in edges.items():
            if dst != '{}' and src != dst:
                values[dst] = input

    print("digraph {")

    # Find Harmony initial states

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

def main():
    file = sys.argv[1]
    with open(file) as f:
        js = json.load(f)
        parse(js);

if __name__ == "__main__":
    main()
