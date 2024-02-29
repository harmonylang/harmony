#include <sys/types.h>
#include <pthread.h>

// Size of disk block in bytes
#define BLOCK_SIZE 512

// Length of the bounded queue
#define QUEUE_LEN 32

// Returns the size (in blocks) of the file in res_n_blocks
struct getsize {
    unsigned int ino;
    blkcnt_t res_n_blocks;
};

// Returns the block of file ino at the given offset in res_block_data and 
// set res_code to 0
// Otherwise, if block does not exist and Harmony returns None, set res_code to -1
struct read {
    unsigned int ino;
    unsigned int offset;
    char res_code;
    char res_block_data[BLOCK_SIZE];
};

// Stores block_data at the given offset in file ino
struct write {
    unsigned int ino;
    unsigned int offset;
    char block_data[BLOCK_SIZE];
};

struct request {
    enum { GETSIZE, READ, WRITE } type;
    enum {
        EMPTY,             // Client hasn't put request
        UNHANDLED,         // Client has put request; server hasn't put reply
        REPLIED,           // Server has replied; client hasn't handled reply
        DONE               // Client has handled reply - ready for cleanup
    } status;
    union {
        struct getsize getsize;
        struct read read;
        struct write write;
    } data;
    pthread_mutex_t req_lk;
    pthread_cond_t replied_cond;
};

struct fuse_queue {
    struct request requests[QUEUE_LEN];
    unsigned int in;        // next slot to put new request
    unsigned int out;       // next unhandled request
    unsigned int gc;        // next slot to be garbage collected
    unsigned int size;      // number of requests not garbage collected (not EMPTY)
    pthread_mutex_t queue_lk;
    pthread_cond_t not_full_cond;
};

void fuse_queue_init(struct fuse_queue *q);

void fuse_queue_alloc_req(struct fuse_queue *q, struct request **req);
void fuse_queue_req_ready(struct fuse_queue *q, struct request *req);

int fuse_queue_get_req(struct fuse_queue *q, struct request **req);
void fuse_queue_reply_ready(struct request *req);

void fuse_queue_get_reply(struct fuse_queue *q, struct request *req);
void fuse_queue_reply_done(struct fuse_queue *q, struct request *req);
