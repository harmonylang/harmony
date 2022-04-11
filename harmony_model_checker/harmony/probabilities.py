from collections import defaultdict
import math
import numpy as np
import json

# TODO: This is just a simple port of charmpp. We probably want extended
# functionality here.
def find_probabilities(top, outputfiles, code, scope):
    if outputfiles['hpo'] is None:
        return

    states = defaultdict(list)

    for o in top["filter_states"]:
        states[o['query']].append(o['state'])

    transitions = defaultdict(list)
    total_states = top['total_states']
    matrix = np.zeros((total_states, total_states))
    for p in top['probabilities']:
        assert p['probability']['denominator'] != 0
        assert p['probability']['numerator'] != 0
        matrix[p['from']][p['to']] = p['probability']['numerator'] / p['probability']['denominator']
        transitions[p['from']].append(p['to'])
    # print(transitions)

    ret = []

    # TODO: Make this more clear instead of using an arbitary id
    for i in range(len(code.hypers)):
        s = set(states[i])

        if i not in states:
            got_prob = 0
        else:
            got_prob = gen_prob(s, total_states, transitions, matrix).get(0, 0.0)

        if code is not None:
            try:
                # This might throw an error, because it is an arbitary harmony
                # expression. Might want to change this in the future.
                expected_prob = eval(code.hypers[i][2][1])
            except SyntaxError:
                print("WARNING: Cannot eval expected value for assertion {code.hypers[i][0][0]} in {code.hypers[i][0][1]}, {code.hypers[i][0][2]}, {code.hypers[i][0][3]}. Ignoring.")
            
            if code.hypers[i][2][0] == "==" and not math.isclose(got_prob, expected_prob):
                print(
                    f"WARNING: Expected probabiliity {expected_prob} for assertion "
                    f"{code.hypers[i][0][0]} in {code.hypers[i][0][1]}, "
                    f"{code.hypers[i][0][2]}:{code.hypers[i][0][3]} but got "
                    f"{got_prob}"
                )
            elif code.hypers[i][2][0] == "!=" and math.isclose(got_prob, expected_prob):
                print(
                    "WARNING: Expected probabiliity not be equal to "
                    f"{expected_prob} for assertion {code.hypers[i][0][0]} in "
                    f"{code.hypers[i][0][1]}, {code.hypers[i][0][2]}:"
                    f"{code.hypers[i][0][3]} but got {got_prob}"
                )
            elif code.hypers[i][2][0] == "<" and (math.isclose(got_prob, expected_prob) or got_prob > expected_prob):
                print(
                    "WARNING: Expected probabiliity to be less than "
                    f"{expected_prob} for assertion {code.hypers[i][0][0]} in "
                    f"{code.hypers[i][0][1]}, {code.hypers[i][0][2]}:"
                    f"{code.hypers[i][0][3]} but got {got_prob}"
                )
            elif code.hypers[i][2][0] == ">" and (math.isclose(got_prob, expected_prob) or got_prob < expected_prob):
                print(
                    "WARNING: Expected probabiliity to be larger than "
                    f"{expected_prob} for assertion {code.hypers[i][0][0]} in "
                    f"{code.hypers[i][0][1]}, {code.hypers[i][0][2]}:"
                    f"{code.hypers[i][0][3]} but got {got_prob}"
                )
            elif code.hypers[i][2][0] == "<=" and (not math.isclose(got_prob, expected_prob) and got_prob > expected_prob):
                print(
                    "WARNING: Expected probabiliity to be less than or equal to "
                    f"{expected_prob} for assertion {code.hypers[i][0][0]} in "
                    f"{code.hypers[i][0][1]}, {code.hypers[i][0][2]}:"
                    f"{code.hypers[i][0][3]} but got {got_prob}"
                )
            elif code.hypers[i][2][0] == ">=" and (not math.isclose(got_prob, expected_prob) and got_prob < expected_prob):
                print(
                    "WARNING: Expected probabiliity to be larger or equal to "
                    f"{expected_prob} for assertion {code.hypers[i][0][0]} in "
                    f"{code.hypers[i][0][1]}, {code.hypers[i][0][2]}:"
                    f"{code.hypers[i][0][3]} but got {got_prob}"
                )

            ret.append({
                "assertion": code.hypers[i][0][0],
                "file": code.hypers[i][0][1],
                "line": code.hypers[i][0][2],
                "column": code.hypers[i][0][3],
                "probability": got_prob,
            })
        else:
            ret.append(got_prob)

    with open(outputfiles['hpo'], 'w') as f:
        json.dump({"probabilities": ret}, f, indent=2)


def gen_prob(states, total_states, transitions, matrix):
    reachable_states = []
    list_b = []

    for i in range(total_states):
        if i in states:
            continue
        if is_reachable(i, transitions, states):
            reachable_states.append(i)
            list_b.append(np.sum(matrix[i][list(states)]))

    if not reachable_states:
        return {}

    reachable_states = np.array(reachable_states)
    print(reachable_states)
    matrix_a = np.identity(len(reachable_states)) - matrix[np.ix_(reachable_states, reachable_states)]
    print(matrix_a, list_b)
    probabilities = np.linalg.solve(matrix_a, list_b)

    # print(reachable_states, probabilities)
    return dict(zip(reachable_states, probabilities))


"""
Try to reach states in `goal` from state
"""
def is_reachable(state, transitions, goals):
    # TODO: There might be more efficient ways to search this, I just ported
    # this since this was in the original implementation
    visited = set()

    def search(s):
        if s in goals:
            return True
        if s in visited:
            return False
        visited.add(s)
        for i in transitions[s]:
            if (search(i)):
                return True
        return False
        
    return search(state)
