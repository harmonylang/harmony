#ifndef SRC_CODE_H
#define SRC_CODE_H

#include "json.h"
#include "value.h"

// This structure describes a Harmony instruction in the code.
struct instr {
    struct op_info *oi;     // information about the type of instruction
    const void *env;        // specific arguments to this instruction

    // For efficiency, a variety of other information is kept handy here.
    //  choose:      a Choose instruction
    //  load:        a Load instruction
    //  store:       a Store instruction
    //  del:         a Del instruction
    //  retop:       a Return instruction
    //  pause:       a Pause instruction
    //  print:       a Print instruction
    //  atomicinc:   an AtomicInc instruction
    //  atomicdec:   an AtomicDec instruction
    //  setintlevel: a SetIntlevel instruction
    //  breakable:   a Load, Store, Del, or AtomicInc instruction
    bool choose, load, store, del, retop, print, pause;
    bool atomicinc, atomicdec, setintlevel, breakable;
};

// Code is simply a list of instructions.  code_map keeps track, for each
// instruction, what line of code it came from.
struct code {
    struct instr *instrs;
    unsigned int len;
    struct dict *code_map;       // maps pc to file:line
};

// This is a badly named structure containing an "allocator" (a way for a thread
// to efficiently allocate memory) and the global values of a Harmony state.
struct engine {
    struct allocator *allocator;
    struct dict *values;
};

// During re-execution, Charm keeps track of the callstack of a thread as a
// linked list of invocation (most recent invocation at the start of the list)
struct callstack {
    struct callstack *parent;
    unsigned int pc;                // program counter of invoked method
    unsigned int sp;                // stack pointer (length of context stack)
    unsigned int return_address;    // return address
    hvalue_t arg;                   // argument to the methods
    hvalue_t vars;                  // saved local variables of the parent method
};

struct code code_init_parse(struct engine *engine, struct json_value *json_code);

#endif //SRC_CODE_H
