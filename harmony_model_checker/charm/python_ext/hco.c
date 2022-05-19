#include "hco.h"
#include "charm.h"

struct symbol_env_t {
    PyObject* symbol_obj;
};

void* insert_symbols(void *env, const void *key, unsigned int key_size, void *value) {
    struct symbol_env_t *se = env;
    const hvalue_t *symbol = key;

    assert(key_size == sizeof(*symbol));
    char *p = value_json(*symbol);
    const PyObject* obj = se->symbol_obj;

    PyDict_SetItemString(obj, itoa((uint64_t) value), p);
}

PyObject* create_symbols(struct dict *symbols) {
    PyObject* symbols = PyDict_New();

    struct symbol_env_t se = {.symbol_obj = symbols};
    dict_iter(symbols, insert_symbols, &se);
    return symbols;
}

static void print_trans_upcall(void *env, const void *key, unsigned int key_size, void *value){
    struct print_trans_env *pte = env;
    const hvalue_t *log = key;
    unsigned int nkeys = key_size / sizeof(hvalue_t);
    struct strbuf *sb = value;

    if (pte->first) {
        pte->first = false;
    }
    else {
        fprintf(pte->out, ",\n");
    }
    fprintf(pte->out, "        [[");
    for (unsigned int i = 0; i < nkeys; i++) {
        void *p = dict_lookup(pte->symbols, &log[i], sizeof(log[i]));
        assert(p != NULL);
        if (i != 0) {
            fprintf(pte->out, ",");
        }
        fprintf(pte->out, "%"PRIu64, (uint64_t) p);
    }
    fprintf(pte->out, "],[%s]]", strbuf_getstr(sb));
    strbuf_deinit(sb);
    free(sb);
}

PyObject* create_transitions(struct dict *symbols, struct edge *edges){
    PyObject* transitions = PyList_New(10);
    for (struct edge *e = edges; e != NULL; e = e->fwdnext) {
        hvalue_t *log = e->log;
        unsigned int node_id = e->dst->id;

        void *p = dict_lookup(symbols, log, sizeof(log));
        assert(p != NULL);
    }
    return transitions;
}

PyObject* create_hco(int no_issues, struct global_t *global) {
    const PyObject* hco = PyDict_New();
    if (no_issues) {
        PyDict_SetItemString(hco, "issue", "No issues");

        destutter1(&global->graph);

        // Output the symbols;
        struct dict *symbols = collect_symbols(&global->graph);
        PyDict_SetItemString(hco, "symbol", create_symbols(symbols));

        const PyObject* nodes_list = PyList_New(global->graph.size);
        for (unsigned int i = 0; i < global->graph.size; i++) {
            struct node *node = global->graph.nodes[i];
            assert(node->id == i);
            if (node->reachable) {
                PyObject *node_obj = PyDict_New();
                PyDict_SetItemString(node_obj, "idx", node->id);
                PyDict_SetItemString(node_obj, "component", node->component);

                PyDict_SetItemString(node_obj,
                    "transitions", create_transitions(symbols, node->fwd));
                if (i == 0) {
                    PyDict_SetItemString(node_obj, "type", "initial");
                }
                else if (node->final) {
                    PyDict_SetItemString(node_obj, "type", "terminal");
                }
                else {
                    PyDict_SetItemString(node_obj, "type", "normal");
                }
            }
        }
    } else {
        // Find shortest "bad" path
        struct failure *bad = NULL;
        if (minheap_empty(global->failures)) {
            bad = minheap_getmin(warnings);
        }
        else {
            bad = minheap_getmin(global->failures);
        }

        switch (bad->type) {
        case FAIL_SAFETY:
            printf("Safety Violation\n");
            PyDict_SetItemString(hco, "issue", "Safety violation");
            break;
        case FAIL_INVARIANT:
            printf("Invariant Violation\n");
            PyDict_SetItemString(hco, "issue", "Invariant violation");
            break;
        case FAIL_BEHAVIOR:
            printf("Behavior Violation: terminal state not final\n");
            PyDict_SetItemString(hco, "issue", "Behavior violation: terminal state not final");
            break;
        case FAIL_TERMINATION:
            printf("Non-terminating state\n");
            PyDict_SetItemString(hco, "issue", "Non-terminating state");
            break;
        case FAIL_BUSYWAIT:
            printf("Active busy waiting\n");
            PyDict_SetItemString(hco, "issue", "Active busy waiting");
            break;
        case FAIL_RACE:
            assert(bad->address != VALUE_ADDRESS);
            char *addr = value_string(bad->address);
            char *json = json_string_encode(addr, strlen(addr));
            printf("Data race (%s)\n", json);
            PyDict_SetItemString(hco, "issue", sprintf("Data race (%s)", json));
            free(addr);
            break;
        default:
            printf("main: bad fail type\n");
            return hco;
        }

        fprintf(out, "  \"macrosteps\": [");
        struct state oldstate;
        memset(&oldstate, 0, sizeof(oldstate));
        struct context *oldctx = calloc(1, sizeof(*oldctx));
        global->dumpfirst = true;
        path_dump(global, out, bad->node, bad->parent, bad->choice, &oldstate, &oldctx, bad->interrupt, bad->node->steps);
        fprintf(out, "\n");
        free(oldctx);
        fprintf(out, "  ],\n");
    }
}
