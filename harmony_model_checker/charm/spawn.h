// Supports experimental feature to execute Harmony code rather than model checking it.

struct spawn_info {
    struct global *global;
    struct state *state;
    struct context *ctx;
};

void spawn_thread(struct global *global, struct state *state, struct context *ctx);
