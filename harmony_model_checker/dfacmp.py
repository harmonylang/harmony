import sys
import json
from typing import Dict, Optional
from automata.fa.dfa import DFA # type: ignore

from harmony_model_checker.iface import Transitions_t

def parse(file):
    with open(file, encoding='utf-8') as f:
        js = json.load(f)

        states = { "__error__": '' }
        initial_state: Optional[str] = None
        final_states = set()
        input_symbols = set()
        transitions: Dict[str, Dict[str, str]] = { "__error__": {} }

        for s in js["nodes"]:
            idx = str(s["idx"])
            val = str(s["value"])
            input_symbols.add(val)
            transitions[idx] = {}
            if s["type"] == "initial":
                assert initial_state is None
                initial_state = idx
            elif s["type"] == "terminal":
                final_states.add(idx)
            states[idx] = val

        for s in states:
            for x in input_symbols:
                transitions[s][x] = "__error__"

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
                transitions[src][val] = dst

    return DFA(
        states=set(states.keys()),
        input_symbols=input_symbols,
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states
    )

def main():
    print("DFA1")
    dfa1 = parse(sys.argv[1])
    print("DFA2")
    dfa2 = parse(sys.argv[2])
    print("CMP")
    assert dfa1 <= dfa2
    print("DONE")

if __name__ == "__main__":
    main()
