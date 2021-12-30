struct dfa *dfa_read(struct values_t *values, char *fname);
int dfa_initial(struct dfa *dfa);
bool dfa_is_final(struct dfa *dfa, int state);
int dfa_step(struct dfa *dfa, int current, uint64_t symbol, bool *transitions);
int dfa_ntransitions(struct dfa *dfa);
