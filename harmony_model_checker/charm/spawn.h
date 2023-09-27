// Supports experimental feature to execute Harmony code rather than model checking it.

struct spawn_info {
    struct state *state;
    struct context *ctx;
};

void spawn_thread(struct state *state, struct context *ctx);
