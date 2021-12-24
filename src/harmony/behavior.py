def read_hfa(file, dfa):
    with open(file) as fd:
        js = json.load(fd)
        initial = js["initial"]
        states = { "{}" }
        final = set()
        symbols = set()
        for e in js["edges"]:
            symbol = json_string(e["symbol"])
            symbols.add(symbol)
        transitions = { "{}": { s: "{}" for s in symbols } }
        for n in js["nodes"]:
            idx = n["idx"]
            states.add(idx)
            if n["type"] == "final":
                final.add(idx)
            transitions[idx] = { s: "{}" for s in symbols }
        for e in js["edges"]:
            symbol = json_string(e["symbol"])
            transitions[e["src"]][symbol] = e["dst"]

    hfa = DFA(
        states=states,
        input_symbols=symbols,
        transitions=transitions,
        initial_state=initial,
        final_states=final
    )

    assert dfa.input_symbols <= hfa.input_symbols
    if dfa.input_symbols < hfa.input_symbols:
        print("behavior warning: symbols missing from behavior:",
            hfa.input_symbols - dfa.input_symbols)
    else:
        assert dfa <= hfa
        if dfa < hfa:
            print("behavior warning: strict subset of specified behavior")

# Modified from automata-lib
def behavior_show_diagram(dfa, path=None):
    graph = pydot.Dot(graph_type='digraph', rankdir='LR')
    nodes = {}
    rename = {}
    next_idx = 0
    for state in dfa.states:
        if state in rename:
            idx = rename[state]
        else:
            rename[state] = idx = next_idx
            next_idx += 1
        if state == "{}":
            continue
        if state == dfa.initial_state:
            # color start state with green
            if state in dfa.final_states:
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
            if state in dfa.final_states:
                state_node = pydot.Node(str(idx), peripheries=2, label="final")
            else:
                state_node = pydot.Node(str(idx), label="")
            nodes[state] = state_node
            graph.add_node(state_node)
    # adding edges
    for from_state, lookup in dfa.transitions.items():
        for to_label, to_state in lookup.items():
            if to_state != '{}' and to_label != "":
                graph.add_edge(pydot.Edge(
                    nodes[from_state],
                    nodes[to_state],
                    label=to_label
                ))
    if path:
        graph.write_png(path)
    return graph

error_state = "{}" if got_automata else frozenset({})

def eps_closure_rec(states, transitions, current, output):
    if current in output:
        return
    output.add(current)
    t = transitions[current]
    if '' in t:
        for s in t['']:
            eps_closure_rec(states, transitions, s, output)

def eps_closure(states, transitions, current):
    x = set()
    eps_closure_rec(states, transitions, current, x)
    return frozenset(x)

def behavior_parse(js, minify, outputfiles, behavior):
    if outputfiles["hfa"] == None and outputfiles["png"] == None and outputfiles["gv"] == None and behavior == None:
        return

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
    # print("initial", initial_state, file=sys.stderr)
    # print("final", final_states, file=sys.stderr)
    # print("symbols", input_symbols, file=sys.stderr)
    # print("transitions", transitions, file=sys.stderr)

    print("NFA -> DFA", file=sys.stderr)

    if got_automata:
        nfa = NFA(
            states=states,
            input_symbols=input_symbols,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states
        )
        intermediate = DFA.from_nfa(nfa)  # returns an equivalent DFA
        if minify and len(final_states) != 0:
            print("minify %d"%len(intermediate.states), file=sys.stderr)
            dfa = intermediate.minify(retain_names = True)
            print("minify done %d"%len(dfa.states), file=sys.stderr)
        else:
            dfa = intermediate
        dfa_states = dfa.states
        (dfa_transitions,) = dfa.transitions,
        dfa_initial_state = dfa.initial_state,
        dfa_final_states = dfa.final_states
    else:
        # Compute the epsilon closure for each state
        eps_closures = { s:eps_closure(states, transitions, s) for s in states }

        # Convert the NFA into a DFA
        dfa_transitions = {}
        dfa_initial_state = eps_closures[initial_state]
        q = [dfa_initial_state]       # queue of states to handle
        while q != []:
            current = q.pop()
            if current in dfa_transitions:
                continue
            dfa_transitions[current] = {}
            for symbol in input_symbols:
                ec = set()
                for nfa_state in current:
                    if symbol in transitions[nfa_state]:
                        for next in transitions[nfa_state][symbol]:
                            ec |= eps_closures[next]
                n = dfa_transitions[current][symbol] = frozenset(ec)
                q.append(n)
        dfa_states = set(dfa_transitions.keys())
        dfa_final_states = set()
        for dfa_state in dfa_states:
            for nfa_state in dfa_state:
                if nfa_state in final_states:
                    dfa_final_states.add(dfa_state)

    if outputfiles["hfa"] != None:
        with open(outputfiles["hfa"], "w") as fd:
            names = {}
            for (idx, s) in enumerate(dfa_states):
                names[s] = idx
            print("{", file=fd)
            print("  \"initial\": \"%s\","%names[dfa_initial_state], file=fd)
            print("  \"nodes\": [", file=fd)
            first = True
            for s in dfa_states:
                if s == error_state:
                    continue
                if first:
                    first = False
                else:
                    print(",", file=fd)
                print("    {", file=fd)
                print("      \"idx\": \"%s\","%names[s], file=fd)
                if s in dfa_final_states:
                    t = "final"
                else:
                    t = "normal"
                print("      \"type\": \"%s\""%t, file=fd)
                print("    }", end="", file=fd)
            print(file=fd)
            print("  ],", file=fd)

            print("  \"edges\": [", file=fd)
            first = True
            for (src, edges) in dfa_transitions.items():
                for (input, dst) in edges.items():
                    if dst != error_state:
                        if first:
                            first = False
                        else:
                            print(",", file=fd)
                        print("    {", file=fd)
                        print("      \"src\": \"%s\","%names[src], file=fd)
                        print("      \"dst\": \"%s\","%names[dst], file=fd)
                        print("      \"symbol\": %s"%json.dumps(labels[input]), file=fd)
                        print("    }", end="", file=fd)
            print(file=fd)
            print("  ]", file=fd)

            print("}", file=fd)

    if outputfiles["gv"] != None:
        with open(outputfiles["gv"], "w") as fd:
            names = {}
            for (idx, s) in enumerate(dfa_states):
                names[s] = idx
            print("digraph {", file=fd)
            print("  rankdir = \"LR\"", file=fd)
            for s in dfa_states:
                if s == error_state:
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
                for (input, dst) in edges.items():
                    if dst != error_state:
                        print("  s%s -> s%s [label=%s]"%(names[src], names[dst], json.dumps(input)), file=fd)
            print("}", file=fd)

    if outputfiles["png"] != None:
        if got_pydot and got_automata:
            behavior_show_diagram(dfa, path=outputfiles["png"])
        else:
            assert outputfiles["gv"] != None
            subprocess.run(["dot", "-Tpng", "-o", outputfiles["png"],
                                outputfiles["gv"] ])

    if behavior != None:
        if got_automata:
            read_hfa(behavior, dfa)
        else:
            print("Can't check behavior subset because automata-lib is not available")