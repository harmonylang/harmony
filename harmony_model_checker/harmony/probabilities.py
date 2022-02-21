from collections import defaultdict
import numpy as np

# TODO: This is just a simple port of charmpp. We probably want extended
# functionality here.
def find_probabilities(top, states, outputfiles):
    transitions = defaultdict(list)
    total_states = top['total_states']
    matrix = np.zeros((total_states, total_states))
    for p in top['probabilities']:
        assert p['probability']['denominator'] != 0
        assert p['probability']['numerator'] != 0
        matrix[p['from']][p['to']] = p['probability']['numerator'] / p['probability']['denominator']
        transitions[p['from']].append(p['to'])
    print(transitions)

    states = set(int(s.strip()) for s in states.split(","))

    reachable_states = []
    list_b = []
    for i in range(total_states):
        if i in states:
            continue
        if is_reachable(i, transitions, states):
            reachable_states.append(i)
            list_b.append(np.sum(matrix[i][list(states)]))

    reachable_states = np.array(reachable_states)
    matrix_a = np.identity(len(reachable_states)) - matrix[np.ix_(reachable_states, reachable_states)]
    probabilities = np.linalg.solve(matrix_a, list_b)

    if outputfiles['hpo'] is not None:
        np.savetxt(outputfiles['hpo'], np.stack((reachable_states, probabilities), axis=1), delimiter=",")


"""
Try to reach states in `goal` from state
"""
def is_reachable(state, transitions, goals):
    # TODO: There might be more efficient ways to search this, I just ported
    # this since this was in the original implementation
    visited = set()

    def search(s):
        print(s)
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
