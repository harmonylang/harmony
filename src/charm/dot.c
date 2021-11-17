#include <stdlib.h>
#include <assert.h>
#include <string.h>

#ifndef HARMONY_COMBINE
#include "dot.h"
#endif

struct dot_graph_t *dot_graph_init(int alloc_len) {
    struct dot_graph_t *graph = malloc(sizeof(struct dot_graph_t));
    graph->nodes = malloc(alloc_len * sizeof(struct dot_node_t *));
    graph->_alloc_len = alloc_len;
    graph->len = 0;
    return graph;
}

void dot_graph_deinit(struct dot_graph_t *graph) {
    for (int i = 0; i < graph->len; i++) {
        free(graph->nodes[i]);
    }
    free(graph->nodes);
    free(graph);
}

struct dot_node_t *dot_graph_new_node(struct dot_graph_t *graph) {
    struct dot_node_t *node = malloc(sizeof(struct dot_node_t));
    node->name = "";
    node->fwd = NULL;
    node->fwd_len = 0;

    int node_idx = graph->len;
    graph->len++;
    assert(graph->len <= graph->_alloc_len);
    if (graph->len == graph->_alloc_len) {
        graph->_alloc_len = 2 * graph->len;
        graph->nodes = realloc(graph->nodes, graph->_alloc_len * sizeof(struct dot_node_t));
    }

    graph->nodes[node_idx] = node;
    return node;
}

void dot_graph_add_edge(struct dot_graph_t *graph, int from_idx, int to_idx) {
    struct dot_node_t *from_node = graph->nodes[from_idx];
    for (int i = 0; i < from_node->fwd_len; i++) {
        if (from_node->fwd[i] == to_idx) {
            return;
        }
    }

    from_node->fwd_len++;
    from_node->fwd = realloc(from_node->fwd, from_node->fwd_len * sizeof(int));
    from_node->fwd[from_node->fwd_len-1] = to_idx;
    graph->nodes[from_idx] = from_node;
}

void node_fprint(struct dot_node_t *node, int i, FILE *f) {
    if (node->initial) {
        fprintf(f, "i");
    } else if (node->terminating) {
        fprintf(f, "t");
    } else {
        fprintf(f, "s");
    }

    fprintf(f, "%d", i);
}

void dot_graph_fprint(struct dot_graph_t *graph, FILE *f) {
    fprintf(f, "digraph {\n");
    for (int i = 0; i < graph->len; i++) {
        struct dot_node_t *node = graph->nodes[i];

        fprintf(f, "  ");

        node_fprint(node, i, f);

        if (node->initial) {
            fprintf(f, " [label=__init__, shape=octagon]\n");
        } else if (node->terminating) {
            fprintf(f, " [label=\"%s\", shape=doubleoctagon]\n", node->name);
        } else if (node->choosing) {
            fprintf(f, " [label=\"%s\", shape=tripleoctagon]\n", node->name);
        } else {
            fprintf(f, " [label=\"%s\", shape=box]\n", node->name);
        }
    }

    for (int node_idx = 0; node_idx < graph->len; node_idx++) {
        struct dot_node_t *node = graph->nodes[node_idx];

        for (int fwd_idx = 0; fwd_idx < node->fwd_len; fwd_idx++) {
            struct dot_node_t *fwd = graph->nodes[node->fwd[fwd_idx]];

            fprintf(f, "  ");
            node_fprint(node, node_idx, f);
            fprintf(f, " -> ");
            node_fprint(fwd, node->fwd[fwd_idx], f);
            fprintf(f, "\n");
        }
    }
    fprintf(f, "}\n");
}
