// Charm can input a DFA or ("Harmony Finite Automaton) to check if some
// model has output behaviors that correspond to the output behaviors of
// another model (usually corresponding to some specification).

#include "head.h"

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "value.h"
#include "hashdict.h"
#include "json.h"
#include "dfa.h"

static int int_parse(char *p, int len){
    char *copy = malloc(len + 1);
    memcpy(copy, p, len);
    copy[len] = 0;
    int v = atoi(copy);
    free(copy);
    return v;
}

// read a DFA from a json file
struct dfa *dfa_read(struct allocator *allocator, char *fname){
    // open the HFA file
    FILE *fp = fopen(fname, "r");
    if (fp == NULL) {
        fprintf(stderr, "charm: can't open %s\n", fname);
        return NULL;
    }

    // read the entire file
    json_buf_t buf;
    buf.base = malloc(CHUNKSIZE);
    buf.len = 0;
    int n;
    while ((n = fread(&buf.base[buf.len], 1, CHUNKSIZE, fp)) > 0) {
        buf.len += n;
        buf.base = realloc(buf.base, buf.len + CHUNKSIZE);
    }
    fclose(fp);

    // parse the contents
    struct json_value *jv = json_parse_value(&buf);
    assert(jv->type == JV_MAP);

    struct dfa *dfa = new_alloc(struct dfa);

    // get the initial state
    struct json_value *initial = dict_lookup(jv->u.map, "initial", 7);
    assert(initial->type == JV_ATOM);
    dfa->initial = int_parse(initial->u.atom.base, initial->u.atom.len);
    // printf("INITIAL %d\n", dfa->initial);

    // read the list of states
    struct json_value *nodes = dict_lookup(jv->u.map, "nodes", 5);
    assert(nodes->type == JV_LIST);
    unsigned int max_idx = 0;
    struct dfa_state *states = NULL;
    for (unsigned int i = 0; i < nodes->u.list.nvals; i++) {
        struct json_value *node = nodes->u.list.vals[i];
        assert(node->type == JV_MAP);

        struct dfa_state *ds = new_alloc(struct dfa_state);

        struct json_value *idx = dict_lookup(node->u.map, "idx", 3);
        assert(idx->type == JV_ATOM);
        ds->idx = int_parse(idx->u.atom.base, idx->u.atom.len);
        if (ds->idx > max_idx) {
            max_idx = ds->idx;
        }

        struct json_value *type = dict_lookup(node->u.map, "type", 4);
        assert(type->type == JV_ATOM);
        assert(type->u.atom.len > 0);
        ds->final = type->u.atom.base[0] == 'f';

        // printf("IDX %d %d\n", ds->idx, ds->final);
        ds->next = states;
        states = ds;
    }

    dfa->nstates = max_idx + 1;
    dfa->states = calloc(sizeof(dfa->states[0]), dfa->nstates);
    for (unsigned int i = 0; i < dfa->nstates; i++) {
        dfa->states[i].idx = -1;            // some may not be used
    }
    struct dfa_state *ds;
    while ((ds = states) != NULL) {
        states = ds->next;
        dfa->states[ds->idx] = *ds;
    }

    // read the list of symbols
    struct json_value *symbols = dict_lookup(jv->u.map, "symbols", 7);
    assert(symbols->type == JV_LIST);
    unsigned int symalloc = 100;     // allocated size of symbol list
    dfa->symbols = malloc(symalloc * sizeof(hvalue_t));
    for (unsigned int i = 0; i < symbols->u.list.nvals; i++) {
        struct json_value *symbol = symbols->u.list.vals[i];
        assert(symbol->type == JV_MAP);
        if (dfa->nsymbols == symalloc) {
            symalloc *= 2;
            dfa->symbols = realloc(dfa->symbols, symalloc * sizeof(hvalue_t));
        }
        dfa->symbols[dfa->nsymbols++] = value_from_json(allocator, symbol->u.map);
    }

    // read the list of edges
    struct json_value *edges = dict_lookup(jv->u.map, "edges", 5);
    assert(edges->type == JV_LIST);
    dfa->nedges = edges->u.list.nvals;
    dfa->edges = malloc(dfa->nedges * sizeof(*dfa->edges));
    for (unsigned int i = 0; i < edges->u.list.nvals; i++) {
        struct json_value *edge = edges->u.list.vals[i];
        assert(edge->type == JV_MAP);

        struct dfa_transition *dt = new_alloc(struct dfa_transition);
        dt->index = i;
        dfa->edges[i] = dt;

        struct json_value *src = dict_lookup(edge->u.map, "src", 3);
        assert(src->type == JV_ATOM);
        unsigned int src_state = int_parse(src->u.atom.base, src->u.atom.len);
        assert(src_state < dfa->nstates);

        struct json_value *dst = dict_lookup(edge->u.map, "dst", 3);
        assert(dst->type == JV_ATOM);
        dt->dst = int_parse(dst->u.atom.base, dst->u.atom.len);
        assert(dt->dst < dfa->nstates);

        struct json_value *symbol = dict_lookup(edge->u.map, "sym", 3);
        assert(symbol->type == JV_ATOM);
        unsigned int sym = int_parse(symbol->u.atom.base, symbol->u.atom.len);
        assert(sym < dfa->nsymbols);
        dt->symbol = dfa->symbols[sym];

        dt->next = dfa->states[src_state].transitions;
        dfa->states[src_state].transitions = dt;

        // printf("EDGE %d %d %s\n", src_state, dt->dst, value_string(dt->symbol));
    }

    json_value_free(jv);
    return dfa;
}

// get the initial state
int dfa_initial(struct dfa *dfa){
    return dfa->initial;
}

// check if the state is terminal
bool dfa_is_final(struct dfa *dfa, int state){
    return dfa->states[state].final;
}

// make a step.  Returns transition id.  Return -1 upon error.
int dfa_step(struct dfa *dfa, int current, hvalue_t symbol){
    struct dfa_state *ds = &dfa->states[current];

    // TODO.  Maybe make symbol lookup a hashmap
    for (struct dfa_transition *dt = ds->transitions; dt != NULL; dt = dt->next) {
        if (dt->symbol == symbol) {
            return dt->index;
        }
    }
    return -1;
}

int dfa_visited(struct dfa *dfa, int current, hvalue_t symbol){
    struct dfa_state *ds = &dfa->states[current];

    for (struct dfa_transition *dt = ds->transitions; dt != NULL; dt = dt->next) {
        if (dt->symbol == symbol) {
            return dt->cnt;
        }
    }
    return -1;
}

int potential_recurse(struct dfa *dfa, bool *visited, int current){
    if (visited[current]) {
        return -1;
    }
    visited[current] = true;
    struct dfa_state *ds = &dfa->states[current];
    for (struct dfa_transition *dt = ds->transitions; dt != NULL; dt = dt->next) {
        if (dt->cnt == 0) {
            return 0;
        }
        int r = potential_recurse(dfa, visited, dt->dst);
        if (r != -1) {
            return r;
        }
    }
    return -1;
}

// See if there are any "potential" transitions reachable
// after taking the step according to symbol
int dfa_potential(struct dfa *dfa, int current, hvalue_t symbol){
    bool *visited = calloc(dfa->nstates, sizeof(bool));
    struct dfa_state *ds = &dfa->states[current];

    visited[current] = true;

    // First see where this takes us
    for (struct dfa_transition *dt = ds->transitions; dt != NULL; dt = dt->next) {
        if (dt->symbol == symbol) {
            if (dt->cnt == 0) {
                free(visited);
                return 0;
            }
            int r = potential_recurse(dfa, visited, dt->dst);
            free(visited);
            return r;
        }
    }
    free(visited);
    return -1;
}

void dfa_dump(struct dfa *dfa){
    printf("%u/%u edges visited\n", dfa->cnt, dfa->nedges);
    printf("%u transitions made\n", dfa->total);
}
