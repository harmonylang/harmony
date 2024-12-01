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

void graph_init(struct graph *graph) {
    graph->size = 0;
    graph->nodes = NULL;
}

#ifdef notdef
void graph_add(struct graph *graph, struct node *node) {
    node->id = graph->size;
    if (graph->size >= graph->alloc_size) {
        graph->alloc_size = (graph->alloc_size + 1) * 2;
        graph->nodes = realloc(graph->nodes, (graph->alloc_size * sizeof(struct node *)));
    }
    graph->nodes[graph->size++] = node;
}
#endif

unsigned int graph_add_multiple(struct graph *graph, unsigned int n) {
    unsigned int node_id = graph->size;
    graph->size += n;
    graph->nodes = realloc(graph->nodes, (graph->size * sizeof(struct node *)));
    return node_id;
}

#ifdef SHORT_PTR
void dump_edges(struct node *src){
    struct edge *e = node_edges(src);
    for (unsigned int i = 0; i < src->nedges; i++, e++) {
        printf("--> dst=%p(%ld) stc=%u m=%u f=%u\n",
            edge_dst(e), (int64_t) e->dest, e->stc_id, e->multiple, e->failed);
    }
}
#endif

struct edge *find_edge(struct node *src, struct node *dst){
    struct edge *e = node_edges(src);
    for (unsigned int i = 0; i < src->nedges; i++, e++) {
        if (edge_dst(e) == dst) {
            return e;
        }
    }

#ifndef notdef
    printf("FINDING %p\n", dst);
    e = node_edges(src);
    for (unsigned int i = 0; i < src->nedges; i++, e++) {
        printf("COMPARE %p\n", edge_dst(e));
    }
    panic("find_edge");         // TODO
#endif
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
                        f->node = node->parent;
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

// Look for nodes where the threads are all doing non-atomic accesses (and so at most one load or
// store each), and where the load operations are for a parent object for all the store operatios.
// Those threads are guaranteed to start with a load or a store operation.
static bool graph_special_race(struct node *node){
    struct edge *edge = edge = node_edges(node);
    for (unsigned int i = 0; i < node->nedges; i++, edge++) {
        unsigned int count = 0;
        // Look for the load operations
        for (struct access_info *ai = edge_output(edge)->ai; ai != NULL; ai = ai->next) {
            if (ai->atomic) {
                return false;
            }
            if (!ai->load) {
                break;
            }
            if (count > 0) {
                return false;
            }
            count += 1;
            struct edge *edge2 = node_edges(node);
            for (unsigned int j = 0; j < node->nedges; j++, edge2++) {
                // Look for the store operations
                for (struct access_info *ai2 = edge_output(edge2)->ai; ai2 != NULL; ai2 = ai2->next) {
                    if (ai2->load) {
                        break;
                    }
                    int min = ai->n < ai2->n ? ai->n : ai2->n;
                    assert(min > 0);
                    if (memcmp(ai->indices, ai2->indices, min * sizeof(hvalue_t)) != 0) {
                        break;
                    }
                    if (ai->n >= ai2->n) {
                        return false;
                    }
                }
            }
        }
    }
    return true;
}

static inline bool is_atomic(struct access_info *ai){
    while (ai != NULL) {
        if (!ai->atomic) {
            return false;
        }
        ai = ai->next;
    }
    return true;
}

static struct node *find_step(struct node *node, hvalue_t ctx){
    struct edge *edge = node_edges(node);
    for (unsigned int i = 0; i < node->nedges; i++, edge++) {
        struct step_input *in = edge_input(edge);
        if (in->ctx == ctx) {
            return edge_dst(edge);
        }
    }
    return NULL;
}

static inline bool commute(struct edge *edge1, struct edge *edge2){
    // If both lead to the same state (probably self-loops), then no race.
    struct node *dst1 = edge_dst(edge1);
    struct node *dst2 = edge_dst(edge2);
    if (dst1 == dst2) {
        return true;
    }

    // Skip over funny states
    if (node_state(dst1)->type != STATE_NORMAL) {
        return true;
    }
    if (node_state(dst2)->type != STATE_NORMAL) {
        return true;
    }

    // See if they commute, i.e., taken first step 1 and then step 2 should lead to
    // the same state as first taking step 2 and then step 1.
    struct step_input *in1 = edge_input(edge1);
    struct step_input *in2 = edge_input(edge2);

    // Ignore interrupt steps
    if (in1->ctx == in2->ctx) {
        return true;
    }

    return find_step(dst1, in2->ctx) == find_step(dst2, in1->ctx);
}

static void print_addr(hvalue_t *indices, unsigned int n){
    printf("%u", n);
    for (unsigned int i = 0; i < n; i++) {
        printf(":%s", value_string(indices[i]));
    }
}

static void print_access(char *what, struct access_info *ai){
    printf("%s %c", what, is_atomic(ai) ? 'A' : '-');
    if (ai == NULL) {
        printf(" NIL");
    }
    while (ai != NULL) {
        printf(" %c%c", ai->load ? 'L' : 'S', ai->atomic ? 'A' : '-');
        print_addr(ai->indices, ai->n);
        ai = ai->next;
    }
    printf("\n");
}

// This checks if any two edges, at least one of which is "non-atomic", commute.
void graph_check_for_data_race(
    struct failure **failures,
    struct node *node,
    struct allocator *allocator
) {
    if (node_state(node)->type != STATE_NORMAL) {
        return;
    }

    struct edge *edge = node_edges(node);
    for (unsigned int i = 0; i < node->nedges; i++, edge++) {
        struct edge *edge2 = edge + 1;
        for (unsigned int j = i + 1; j < node->nedges; j++, edge2++) {
            if (is_atomic(edge_output(edge)->ai) && is_atomic(edge_output(edge2)->ai)) {
                continue;
            }
            if (!commute(edge, edge2)) {
                print_access("A1", edge_output(edge)->ai);
                print_access("A2", edge_output(edge2)->ai);
                struct failure *f = new_alloc(struct failure);
                f->type = FAIL_RACE;
                f->node = node;
                f->edge = edge2;
                f->address = VALUE_ADDRESS_SHARED;
                add_failure(failures, f);
            }
        }
    }
}

void graph_check_for_data_race2(
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
                if (edge->multiple && !ai->load && !ai->atomic) {
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
