//
// Created by William Ma on 10/12/21.
//

#ifndef SRC_IFACE_GRAPH_H
#define SRC_IFACE_GRAPH_H

#include <stdint.h>
#include <stdbool.h>

struct iface_node_t {
    int idx;
    struct node *node;

    uint64_t value;
    bool initial;
    bool terminated;
    bool choosing;
    int choosing_atomic_level;

    struct iface_edge_t *fwd;
    struct iface_edge_t *bwd;

    int _tag;
};

struct iface_edge_t {
    struct iface_edge_t *next;

    /**
     * is_fwd iff this edge \in src.fwd
     * !is_fwd iff this edge \in dst.bwd
     */
    bool is_fwd;
    struct iface_node_t *src;
    struct iface_node_t *dst;
};

struct iface_graph_t {
    struct iface_node_t **nodes;
    int nodes_len;
    int _nodes_alloc_len;

    struct iface_edge_t **edges; // all edges, including fwd and bwd
    int edges_len;
    int _edges_alloc_len;
};

void iface_graph_print(struct iface_graph_t *graph);
struct iface_graph_t *iface_graph_init(int initial_size);
void iface_graph_deinit(struct iface_graph_t *graph);
struct iface_node_t *iface_graph_add_node(struct iface_graph_t *graph);
void iface_graph_add_edge(struct iface_graph_t *graph, int src_idx, int dst_idx);
struct iface_graph_t *iface_graph_destutter(struct iface_graph_t *graph);

#endif //SRC_IFACE_GRAPH_H
