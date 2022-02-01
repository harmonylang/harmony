#ifndef SRC_DFA_H
#define SRC_DFA_H

#include "global.h"

struct dfa *dfa_read(struct values_t *values, char *fname);
int dfa_initial(struct dfa *dfa);
bool dfa_is_final(struct dfa *dfa, int state);
int dfa_step(struct dfa *dfa, int current, hvalue_t symbol);
int dfa_ntransitions(struct dfa *dfa);
void dfa_check_trie(struct global_t *global);

#endif // SRC_DFA_H
