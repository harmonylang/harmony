#ifndef SRC_DFA_H
#define SRC_DFA_H

#include "global.h"

#define dfa_ntransitions(dfa)   ((dfa)->nedges)
#define dfa_dest(dfa, t)        ((dfa)->edges[t]->dst)

struct dfa_transition {
    struct dfa_transition *next; // linked list maintenance
    unsigned int index;          // transition index in list
    hvalue_t symbol;             // transition symbol
    unsigned int dst;            // destination state
    unsigned int cnt;            // for statistics
};

struct dfa_state {
    struct dfa_state *next;      // linked list maintenance
    unsigned int idx;            // name of state
    bool final;                  // terminal state
    struct dfa_transition *transitions;     // transition map

    // TODO.  Maybe should make transitions a dict
};

struct dfa {
    unsigned int nstates;          // number of states
    unsigned int nedges;           // number of edges
    unsigned int initial;          // initial state
    struct dfa_state *states;      // array of states
    struct dfa_transition **edges; // all transitions
    unsigned int nsymbols;         // number of symbols
    hvalue_t *symbols;             // list of symbols

    // stats
    unsigned int cnt;              // # edges visited
    unsigned int total;            // total transitions done
};

struct dfa *dfa_read(struct allocator *allocator, char *fname);
int dfa_initial(struct dfa *dfa);
bool dfa_is_final(struct dfa *dfa, int state);
int dfa_step(struct dfa *dfa, int current, hvalue_t symbol);
void dfa_check_trie(struct global *global);
int dfa_visited(struct dfa *dfa, int current, hvalue_t symbol);
int dfa_potential(struct dfa *dfa, int current, hvalue_t symbol);
void dfa_dump(struct dfa *dfa);

#endif // SRC_DFA_H
