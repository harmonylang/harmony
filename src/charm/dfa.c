struct dfa_transition {
    struct dfa_transition *next; // linked list maintenance
    uint64_t symbol;             // transition symbol
    int dst;                     // destination state
    int idy;                     // unique id for transition
};

struct dfa_state {
    struct dfa_state *next;      // linked list maintenance
    int idx;                     // name of state
    bool final;                  // terminal state
    struct dfa_transition *transitions;     // transition map

    // TODO.  Maybe should make transitions a dict
};

struct dfa {
    int nstates, ntransitions;
    int initial;
    struct dfa_state *states;
};

static int int_parse(char *p, int len){
    char *copy = malloc(len + 1);
    memcpy(copy, p, len);
    copy[len] = 0;
    int v = atoi(copy);
    free(copy);
    return v;
}

// read a DFA from a json file
struct dfa *dfa_read(struct values_t *values, char *fname){
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
    int max_idx = 0;
    struct dfa_state *states = NULL;
    for (int i = 0; i < nodes->u.list.nvals; i++) {
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
    for (int i = 0; i < dfa->nstates; i++) {
        dfa->states[i].idx = -1;            // some may not be used
    }
    struct dfa_state *ds;
    while ((ds = states) != NULL) {
        states = ds->next;
        dfa->states[ds->idx] = *ds;
    }

    // read the list of edges
    struct json_value *edges = dict_lookup(jv->u.map, "edges", 5);
    assert(edges->type == JV_LIST);
    for (int i = 0; i < edges->u.list.nvals; i++) {
        struct json_value *edge = edges->u.list.vals[i];
        assert(edge->type == JV_MAP);

        struct dfa_transition *dt = new_alloc(struct dfa_transition);

        struct json_value *src = dict_lookup(edge->u.map, "src", 3);
        assert(src->type == JV_ATOM);
        int src_state = int_parse(src->u.atom.base, src->u.atom.len);
        assert(src_state < dfa->nstates);

        struct json_value *dst = dict_lookup(edge->u.map, "dst", 3);
        assert(dst->type == JV_ATOM);
        dt->dst = int_parse(dst->u.atom.base, dst->u.atom.len);
        assert(dt->dst < dfa->nstates);

        struct json_value *symbol = dict_lookup(edge->u.map, "symbol", 6);
        assert(symbol->type == JV_MAP);
        dt->symbol = value_from_json(values, symbol->u.map);

        dt->idy = dfa->ntransitions++;

        dt->next = dfa->states[src_state].transitions;
        dfa->states[src_state].transitions = dt;

        // printf("EDGE %d %d %s\n", src_state, dt->dst, value_string(dt->symbol));
    }

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

// make a step.  Return -1 upon error.  Record transition in
// transitions if requested
int dfa_step(struct dfa *dfa, int current, uint64_t symbol, bool *transitions){
    struct dfa_state *ds = &dfa->states[current];

    for (struct dfa_transition *dt = ds->transitions; dt != NULL; dt = dt->next) {
        if (dt->symbol == symbol) {
            if (transitions != NULL) {
                transitions[dt->idy] = true;
            }
            return dt->dst;
        }
    }
    return -1;
}

// TODO.  May not need this.
int dfa_ntransitions(struct dfa *dfa){
    return dfa->ntransitions;
}

// See if each of the transitions is in the list of children.
static void dfa_check_missing(struct dfa_state *ds, struct dict *children){
    for (struct dfa_transition *dt = ds->transitions; dt != NULL; dt = dt->next) {
        void *p = dict_lookup(children, &dt->symbol, sizeof(dt->symbol));
        if (p == NULL) {
            printf("MISSING TRANSITION ON %s\n", value_string(dt->symbol));
        }
    }
}

struct ddt_env {
    struct global_t *global;
    int level;
    int dfa_state;
};

static void ddt_visit(void *env, const void *key, unsigned int key_size, void *value){
    struct ddt_env *de = env;
    assert(key_size == sizeof(uint64_t));
    const uint64_t *symbol = key;
    struct dfa_trie *dt = value;

    for (int i = 0; i < de->level; i++) {
        printf("    ");
    }
    char *p = value_string(*symbol);
    printf("%d: %s\n", de->dfa_state, p);
    free(p);

    struct ddt_env de2 = {
        .global = de->global,
        .dfa_state = dfa_step(de->global->dfa, de->dfa_state, *symbol, NULL),
        .level = de->level + 1
    };
    dfa_check_missing(&de->global->dfa->states[de2.dfa_state], dt->children);
    dict_iter(dt->children, ddt_visit, &de2);
}

void dfa_dump_trie(struct global_t *global){
    struct ddt_env de = {
        .global = global,
        .level = 0,
        .dfa_state = dfa_initial(global->dfa)
    };
    dfa_check_missing(&global->dfa->states[de.dfa_state], global->dfa_trie->children);
    dict_iter(global->dfa_trie->children, ddt_visit, &de);
}
