#ifndef SRC_DFA2_H
#define SRC_DFA2_H

struct dfa_node {
    unsigned int id;            // DFA state id
    struct dict *transitions;   // map of symbol to dfa_node
    bool empty;                 // has no out transitions
    bool final;                 // final state
    struct dfa_node *next;      // for partitioning during minification
    struct dfa_node *rep;       // representative node for partition
};

#endif // SRC_DFA2_H
