#include "head.h"

#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#ifndef HARMONY_COMBINE
#include "value.h"
#include "ops.h"
#include "charm.h"
#include "graph.h"
#endif

#define new_alloc(t)	(t *) calloc(1, sizeof(t))

void graph_init(struct graph *graph, unsigned int initial_size) {
    assert(initial_size >= 1);
    graph->size = 0;
    graph->alloc_size = initial_size;
    graph->nodes = malloc(graph->alloc_size * sizeof(struct node *));
}

void graph_add(struct graph *graph, struct node *node) {
    node->id = graph->size;
    if (graph->size >= graph->alloc_size) {
        graph->alloc_size = (graph->alloc_size + 1) * 2;
        graph->nodes = realloc(graph->nodes, (graph->alloc_size * sizeof(struct node *)));
    }
    graph->nodes[graph->size++] = node;
}

unsigned int graph_add_multiple(struct graph *graph, unsigned int n) {
    unsigned int node_id = graph->size;
    graph->size += n;
    if (graph->size > graph->alloc_size) {
        graph->alloc_size = (graph->size + 1) * 2;
        graph->nodes = realloc(graph->nodes, (graph->alloc_size * sizeof(struct node *)));
    }
    return node_id;
}

struct edge *find_edge(struct node *src, struct node *dst){
    struct edge *e = node_edges(src);
    for (unsigned int i = 0; i < src->nedges; i++, e++) {
        if (e->u.after.dst == dst) {
            return e;
        }
    }
    return NULL;
}

struct edge *node_to_parent(struct node *n){
    return n->parent == NULL ? NULL : find_edge(n->parent, n);
}

static bool graph_edge_conflict(
    struct failure **failures,
    struct allocator *allocator,
    struct node *node,
    struct edge *edge,
    struct edge *edge2
) {
    for (struct access_info *ai = edge_output(edge)->ai; ai != NULL; ai = ai->next) {
        if (ai->indices != NULL) {
            for (struct access_info *ai2 = edge_output(edge2)->ai; ai2 != NULL; ai2 = ai2->next) {
                if (ai2->indices != NULL && !(ai->load && ai2->load) && (!ai->atomic || !ai2->atomic)) {
                    int min = ai->n < ai2->n ? ai->n : ai2->n;
                    assert(min > 0);
                    if (memcmp(ai->indices, ai2->indices,
                                   min * sizeof(hvalue_t)) == 0) {
                        struct failure *f = new_alloc(struct failure);
                        f->type = FAIL_RACE;
                        f->edge = node_to_parent(node);
                        f->address = value_put_address(allocator, ai->indices, min * sizeof(hvalue_t));
                        add_failure(failures, f);
                        return true;
                    }
                }
            }
        }
    }
    return false;
}

void graph_check_for_data_race(
    struct failure **failures,
    struct node *node,
    struct allocator *allocator
) {
    // First check whether any edges conflict with themselves.  That could
    // happen if more than one thread is in the same state and (all) write
    // the same variable
    struct edge *edge = node_edges(node);
    for (unsigned int i = 0; i < node->nedges; i++, edge++) {
        for (struct access_info *ai = edge_output(edge)->ai; ai != NULL; ai = ai->next) {
            if (ai->indices != NULL) {
                assert(ai->n > 0);
                if ((edge->u.after.flags & EDGE_MULTIPLE) && !ai->load && !ai->atomic) {
                    struct failure *f = new_alloc(struct failure);
                    f->type = FAIL_RACE;
                    f->edge = node_to_parent(node);
                    f->address = value_put_address(allocator, ai->indices, ai->n * sizeof(hvalue_t));
                    add_failure(failures, f);
                }
            }
        }
    }

    // Now check if different edges conflict with one another
    edge = node_edges(node);
    for (unsigned int i = 0; i < node->nedges; i++, edge++) {
        struct edge *edge2 = edge + 1;
        for (unsigned int j = i + 1; j < node->nedges; j++, edge2++) {
            if (graph_edge_conflict(failures, allocator, node, edge, edge2)) {
                break;
            }
        }
    }
}
