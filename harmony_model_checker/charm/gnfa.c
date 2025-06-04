#include "head.h"

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "value.h"
#include "hashdict.h"
#include "json.h"
#include "dfa.h"
#include "gnfa.h"

#define gnfa_matrix(g, x, y)   ((g)->transitions[((x) * (g)->size) + (y)])

void regexp_dump(struct regexp *re){
	if (re == NULL) {
		printf("NULL");
		return;
	}
    switch (re->type) {
    case RE_EPSILON:
        printf("e");
        break;
    case RE_SYMBOL:
        printf("[%s]", value_string(re->u.symbol));
        break;
    case RE_DISJUNCTION:
        printf("(");
        for (unsigned int i = 0; i < re->u.disjunction.ndisj; i++) {
            if (i != 0) {
                printf("|");
            }
            regexp_dump(re->u.disjunction.disj[i]);
        }
        printf(")");
        break;
    case RE_SEQUENCE:
        printf("(");
        for (unsigned int i = 0; i < re->u.sequence.nseq; i++) {
            regexp_dump(re->u.sequence.seq[i]);
        }
        printf(")");
        break;
    case RE_KLEENE:
        regexp_dump(re->u.kleene);
        printf("*");
        break;
    default:
        assert(false);
    }
}

struct regexp *regexp_epsilon(){
    struct regexp *re = malloc(sizeof(*re));
    re->type = RE_EPSILON;
    return re;
}

struct regexp *regexp_symbol(hvalue_t symbol){
    struct regexp *re = malloc(sizeof(*re));
    re->type = RE_SYMBOL;
    re->u.symbol = symbol;
    return re;
}

struct regexp *regexp_disjunction(struct regexp *disj[], unsigned int ndisj){
    struct regexp *re = malloc(sizeof(*re));
    re->type = RE_DISJUNCTION;
    unsigned int size = sizeof(re) * ndisj;
    re->u.disjunction.ndisj = ndisj;
    re->u.disjunction.disj = malloc(size);
    memcpy(re->u.disjunction.disj, disj, size);
    return re;
}

struct regexp *regexp_sequence(struct regexp *seq[], unsigned int nseq){
    // See how many non-epsilon transitions there are
    unsigned int noneps = 0;
    for (unsigned int i = 0; i < nseq; i++) {
        if (seq[i]->type != RE_EPSILON) {
            noneps++;
        }
    }

    // If they are all epsilon transitions, just return one of them.
    if (noneps == 0) {
        return seq[0];
    }

    // If there is only one non-epsilon transition, return that one.
    if (noneps == 0) {
        for (unsigned int i = 0; i < nseq; i++) {
            if (seq[i]->type != RE_EPSILON) {
                return seq[i];
            }
        }
    }

    struct regexp *re = malloc(sizeof(*re));
    re->type = RE_SEQUENCE;
    unsigned int size = sizeof(re) * noneps;
    re->u.sequence.nseq = noneps;
    re->u.sequence.seq = malloc(size);
    unsigned int j = 0;
    for (unsigned int i = 0; i < nseq; i++) {
        if (seq[i]->type != RE_EPSILON) {
            re->u.sequence.seq[j++] = seq[i];
        }
    }
    return re;
}

struct regexp *regexp_kleene(struct regexp *kleene){
    struct regexp *re = malloc(sizeof(*re));
    re->type = RE_KLEENE;
    re->u.kleene = kleene;
    return re;
}

// Create a new gNFA from a DFA.  The gNFA will be represented by an
// NxN matrix of transitions, each labeled with a regular expression.
// N is initially the number of states in the DFA plus a new initial
// and final state.  The initial state is 0, the final state is 1.
struct gnfa *gnfa_from_dfa(struct dfa *dfa){
    struct gnfa *gnfa = malloc(sizeof(*gnfa));
    gnfa->nstates = gnfa->size = dfa->nstates + 2;
    gnfa->transitions = calloc(gnfa->size * gnfa->size, sizeof(struct regexp));

    // Go through the original transitions.
    for (unsigned int i = 0; i < dfa->nstates; i++) {
        struct dfa_state *ds = &dfa->states[i];
        for (struct dfa_transition *dt = ds->transitions; dt != NULL;
                                                            dt = dt->next) {
            gnfa_matrix(gnfa, i + 2, dt->dst + 2) = regexp_symbol(dt->symbol);
			printf("%u ==> %u\n", i+2, dt->dst+2);
        }

        if (i == dfa->initial) {
			printf("INIT %u\n", i);
            gnfa_matrix(gnfa, 0, i + 2) = regexp_epsilon();
        }
        if (ds->final) {
			printf("FINAL %u\n", i);
            gnfa_matrix(gnfa, i + 2, 1) = regexp_epsilon();
        }
    }

    return gnfa;
}

// Rip out the last state.
void gnfa_rip1(struct gnfa *gnfa){
    unsigned int last = gnfa->nstates - 1;
    struct regexp *self_loop;
    if (gnfa_matrix(gnfa, last, last) == NULL) {
        self_loop = NULL;
    }
    else {
        self_loop = regexp_kleene(gnfa_matrix(gnfa, last, last));
    }
    for (unsigned int x = 0; x < gnfa->nstates; x++) {
        for (unsigned int y = 0; y < gnfa->nstates; y++) {
            if (x == y) {
                continue;
            }
            struct regexp *r1 = gnfa_matrix(gnfa, x, last);
            if (r1 == NULL) {
                continue;
            }
            struct regexp *r2 = gnfa_matrix(gnfa, last, y);
            if (r2 == NULL) {
                continue;
            }
			printf("FOUND %u -> %u -> %u\n", x, last, y);
            struct regexp *re;
            if (self_loop) {
                struct regexp *seq[3];
                seq[0] = r1;
                seq[1] = self_loop;
                seq[2] = r2;
                re = regexp_sequence(seq, 3);
            }
            else {
                struct regexp *seq[2];
                seq[0] = r1;
                seq[1] = r2;
                re = regexp_sequence(seq, 2);
            }
            struct regexp *re2 = gnfa_matrix(gnfa, x, y);
            if (re2 == NULL) {
                gnfa_matrix(gnfa, x, y) = re;
            }
            else {
                struct regexp *disj[2];
                disj[0] = re2;
                disj[1] = re;
                gnfa_matrix(gnfa, x, y) = regexp_disjunction(disj, 2);
            }
        }
    }

	// Reduce size of graph by 1
	// TODO.  Remove last row and last column
    gnfa->nstates = last;
}

// Keep ripping out states until just initial and final state left.
void gnfa_rip(struct gnfa *gnfa){
    printf("REGEXP: ");
    while (gnfa->nstates > 2) {
        gnfa_rip1(gnfa);
    }
    regexp_dump(gnfa_matrix(gnfa, 0, 1));
    printf("\n");
}
