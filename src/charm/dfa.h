struct dfa_trie {
    pthread_mutex_t lock;
    struct dfa_trie *parent;
    uint64_t symbol;            // invalid if parent == NULL
    int dfa_state;
    struct dict *children;      // symbol to child mapping
};

struct dfa *dfa_read(struct values_t *values, char *fname);
int dfa_initial(struct dfa *dfa);
bool dfa_is_final(struct dfa *dfa, int state);
int dfa_step(struct dfa *dfa, int current, uint64_t symbol, bool *transitions);
int dfa_ntransitions(struct dfa *dfa);
void dfa_check_trie(struct global_t *global);
