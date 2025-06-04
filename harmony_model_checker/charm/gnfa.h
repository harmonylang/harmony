#ifndef SRC_GNFA_H
#define SRC_GNFA_H

#include "global.h"

struct regexp {
    enum { RE_EPSILON, RE_SYMBOL, RE_DISJUNCTION, RE_SEQUENCE, RE_KLEENE } type;
    union {
        hvalue_t symbol;
        struct {
            unsigned int ndisj;
            struct regexp **disj;
        } disjunction;
        struct {
            unsigned int nseq;
            struct regexp **seq;
        } sequence;
        struct regexp *kleene;
    } u;
};

struct gnfa {
    unsigned int nstates;          // number of states
    unsigned int size;             // original size of matrix
    struct regexp **transitions;
};

struct gnfa *gnfa_from_dfa(struct dfa *dfa);
void gnfa_rip(struct gnfa *gnfa);

#endif // SRC_GNFA_H
