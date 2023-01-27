#ifndef SRC_CALM_CONHASHTAB_H
#define SRC_CALM_CONHASHTAB_H

#include <stdatomic.h>

//concurrent hashtable for calm
struct Conhashtab {
    atomic_bool *resize_flag;
};

void conhashtab_init(struct Conhashtab *ht, atomic_bool *flag);

#endif //SRC_CALM_CONHASHTAB_H