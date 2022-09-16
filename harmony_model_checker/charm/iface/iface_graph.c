//
// Created by William Ma on 10/12/21.
//

#include "head.h"

#include <stdio.h>
#include <assert.h>
#include <stdlib.h>

#ifndef HARMONY_COMBINE
#include "iface_graph.h"
#include "hashset.h"
#include "stack.h"
#endif

void iface_graph_print(struct iface_graph_t *graph) {
    printf("graph: %p\n", (void*) graph);
    printf("nodes: %d alloc %d\n", graph->nodes_len, graph->_nodes_alloc_len);
    printf("edges: %d alloc %d\n", graph->edges_len, graph->_edges_alloc_len);

    for (int i = 0; i < graph->edges_len; i++) {
        printf("(%d, %d)\n", graph->edges[i]->src->idx, graph->edges[i]->dst->idx);
    }
}

static void iface_graph_check_invariants(struct iface_graph_t *graph) {
#ifndef NDEBUG
    assert(0 <= graph->nodes_len);
    assert(graph->nodes_len <= graph->_nodes_alloc_len);

    int num_edges = 0;
    for (int i = 0; i < graph->nodes_len; i++) {
        struct iface_node_t *node = graph->nodes[i];
        assert(node->idx == i);

        for (struct iface_edge_t *edge = node->fwd; edge != NULL; edge = edge->next) {
            assert(0 <= edge->dst->idx && edge->dst->idx < graph->nodes_len);
            num_edges += 1;
        }

        for (struct iface_edge_t *edge = node->bwd; edge != NULL; edge = edge->next) {
            assert(0 <= edge->dst->idx && edge->dst->idx < graph->nodes_len);
            num_edges += 1;
        }
    }

    assert(graph->edges_len == num_edges);
#endif
}

struct iface_graph_t *iface_graph_init(int initial_size) {
    assert(initial_size >= 1);

    struct iface_graph_t *graph = malloc(sizeof(struct iface_graph_t));

    graph->nodes_len = 0;
    graph->_nodes_alloc_len = initial_size;
    graph->nodes = malloc(graph->_nodes_alloc_len * sizeof(struct iface_node_t *));

    graph->edges_len = 0;
    graph->_edges_alloc_len = initial_size;
    graph->edges = malloc(graph->_edges_alloc_len * sizeof(struct iface_edge_t *));

    iface_graph_check_invariants(graph);
    return graph;
}

void iface_graph_deinit(struct iface_graph_t *graph) {
    iface_graph_check_invariants(graph);

    for (int i = 0; i < graph->nodes_len; i++) {
        free(graph->nodes[i]);
    }
    free(graph->nodes);

    for (int i = 0; i < graph->edges_len; i++) {
        free(graph->edges[i]);
    }
    free(graph->edges);

    free(graph);
}

struct iface_node_t *iface_graph_add_node(struct iface_graph_t *graph) {
    iface_graph_check_invariants(graph);

    graph->nodes_len++;
    if (graph->nodes_len > graph->_nodes_alloc_len) {
        graph->_nodes_alloc_len = 2 * graph->nodes_len;
        graph->nodes = realloc(graph->nodes, graph->_nodes_alloc_len * sizeof(struct iface_node_t *));
    }

    struct iface_node_t *node = malloc(sizeof(struct iface_node_t));
    node->value = 0;
    node->initial = false;
    node->terminated = false;
    node->choosing = false;
    node->state = NULL;
    node->fwd = NULL;
    node->bwd = NULL;
    node->idx = graph->nodes_len - 1;
    graph->nodes[node->idx] = node;

    iface_graph_check_invariants(graph);

    return graph->nodes[node->idx];
}

void iface_graph_add_edge(struct iface_graph_t *graph, int src_idx, int dst_idx) {
    iface_graph_check_invariants(graph);

    assert(0 <= src_idx && src_idx < graph->nodes_len);
    assert(0 <= dst_idx && dst_idx < graph->nodes_len);

    graph->edges_len += 2;
    if (graph->edges_len > graph->_edges_alloc_len) {
        graph->_edges_alloc_len = 2 * graph->edges_len;
        graph->edges = realloc(graph->edges, graph->_edges_alloc_len * sizeof(struct iface_edge_t *));
    }

    struct iface_edge_t *fwd_edge = malloc(sizeof(struct iface_edge_t));
    fwd_edge->src = graph->nodes[src_idx];
    fwd_edge->dst = graph->nodes[dst_idx];
    fwd_edge->next = graph->nodes[src_idx]->fwd;
    fwd_edge->is_fwd = true;
    graph->nodes[src_idx]->fwd = fwd_edge;
    graph->edges[graph->edges_len - 2] = fwd_edge;

    struct iface_edge_t *bwd_edge = malloc(sizeof(struct iface_edge_t));
    bwd_edge->src = graph->nodes[dst_idx];
    bwd_edge->dst = graph->nodes[src_idx];
    bwd_edge->next = graph->nodes[dst_idx]->bwd;
    bwd_edge->is_fwd = false;
    graph->nodes[dst_idx]->bwd = bwd_edge;
    graph->edges[graph->edges_len - 1] = bwd_edge;

    iface_graph_check_invariants(graph);
}

void iface_graph_add_edge_unique(struct iface_graph_t *graph, int src_idx, int dst_idx, bool is_fwd) {
    for (int i = 0; i < graph->edges_len; i++) {
        struct iface_edge_t *edge = graph->edges[i];
        if (edge->src->idx == src_idx && edge->dst->idx == dst_idx && edge->is_fwd == is_fwd) {
            return;
        }
    }

    iface_graph_add_edge(graph, src_idx, dst_idx);
}

bool iface_node_is_equal(struct iface_node_t *lhs, struct iface_node_t *rhs) {
    return lhs->value == rhs->value
        && lhs->initial == rhs->initial
        && lhs->terminated == rhs->terminated
        && lhs->choosing == rhs->choosing;
}

/**
 * Performs a DFS starting at `node_in_region` and tags all nodes equal to
 * `node_in_region` and touching `nodes_in_region` with `tag`.
 */
static void mark_region_with_tag(struct iface_node_t *node_in_region, const int tag) {
    struct hashset_t visited = hashset_new(0);
    struct stack_t *stack = stack_init(1);

    node_in_region->_tag = tag;
    stack_push(stack, node_in_region);

    while (stack_len(stack) > 0) {
        struct iface_node_t *node = stack_pop(stack);
        if (hashset_contains(visited, &node, sizeof(struct iface_node_t *))) {
            continue;
        }
        assert(iface_node_is_equal(node, node_in_region));

#ifdef true
        bool belongs_in_same_region = true;
        for (struct iface_edge_t *edge = node->fwd; edge != NULL; edge = edge->next) {
            if (!iface_node_is_equal(edge->dst, node_in_region)) {
                belongs_in_same_region = false;
                break;
            }
        }

        if (!belongs_in_same_region) {
            continue;
        }
#endif

        assert(node->_tag == -1 || node->_tag == tag);
        hashset_insert(visited, &node, sizeof(struct iface_node_t *));
        node->_tag = tag;

        for (struct iface_edge_t *edge = node->fwd; edge != NULL; edge = edge->next) {
            if (iface_node_is_equal(edge->dst, node_in_region)) {
                stack_push(stack, edge->dst);
            }
        }

        for (struct iface_edge_t *edge = node->bwd; edge != NULL; edge = edge->next) {
            if (iface_node_is_equal(edge->dst, node_in_region)) {
                stack_push(stack, edge->dst);
            }
        }
    }

    hashset_delete(visited);
    stack_deinit(stack);
}

struct iface_graph_t *iface_graph_destutter(struct iface_graph_t *graph) {
    iface_graph_check_invariants(graph);

    for (int i = 0; i < graph->nodes_len; i++) {
        graph->nodes[i]->_tag = -1;
    }

    int num_tags = 0;
    for (int i = 0; i < graph->nodes_len; i++) {
        struct iface_node_t *node = graph->nodes[i];
        if (node->_tag == -1) {
            mark_region_with_tag(node, num_tags);
            num_tags++;
        }
    }

    struct iface_graph_t *normalized = iface_graph_init(num_tags);
    for (int i = 0; i < num_tags; i++) {
        iface_graph_add_node(normalized);
    }

    for (int i = 0; i < graph->nodes_len; i++) {
        struct iface_node_t *n = graph->nodes[i];
        assert(0 <= n->_tag && n->_tag < num_tags);

        struct iface_node_t *node = normalized->nodes[n->_tag];

        node->value = n->value;
        node->initial = n->initial;
        node->terminated = n->terminated;
        node->choosing = n->choosing;
        node->state = n->state;
    }

    for (int i = 0; i < graph->edges_len; i++) {
        struct iface_edge_t *e = graph->edges[i];
        if (e->is_fwd && e->src->_tag != e->dst->_tag) {
            iface_graph_add_edge_unique(normalized, e->src->_tag, e->dst->_tag, e->is_fwd);
        }
    }

    iface_graph_check_invariants(normalized);

    return normalized;
}

