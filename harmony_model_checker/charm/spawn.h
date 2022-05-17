struct spawn_info {
    struct global_t *global;
    struct state *state;
    struct context *ctx;
};

void spawn_thread(struct global_t *global, struct state *state, struct context *ctx);
