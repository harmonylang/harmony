#include "head.h"

#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#ifndef HARMONY_COMBINE
#include "charm.h"
#include "graph.h"
#endif

#define new_alloc(t)	(t *) calloc(1, sizeof(t))

void graph_init(struct graph_t *graph, unsigned int initial_size) {
    assert(initial_size >= 1);
    graph->size = 0;
    graph->alloc_size = initial_size;
    graph->nodes = malloc(graph->alloc_size * sizeof(struct node *));
}

void graph_add(struct graph_t *graph, struct node *node) {
    node->id = graph->size;
    if (graph->size >= graph->alloc_size) {
        graph->alloc_size = (graph->alloc_size + 1) * 2;
        graph->nodes = realloc(graph->nodes, (graph->alloc_size * sizeof(struct node *)));
    }
    graph->nodes[graph->size++] = node;
}

unsigned int graph_add_multiple(struct graph_t *graph, unsigned int n) {
    unsigned int node_id = graph->size;
    graph->size += n;
    if (graph->size > graph->alloc_size) {
        graph->alloc_size = (graph->alloc_size + 1) * 2;
        graph->nodes = realloc(graph->nodes, (graph->alloc_size * sizeof(struct node *)));
    }
    return node_id;
}

static void inline swap(struct graph_t *graph, unsigned int x, unsigned int y){
    struct node *tmp = graph->nodes[x];
    graph->nodes[x] = graph->nodes[y];
    graph->nodes[y] = tmp;
    graph->nodes[x]->id = x;
    graph->nodes[y]->id = y;
}

struct scc *scc_alloc(unsigned int start, unsigned int finish, struct scc *next){
    struct scc *scc = new_alloc(struct scc);
    scc->start = start;
    scc->finish = finish;
    scc->next = next;
    return scc;
}

// Partition the range scc->start to scc->finish up into four chunks: the nodes in the strongly
// connected component holding node scc->start, the remaining successors of the node, the remaining
// nodes minus the predecessors and the successors, and finally the predecessors minus the nodes
// in the strongly connected component.  Then iteratively visit the last three partitions.
struct scc *graph_find_scc_one(struct graph_t *graph, struct scc *scc, unsigned int component) {
    unsigned int start = scc->start;
    unsigned int finish = scc->finish;
    assert(start < finish);
    struct scc *next_scc = scc->next;

    // Optimization. See if this node has either no incoming or
    // no outgoing edges.  If so, it's a component in its own right
    bool optim = true;
    struct node *node = graph->nodes[start];
    for (struct edge *e = node->fwd; e != NULL; e = e->fwdnext) {
        struct node *next = e->dst;
        if (next->id >= start && next->id < finish) {
            optim = false;
            break;
        }
    }
    if (optim) {
        for (struct edge *e = node->bwd; e != NULL; e = e->bwdnext) {
            struct node *next = e->dst;
            if (next->id >= start && next->id < finish) {
                optim = false;
            }
        }
    }
    if (optim) {
        scc->start++;
        if (scc->start < scc->finish) {
            return scc;
        }
        free(scc);
        return next_scc;
    }

    free(scc);
    scc = next_scc;

    // Better balancing?
    if (finish - start > 100) {
        swap(graph, start, (finish + start) / 2);
    }

    graph->nodes[start]->component = component;

    // Phase 1: move all successors of nodes[0] to the bottom
    unsigned int lo = start + 1;
    for (unsigned int i = start; i < lo; i++) {
        struct node *node = graph->nodes[i];
        for (struct edge *e = node->fwd; e != NULL; e = e->fwdnext) {
            struct node *next = e->dst;
            if (next->id < start || next->id >= finish) {
                continue;
            }
            if (next->id < lo) {
                continue;
            }
            if (next->id > lo) {
                swap(graph, lo, next->id);
            }
            lo++;
            assert(lo <= finish);
        }
    }

    unsigned int hi = finish - 1;
    unsigned int mid = start + 1;

    // Phase 2: move all precedessors
    for (unsigned int i = start, j = hi; i < mid || j > hi;) {
        bool in_scc = i < mid;
        struct node *node = in_scc ? graph->nodes[i] : graph->nodes[j];
        for (struct edge *e = node->bwd; e != NULL; e = e->bwdnext) {
            struct node *next = e->src;
            if (next->id < start || next->id >= finish) {
                continue;
            }
            if (next->id < lo) {        // in SCC
                if (next->id >= mid) {
                    next->component = component;
                    if (next->id > mid) {
                        swap(graph, mid, next->id);
                    }
                    mid++;
                    assert(mid <= lo);
                }
            }
            else {
                if (next->id <= hi) {
                    if (next->id < hi) {
                        swap(graph, hi, next->id);
                    }
                    hi--;
                    assert(hi >= start);
                }
            }
        }
        if (in_scc) { i++; } else { j--; }
    }
    if (mid < lo) {    // predecessors - scc
        scc = scc_alloc(mid, lo, scc);
    }
    if (lo <= hi) {     // rest
        scc = scc_alloc(lo, hi + 1, scc);
    }
    if (hi + 1 < finish) {  // successors - scc
        scc = scc_alloc(hi + 1, finish, scc);
    }
    return scc;
}

unsigned int graph_find_scc(struct graph_t *graph) {
    struct scc *scc = scc_alloc(0, graph->size, NULL);
    unsigned int count = 0;
    while (scc != NULL) {
        scc = graph_find_scc_one(graph, scc, count);
        count++;
    }
    return count;
}

// For tracking data races
struct access_info *graph_ai_alloc(int multiplicity, int atomic, int pc) {
    struct access_info *ai = calloc(1, sizeof(*ai));
    ai->multiplicity = multiplicity;
    ai->atomic = atomic;
    ai->pc = pc;
    return ai;
}

void graph_check_for_data_race(
    struct node *node,
    struct minheap *warnings,
    struct engine *engine
) {
    // TODO.  We're checking both if x and y conflict and y and x conflict for any two x and y, which is redundant
    for (struct edge *edge = node->fwd; edge != NULL; edge = edge->fwdnext) {
        for (struct access_info *ai = edge->ai; ai != NULL; ai = ai->next) {
            if (ai->indices != NULL) {
                assert(ai->n > 0);
                if (ai->multiplicity > 1 && !ai->load && ai->atomic == 0) {
                    struct failure *f = new_alloc(struct failure);
                    f->type = FAIL_RACE;
                    f->edge = node->to_parent;
                    f->address = value_put_address(engine, ai->indices, ai->n * sizeof(hvalue_t));
                    minheap_insert(warnings, f);
                }
                else {
                    for (struct edge *edge2 = edge->fwdnext; edge2 != NULL; edge2 = edge2->fwdnext) {
                        for (struct access_info *ai2 = edge2->ai; ai2 != NULL; ai2 = ai2->next) {
                            if (ai2->indices != NULL && !(ai->load && ai2->load) &&
                                (ai->atomic == 0 || ai2->atomic == 0)) {
                                int min = ai->n < ai2->n ? ai->n : ai2->n;
                                assert(min > 0);
                                if (memcmp(ai->indices, ai2->indices,
                                           min * sizeof(hvalue_t)) == 0) {
                                    struct failure *f = new_alloc(struct failure);
                                    f->type = FAIL_RACE;
                                    f->edge = node->to_parent;
                                    f->address = value_put_address(engine, ai->indices, min * sizeof(hvalue_t));
                                    minheap_insert(warnings, f);
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
