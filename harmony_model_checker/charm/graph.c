#include "head.h"

#include <assert.h>
#include <stdlib.h>
#include <string.h>

#ifndef HARMONY_COMBINE
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

static struct stack {
    struct stack *next;
    struct node *node;
} *stack;

static void kosaraju_visit(struct node *node) {
    if (node->visited) {
        return;
    }
    node->visited = true;

    for (struct edge *edge = node->fwd; edge != NULL; edge = edge->fwdnext) {
        kosaraju_visit(edge->dst);
    }

    // Push node
    struct stack *s = new_alloc(struct stack);
    s->node = node;
    s->next = stack;
    stack = s;
}

static void kosaraju_assign(struct node *node, int component) {
    if (node->visited) {
        return;
    }
    node->visited = true;
    node->component = component;
    for (struct edge *edge = node->bwd; edge != NULL; edge = edge->bwdnext) {
        kosaraju_assign(edge->src, component);
    }
}

int graph_find_scc(struct graph_t *graph) {
    for (unsigned int i = 0; i < graph->size; i++) {
        kosaraju_visit(graph->nodes[i]);
    }

    // make sure all nodes are marked and on the stack
    // while at it clear all the visited flags
    unsigned int count = 0;
    for (struct stack *s = stack; s != NULL; s = s->next) {
        assert(s->node->visited);
        s->node->visited = false;
        count++;
    }
    assert(count == graph->size);

    count = 0;
    while (stack != NULL) {
        // Pop
        struct stack *top = stack;
        stack = top->next;
        struct node *next = top->node;
        free(top);

        if (!next->visited) {
            kosaraju_assign(next, count++);
        }
    }
    for (unsigned int i = 0; i < graph->size; i++) {
        assert(graph->nodes[i]->visited);
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
                    f->choice = node->choice;
                    f->node = node;
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
                                    f->choice = node->choice;
                                    f->node = node;
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
