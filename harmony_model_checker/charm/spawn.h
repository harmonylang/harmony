struct spawn_info {
    struct global *global;
    struct state *state;
    struct context *ctx;
};

void spawn_thread(struct global *global, struct state *state, struct context *ctx);
