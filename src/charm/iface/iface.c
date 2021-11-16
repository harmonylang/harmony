#include <stdint.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#ifndef HARMONY_COMBINE
#include "iface.h"
#include "hashset.h"
#include "iface_graph.h"
#endif

struct node_vec_t {
    struct node **arr;
    int len;
    int _alloc_len;
};

struct node_vec_t *node_vec_init(int alloc_len) {
    assert(alloc_len > 0);

    struct node_vec_t *vec = malloc(sizeof(struct node_vec_t));
    vec->_alloc_len = alloc_len;
    vec->len = 0;
    vec->arr = malloc(vec->_alloc_len * sizeof(struct node *));
    return vec;
}

void node_vec_deinit(struct node_vec_t *vec) {
    free(vec->arr);
    free(vec);
}

void node_vec_push(struct node_vec_t *vec, struct node *n) {
    vec->len++;
    if (vec->len > vec->_alloc_len) {
        vec->_alloc_len = 2 * vec->len;
        vec->arr = realloc(vec->arr, vec->_alloc_len * sizeof(struct node));
    }

    vec->arr[vec->len - 1] = n;
}

struct node *node_stack_pop(struct node_vec_t *vec) {
    assert(vec->len > 0);
    vec->len--;
    return vec->arr[vec->len];
}

bool node_vec_is_empty(struct node_vec_t *vec) {
    return vec->len == 0;
}

void node_vec_append_all(struct node_vec_t *dst, struct node_vec_t *src) {
    for (int i = 0; i < src->len; i++) {
        node_vec_push(dst, src->arr[i]);
    }
}

void node_vec_print_node_ids(struct node_vec_t *vec) {
    printf("[");
    for (int i = 0; i < vec->len - 1; i++) {
        printf("%d,", vec->arr[i]->id);
    }
    if (vec->len > 0) {
        printf("%d", vec->arr[vec->len - 1]->id);
    }
    printf("]\n");
}

struct node_vec_t *find_one_step_children(struct node *n) {
    struct node_vec_t *result = node_vec_init(1);
    struct node_vec_t *work = node_vec_init(1);
    struct hashset_t visited = hashset_new(0);

    node_vec_push(work, n);
    while (!node_vec_is_empty(work)) {
        struct node *node = node_stack_pop(work);
        if (hashset_contains(visited, &node, sizeof(struct node *))) {
            continue;
        }

        hashset_insert(visited, &node, sizeof(struct node *));

        struct context *ctx = value_get(node->after, NULL);
        if (node != n && (ctx->atomic == 0 || ctx->terminated)) {
            node_vec_push(result, node);
        } else {
            for (struct edge *edge = node->fwd; edge != NULL; edge = edge->next) {
                if (!hashset_contains(visited, &edge->node, sizeof(struct node *))) {
                    node_vec_push(work, edge->node);
                }
            }
        }
    }

    node_vec_deinit(work);
    hashset_delete(visited);

    return result;
}

struct node_vec_t *find_all_children(struct node *n) {
    struct node_vec_t *result = node_vec_init(1);
    for (struct edge *e = n->fwd; e != NULL; e = e->next) {
        node_vec_push(result, e->node);
    }
    return result;
}

uint64_t iface_evaluate(struct global_t *global, struct state *state, struct context **pctx) {
    (*pctx)->terminated = false;
    (*pctx)->failure = 0;
    (*pctx)->sp = 0;
    (*pctx)->pc++;

    while (!(*pctx)->terminated) {
        struct op_info *oi = global->code.instrs[(*pctx)->pc].oi;
        if (strcmp(oi->name, "Return") == 0) {
            break;
        }

        int oldpc = (*pctx)->pc;
        (*oi->op)(global->code.instrs[oldpc].env, state, pctx, global);
        if ((*pctx)->failure != 0) {
            (*pctx)->sp = 0;
            return 0;
        }
        assert((*pctx)->pc != oldpc);
    }

    return value_dict_load((*pctx)->vars, value_put_atom(&global->values, "result", 6));
}

int iface_find_pc(struct code_t *code) {
    const int len = code->len;
    for (int i = 0; i < len; i++) {
        struct instr_t instr = code->instrs[i];
        struct op_info *oi = instr.oi;
        if (strcmp(oi->name, "Frame") == 0) {
            const struct env_Frame *envFrame = instr.env;
            if (strcmp(value_string(envFrame->name), ".__iface__") == 0) {
                return i;
            }
        }
    }
    return -1;
}

/**
 * Creates an iface graph containing the results of evaluating the iface
 * expression at every step.
 *
 * @param global
 * @param iface_pc - pc of the instr that starts the iface function
 * @return
 */
struct iface_graph_t *iface_evaluate_spec_graph(struct global_t *global, int iface_pc) {
    // Create a context for evaluating iface
    struct context *iface_ctx = new_alloc(struct context);
    iface_ctx->name = value_put_atom(&global->values, "__iface__", 8);
    iface_ctx->arg = VALUE_DICT;
    iface_ctx->this = VALUE_DICT;
    iface_ctx->vars = VALUE_DICT;
    iface_ctx->atomic = iface_ctx->readonly = 1;
    iface_ctx->interruptlevel = false;

    // make a guess that the spec graph will have half as many nodes as the
    // global graph
    struct iface_graph_t *iface_graph = iface_graph_init(global->graph.size / 2);

    // dict from (struct node *) to (struct iface_node_t *)
    struct dict *node_to_iface_node = dict_new(global->graph.size / 2);

    struct hashset_t visited = hashset_new(0);

    assert(global->graph.size > 0);
    struct node_vec_t *worklist = node_vec_init(1);
    {
        // process initial node
        struct node *initial_node = global->graph.nodes[0];
        node_vec_push(worklist, initial_node);
        struct iface_node_t **iface_node = (struct iface_node_t **)
                dict_insert(node_to_iface_node, &initial_node, sizeof(struct node *));
        *iface_node = iface_graph_add_node(iface_graph);

        // Give initial node the None value, though it's displayed as "__init__"
        (*iface_node)->value = VALUE_ADDRESS;
        (*iface_node)->initial = true;
        (*iface_node)->terminated = false;

        struct node_vec_t *children = find_all_children(initial_node);
        node_vec_append_all(worklist, children);
        for (int i = 0; i < children->len; i++) {
            struct node *child = children->arr[i];

            struct iface_node_t **child_iface_node = (struct iface_node_t **)
                    dict_insert(node_to_iface_node, &child, sizeof(struct node *));

            if (*child_iface_node == NULL) {
                *child_iface_node = iface_graph_add_node(iface_graph);
            }

            iface_graph_add_edge(iface_graph, (*iface_node)->idx, (*child_iface_node)->idx);
        }

        hashset_insert(visited, &initial_node, sizeof(struct node *));
        node_vec_deinit(children);
    }

    while (!node_vec_is_empty(worklist)) {
        struct node *node = node_stack_pop(worklist);

        if (hashset_contains(visited, &node, sizeof(struct node *))) {
            continue;
        }

        struct iface_node_t *iface_node
                = dict_lookup(node_to_iface_node, &node, sizeof(struct node *));
        assert(iface_node != NULL);

        iface_ctx->pc = iface_pc;
        iface_node->value = iface_evaluate(global, node->state, &iface_ctx);
        iface_node->initial = false;
        iface_node->terminated = value_ctx_all_eternal(node->state->ctxbag);
        if (iface_ctx->failure != 0) {
            iface_node->value = VALUE_ADDRESS;
#ifndef NDEBUG
            printf("Iface Failure: %s\n", value_string(iface_ctx->failure));
#endif
        }

        struct node_vec_t *children = find_all_children(node);
        node_vec_append_all(worklist, children);
        for (int i = 0; i < children->len; i++) {
            struct node *child = children->arr[i];

            struct iface_node_t **child_iface_node = (struct iface_node_t **)
                    dict_insert(node_to_iface_node, &child, sizeof(struct node *));

            if (*child_iface_node == NULL) {
                *child_iface_node = iface_graph_add_node(iface_graph);
            }

            iface_graph_add_edge(iface_graph, iface_node->idx, (*child_iface_node)->idx);
        }

        hashset_insert(visited, &node, sizeof(struct node *));
        node_vec_deinit(children);
    }

    node_vec_deinit(worklist);

    return iface_graph;
}

struct dot_graph_t *iface_convert_to_dot(struct iface_graph_t *graph) {
    struct dot_graph_t *dot = dot_graph_init(graph->nodes_len);

    for (int i = 0; i < graph->nodes_len; i++) {
        struct iface_node_t *node = graph->nodes[i];

        struct dot_node_t *dot_node = dot_graph_new_node(dot);
        dot_node->name = value_string(node->value);
        dot_node->terminating = node->terminated;
        dot_node->initial = node->initial;
    }

    for (int i = 0; i < graph->edges_len; i++) {
        struct iface_edge_t *edge = graph->edges[i];
        if (edge->is_fwd) {
            dot_graph_add_edge(dot, edge->src->idx, edge->dst->idx);
        }
    }

    return dot;
}

struct dot_graph_t *iface_generate_dot_graph(struct global_t *global) {
    int iface_pc = iface_find_pc(&global->code);
    if (iface_pc < 0) {
        return NULL;
    }

    struct iface_graph_t *iface_graph = iface_evaluate_spec_graph(global, iface_pc);
    struct dot_graph_t *dot;
#if true
    struct iface_graph_t *destuttered = iface_graph_destutter(iface_graph);
    iface_graph_deinit(iface_graph);
    dot = iface_convert_to_dot(destuttered);
    iface_graph_deinit(destuttered);
#else
    dot = iface_convert_to_dot(iface_graph);
#endif
    return dot;
}

void iface_write_spec_graph_to_file(struct global_t *global, const char* filename) {
    struct dot_graph_t *dot = iface_generate_dot_graph(global);
    if (dot == NULL) {
        return;
    }

    FILE *iface_file = fopen(filename, "w");
    if (iface_file == NULL) {
        perror(filename);
        exit(1);
    }
    dot_graph_fprint(dot, iface_file);

    dot_graph_deinit(dot);
    fclose(iface_file);
}

void iface_write_spec_graph_to_json_file(struct global_t *global, const char* filename) {
    int iface_pc = iface_find_pc(&global->code);
    if (iface_pc < 0) {
        fprintf(stderr, "iface_write_spec_graph_to_json_file: find_pc failed\n");
        exit(1);
    }
    struct iface_graph_t *iface_graph = iface_evaluate_spec_graph(global, iface_pc);
    struct iface_graph_t *destuttered = iface_graph_destutter(iface_graph);
    iface_graph_deinit(iface_graph);

    FILE *iface_file = fopen(filename, "w");
    if (iface_file == NULL) {
        perror(filename);
        exit(1);
    }

    fprintf(iface_file, "{\n");

    fprintf(iface_file, "  \"nodes\": [\n");
    bool first = true;
    for (int i = 0; i < destuttered->nodes_len; i++) {
        struct iface_node_t *node = destuttered->nodes[i];

        if (!first) {
            fprintf(iface_file, ",\n");
        }
        else {
            first = false;
        }
        fprintf(iface_file, "    {\n");
        fprintf(iface_file, "      \"idx\": %d,\n", node->idx);
        fprintf(iface_file, "      \"value\": \"%s\",\n", value_string(node->value));
        fprintf(iface_file, "      \"type\": ");
        if (node->initial) {
            fprintf(iface_file, "\"initial\"");
        }
        else if (node->terminated) {
            fprintf(iface_file, "\"terminal\"");
        }
        else {
            fprintf(iface_file, "\"normal\"");
        }
        fprintf(iface_file, "\n");
        fprintf(iface_file, "    }");
    }
    fprintf(iface_file, "\n");
    fprintf(iface_file, "  ],\n");

    fprintf(iface_file, "  \"edges\": [\n");
    first = true;
    for (int i = 0; i < destuttered->edges_len; i++) {
        struct iface_edge_t *edge = destuttered->edges[i];

        if (edge->is_fwd) {
            if (!first) {
                fprintf(iface_file, ",\n");
            }
            else {
                first = false;
            }
            fprintf(iface_file, "    {\n");
            fprintf(iface_file, "      \"src\": %d,\n", edge->src->idx);
            fprintf(iface_file, "      \"dst\": %d\n", edge->dst->idx);
            fprintf(iface_file, "    }");
        }
    }
    fprintf(iface_file, "\n");
    fprintf(iface_file, "  ]\n");

    fprintf(iface_file, "}\n");

    iface_graph_deinit(destuttered);
}
