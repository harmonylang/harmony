# Modified from automata-lib
def behavior_show_diagram(dfa, path=None):
    graph = pydot.Dot(graph_type='digraph', rankdir='LR')
    nodes = {}
    for state in dfa.states:
        if state == "{}":
            continue
        if state == dfa.initial_state:
            # color start state with green
            if state in dfa.final_states:
                initial_state_node = pydot.Node(
                    state,
                    style='filled',
                    peripheries=2,
                    fillcolor='#66cc33', label="initial")
            else:
                initial_state_node = pydot.Node(
                    state, style='filled', fillcolor='#66cc33', label="initial")
            nodes[state] = initial_state_node
            graph.add_node(initial_state_node)
        else:
            if state in dfa.final_states:
                state_node = pydot.Node(state, peripheries=2, label="final")
            else:
                state_node = pydot.Node(state, label="")
            nodes[state] = state_node
            graph.add_node(state_node)
    # adding edges
    for from_state, lookup in dfa.transitions.items():
        for to_label, to_state in lookup.items():
            if to_state != '{}' and (from_state != to_state or to_label != ""):
                graph.add_edge(pydot.Edge(
                    nodes[from_state],
                    nodes[to_state],
                    label=to_label
                ))
    if path:
        graph.write_png(path)
    return graph

def behavior_parse(js, minify, output):
    states = set()
    initial_state = None;
    final_states = set()
    input_symbols = set()
    transitions = {}
    labels = {}

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

    def add_edge(src, val, dst):
        assert dst != initial_state
        assert src not in final_states
        if val in transitions[src]:
            transitions[src][val].add(dst)
        else:
            transitions[src][val] = {dst}

    intermediate = 0
    for edge in js['edges']:
        src = str(edge["src"])
        dst = str(edge["dst"])
        if edge["print"] == []:
            add_edge(src, "", dst)
        else:
            for e in edge["print"][:-1]:
                symbol = json_string(e)
                input_symbols.add(symbol)
                labels[symbol] = e
                inter = "s%d"%intermediate
                intermediate += 1
                states.add(inter)
                transitions[inter] = {}
                add_edge(src, symbol, inter)
                src = inter
            e = edge["print"][-1]
            symbol = json_string(e)
            add_edge(src, symbol, dst)
            input_symbols.add(symbol)
            labels[symbol] = e

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

    # VOODOO constant warning: 200 is arbitrary, but minimization doesn't
    # scale so well and we don't really need it usually
    if minify and len(final_states) != 0 and len(states) < 200:
        print("minify %d"%len(intermediate.states), file=sys.stderr)
        dfa = intermediate.minify(retain_names = True)
        print("minify done %d"%len(dfa.states), file=sys.stderr)
    else:
        dfa = intermediate

    behavior_show_diagram(dfa, path=output + ".png")

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

    with open(output + ".hfa", "w") as fd:
        names = {}
        for (idx, s) in enumerate(dfa.states):
            names[s] = idx
        print("{", file=fd)
        print("  \"initial\": \"%s\""%names[dfa.initial_state], file=fd)
        print("  \"nodes\": [", file=fd)
        first = True
        for s in dfa.states:
            if s == "{}":
                continue
            if first:
                first = False
            else:
                print(",", file=fd)
            print("    {", file=fd)
            print("      \"idx\": \"%s\","%names[s], file=fd)
            if s in dfa.final_states:
                t = "final"
            else:
                t = "normal"
            print("      \"type\": \"%s\""%t, file=fd)
            print("    }", end="", file=fd)
        print(file=fd)
        print("  ],", file=fd)

        print("  \"edges\": [", file=fd)
        first = True
        for (src, edges) in dfa.transitions.items():
            for (input, dst) in edges.items():
                if dst != '{}':
                    if first:
                        first = False
                    else:
                        print(",", file=fd)
                    print("    {", file=fd)
                    print("      \"src\": \"%s\","%names[src], file=fd)
                    print("      \"dst\": \"%s\","%names[dst], file=fd)
                    print("      \"symbol\": %s"%labels[input], file=fd)
                    print("    }", end="", file=fd)
        print(file=fd)
        print("  ]", file=fd)

        print("}", file=fd)
