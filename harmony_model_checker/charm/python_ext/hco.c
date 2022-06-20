#include <stdlib.h>

#include "hco.h"
#include "charm.h"
#include "ops.h"
#include "json.h"
#include "hashdict.h"

#define PYSTR(s) Py_BuildValue("s", s)

static char *json_string_encode(char *s, int len){
    char *result = malloc(4 * len), *p = result;

    while (len > 0) {
        switch (*s) {
        case '\r':
            *p++ = '\\'; *p++ = 'r';
            break;
        case '\n':
            *p++ = '\\'; *p++ = 'n';
            break;
        case '\f':
            *p++ = '\\'; *p++ = 'f';
            break;
        case '\t':
            *p++ = '\\'; *p++ = 't';
            break;
        case '"':
            *p++ = '\\'; *p++ = '"';
            break;
        case '\\':
            *p++ = '\\'; *p++ = '\\';
            break;
        default:
            *p++ = *s;
        }
        s++;
        len--;
    }
    *p++ = 0;
    return result;
}

// /**
//  * C++ version 0.4 char* style "itoa":
//  * Written by Lukás Chmela
//  * Released under GPLv3.
// */
// static char* itoa(int value, char* result, int base) {
//     // check that the base if valid
//     if (base < 2 || base > 36) { *result = '\0'; return result; }

//     char* ptr = result, *ptr1 = result, tmp_char;
//     int tmp_value;

//     do {
//         tmp_value = value;
//         value /= base;
//         *ptr++ = "zyxwvutsrqponmlkjihgfedcba9876543210123456789abcdefghijklmnopqrstuvwxyz" [35 + (tmp_value - value * base)];
//     } while ( value );

//     // Apply negative sign
//     if (tmp_value < 0) *ptr++ = '-';
//     *ptr-- = '\0';
//     while(ptr1 < ptr) {
//         tmp_char = *ptr;
//         *ptr--= *ptr1;
//         *ptr1++ = tmp_char;
//     }
//     return result;
// }

// char *json_escape_value(hvalue_t v){
//     char *s = value_string(v);
//     int len = strlen(s);
//     if (*s == '[') {
//         *s = '(';
//         s[len-1] = ')';
//     }
//     char *r = json_escape(s, len);
//     free(s);
//     return r;
// }

// bool invariant_check(struct global_t *global, struct state *state, struct step *step, int end){
//     assert(step->ctx->sp == 0);
//     assert(step->ctx->failure == 0);
//     step->ctx->pc++;
//     while (step->ctx->pc != end) {
//         struct op_info *oi = global->code.instrs[step->ctx->pc].oi;
//         int oldpc = step->ctx->pc;
//         (*oi->op)(global->code.instrs[oldpc].env, state, step, global);
//         if (step->ctx->failure != 0) {
//             step->ctx->sp = 0;
//             return false;
//         }
//         assert(step->ctx->pc != oldpc);
//         assert(!step->ctx->terminated);
//     }
//     assert(step->ctx->sp == 1);
//     step->ctx->sp = 0;
//     assert(step->ctx->fp == 0);
//     hvalue_t b = step->ctx->stack[0];
//     assert(VALUE_TYPE(b) == VALUE_BOOL);
//     return VALUE_FROM_BOOL(b);
// }

// static struct dict *collect_symbols(struct graph_t *graph){
//     struct dict *symbols = dict_new(0, NULL, NULL);
//     hvalue_t symbol_id = 0;

//     for (unsigned int i = 0; i < graph->size; i++) {
//         struct node *n = graph->nodes[i];
//         if (!n->reachable) {
//             continue;
//         }
//         for (struct edge *e = n->fwd; e != NULL; e = e->fwdnext) {
//             for (unsigned int j = 0; j < e->nlog; j++) {
//                 void **p = dict_insert(symbols, &e->log[j], sizeof(e->log[j]));
//                 if (*p == NULL) {
//                     *p = (void *) ++symbol_id;
//                 }
//             }
//         }
//     }
//     return symbols;
// }

// struct symbol_env_t {
//     PyObject* symbol_obj;
// };

// static char *json_string_encode(char *s, int len){
//     char *result = malloc(4 * len), *p = result;

//     while (len > 0) {
//         switch (*s) {
//         case '\r':
//             *p++ = '\\'; *p++ = 'r';
//             break;
//         case '\n':
//             *p++ = '\\'; *p++ = 'n';
//             break;
//         case '\f':
//             *p++ = '\\'; *p++ = 'f';
//             break;
//         case '\t':
//             *p++ = '\\'; *p++ = 't';
//             break;
//         case '"':
//             *p++ = '\\'; *p++ = '"';
//             break;
//         case '\\':
//             *p++ = '\\'; *p++ = '\\';
//             break;
//         default:
//             *p++ = *s;
//         }
//         s++;
//         len--;
//     }
//     *p++ = 0;
//     return result;
// }

// void insert_symbols(void *env, const void *key, unsigned int key_size, void *value) {
//     struct symbol_env_t *se = env;
//     const hvalue_t *symbol = key;

//     assert(key_size == sizeof(*symbol));
//     char *p = value_json(*symbol);
//     PyObject* obj = se->symbol_obj;

//     char buffer[sizeof(uint64_t)*8+1];
//     PyDict_SetItemString(obj, itoa((uint64_t) value, buffer, 10), PYSTR(p));
// }

// PyObject* create_symbols(struct dict *symbols) {
//     PyObject* symbols_obj = PyDict_New();

//     struct symbol_env_t se = {.symbol_obj = symbols_obj};
//     dict_iter(symbols, insert_symbols, &se);
//     return symbols_obj;
// }

// PyObject* create_transitions(struct dict *symbols, struct edge *edges){
//     //! TODO
//     PyObject* transitions = PyList_New(10);
//     for (struct edge *e = edges; e != NULL; e = e->fwdnext) {
//         hvalue_t *log = e->log;
//         unsigned int node_id = e->dst->id;

//         void *p = dict_lookup(symbols, log, sizeof(log));
//         assert(p != NULL);
//     }
//     return transitions;
// }

// PyObject* create_vars(hvalue_t v){
//     PyObject* vars_obj = PyDict_New();
//     assert(VALUE_TYPE(v) == VALUE_DICT);
//     unsigned int size;
//     hvalue_t *vars = value_get(v, &size);
//     size /= sizeof(hvalue_t);
//     for (unsigned int i = 0; i < size; i += 2) {
//         char *k = value_string(vars[i]);
// 		int len = strlen(k);
//         char *v = value_json(vars[i+1]);

//         char buffer[len-2];
//         sprintf(buffer, "%.*s", len - 2, k + 1);
//         PyDict_SetItemString(vars_obj, buffer, PYSTR(v));
//         free(k);
//         free(v);
//     }
//     return vars_obj;
// }

// PyObject* create_trace(
//     struct global_t *global,
//     struct context *ctx,
//     int pc,
//     int fp,
//     hvalue_t vars
// ) {
//     if (fp == 0) {
//         return NULL;
//     }
//     assert(fp >= 4);

// 	int level = 0, orig_pc = pc;
//     if (strcmp(global->code.instrs[pc].oi->name, "Frame") == 0) {
//         hvalue_t ct = ctx->stack[ctx->sp - 2];
//         assert(VALUE_TYPE(ct) == VALUE_INT);
//         switch (VALUE_FROM_INT(ct)) {
//         case CALLTYPE_PROCESS:
//             pc++;
//             break;
//         case CALLTYPE_INTERRUPT:
//         case CALLTYPE_NORMAL:
//             {
//                 hvalue_t retaddr = ctx->stack[ctx->sp - 3];
//                 assert(VALUE_TYPE(retaddr) == VALUE_PC);
//                 pc = VALUE_FROM_PC(retaddr);
//             }
//             break;
//         default:
//             fprintf(stderr, "call type: %"PRI_HVAL" %d %d %d\n", ct, ctx->sp, ctx->fp, ctx->pc);
//             // panic("print_trace: bad call type 1");
//         }
//     }
//     while (--pc >= 0) {
//         const char *name = global->code.instrs[pc].oi->name;

//         if (strcmp(name, "Return") == 0) {
// 			level++;
// 		}
//         else if (strcmp(name, "Frame") == 0) {
// 			if (level == 0) {
//                 PyListObject *trace_list = (PyListObject *)PyList_New(10);
// 				if (fp >= 5) {
//                     assert(VALUE_TYPE(ctx->stack[fp - 5]) == VALUE_PC);
// 					int npc = VALUE_FROM_PC(ctx->stack[fp - 5]);
// 					hvalue_t nvars = ctx->stack[fp - 2];
// 					int nfp = ctx->stack[fp - 1] >> VALUE_BITS;

// 					PyObject *prev;
//                     if ((prev = create_trace(global, ctx, npc, nfp, nvars))) {
//                         _PyList_Extend(trace_list, prev);
//                     }
// 				}
//                 PyObject *trace_entry = PyDict_New();
//                 char buffer[(sizeof(int)*8+1)];
//                 PyDict_SetItemString(trace_entry, "pc", PYSTR(itoa(orig_pc, buffer, 10)));

//                 memset(buffer, 0, sizeof buffer);
//                 PyDict_SetItemString(trace_entry, "xpc", PYSTR(itoa(pc, buffer, 10)));

// 				const struct env_Frame *ef = global->code.instrs[pc].env;
// 				char *s = value_string(ef->name), *a = NULL;
// 				int len = strlen(s);
//                 a = json_escape_value(ctx->stack[fp - 3]);
//                 char *str_buffer = malloc(len+strlen(a));
// 				if (*a == '(') {
//                     sprintf(str_buffer, "%.*s%s", len - 2, s + 1, a);
//                     PyDict_SetItemString(trace_entry, "method", PYSTR(str_buffer));
// 				}
// 				else {
//                     sprintf(str_buffer, "%.*s(%s)", len - 2, s + 1, a);
//                     PyDict_SetItemString(trace_entry, "method", PYSTR(str_buffer));
// 				}
//                 free(str_buffer);

//                 hvalue_t ct = ctx->stack[fp - 4];
//                 assert(VALUE_TYPE(ct) == VALUE_INT);
//                 switch (VALUE_FROM_INT(ct)) {
//                 case CALLTYPE_PROCESS:
//                     PyDict_SetItemString(trace_entry, "calltype", PYSTR("process"));
//                     break;
//                 case CALLTYPE_NORMAL:
//                     PyDict_SetItemString(trace_entry, "calltype", PYSTR("normal"));
//                     break;
//                 case CALLTYPE_INTERRUPT:
//                     PyDict_SetItemString(trace_entry, "calltype", PYSTR("interrupt"));
//                     break;
//                 default:
//                     panic("print_trace: bad call type 2");
//                 }

// 				free(s);
// 				free(a);
//                 PyDict_SetItemString(trace_entry, "vars", create_vars(vars));
//                 PyList_Append((PyObject *)trace_list, trace_entry);
//                 return (PyObject *)trace_list;
// 			}
//             else {
//                 assert(level > 0);
//                 level--;
//             }
//         }
//     }
//     return NULL;
// }

// PyObject* diff_state(
//     struct global_t *global,
//     struct state *oldstate,
//     struct state *newstate,
//     struct context *oldctx,
//     struct context *newctx,
//     bool interrupt,
//     bool choose,
//     hvalue_t choice,
//     char *print
// ) {
//     PyObject* diff = PyDict_New();
//     if (global->dumpfirst) {
//         global->dumpfirst = false;
//     }
//     if (newstate->vars != oldstate->vars) {
//         PyDict_SetItemString(diff, "shared", create_vars(newstate->vars));
//     }
//     if (interrupt) {
//         PyDict_SetItemString(diff, "interrupt", PYSTR("True"));
//     }
//     if (choose) {
//         char *val = value_json(choice);
//         PyDict_SetItemString(diff, "choose", PYSTR(val));
//         free(val);
//     }
//     if (print != NULL) {
//         PyDict_SetItemString(diff, "print", PYSTR(print));
//     }
//     char buffer[sizeof(int)*8+1];
//     PyDict_SetItemString(diff, "npc", PYSTR(itoa(newctx->pc, buffer, 10)));
//     if (newctx->fp != oldctx->fp) {
//         PyDict_SetItemString(diff, "fp", PYSTR(itoa(newctx->fp, buffer, 10)));
//         PyObject *trace = create_trace(global, newctx, newctx->pc, newctx->fp, newctx->vars);
//         trace = trace ? trace : PyList_New(0);
//         PyDict_SetItemString(diff, "trace", trace);
//     }
//     if (newctx->this != oldctx->this) {
//         char *val = value_json(newctx->this);
//         PyDict_SetItemString(diff, "this", PYSTR(val));
//         free(val);
//     }
//     if (newctx->vars != oldctx->vars) {
//         PyDict_SetItemString(diff, "local", create_vars(newctx->vars));
//     }
//     if (newctx->atomic != oldctx->atomic) {
//         itoa(newctx->atomic, buffer, 10);
//         PyDict_SetItemString(diff, "atomic", PYSTR(buffer));
//     }
//     if (newctx->readonly != oldctx->readonly) {
//         itoa(newctx->readonly, buffer, 10);
//         PyDict_SetItemString(diff, "readonly", PYSTR(buffer));
//     }
//     if (newctx->interruptlevel != oldctx->interruptlevel) {
//         PyDict_SetItemString(diff, "interruptlevel", PYSTR(newctx->interruptlevel ? "1" : "0"));
//     }
//     if (newctx->failure != 0) {
//         char *val = value_string(newctx->failure);
//         PyDict_SetItemString(diff, "failure", PYSTR(val));
//         PyDict_SetItemString(diff, "mode", PYSTR("failed"));
//         free(val);
//     }
//     else if (newctx->terminated) {
//         PyDict_SetItemString(diff, "mode", PYSTR("terminated"));
//     }

//     int common;
//     for (common = 0; common < newctx->sp && common < oldctx->sp; common++) {
//         if (newctx->stack[common] != oldctx->stack[common]) {
//             break;
//         }
//     }
//     if (common < oldctx->sp) {
//         memset(buffer, 0, sizeof buffer);
//         PyDict_SetItemString(diff, "pop", PYSTR(itoa(oldctx->sp - common, buffer, 10)));
//     }
//     PyObject *push_list = PyList_New(newctx->sp);
//     for (int i = common; i < newctx->sp; i++) {
//         char *val = value_json(newctx->stack[i]);
//         PyList_Append(push_list, PYSTR(val));
//         free(val);
//     }
//     PyDict_SetItemString(diff, "push", push_list);
    
//     memset(buffer, 0, sizeof buffer);
//     PyDict_SetItemString(diff, "pc", PYSTR(itoa(oldctx->pc, buffer, 10)));

//     return diff;
// }

// PyObject* diff_dump(
//     struct global_t *global,
//     struct state *oldstate,
//     struct state *newstate,
//     struct context **oldctx,
//     struct context *newctx,
//     bool interrupt,
//     bool choose,
//     hvalue_t choice,
//     char *print
// ) {
//     int newsize = sizeof(*newctx) + (newctx->sp * sizeof(hvalue_t));

//     if (memcmp(oldstate, newstate, sizeof(struct state)) == 0 &&
//             (*oldctx)->sp == newctx->sp &&
//             memcmp(*oldctx, newctx, newsize) == 0) {
//         return NULL;
//     }

//     // Keep track of old state and context for taking diffs
//     PyObject *diff = diff_state(global, oldstate, newstate, *oldctx, newctx, interrupt, choose, choice, print);
//     *oldstate = *newstate;
//     free(*oldctx);
//     *oldctx = malloc(newsize);
//     memcpy(*oldctx, newctx, newsize);
//     return diff;
// }

// struct microstep_t {
//     PyObject* microsteps;
//     hvalue_t ctx;
// };

// struct microstep_t create_microsteps(
//     struct global_t *global,
//     struct node *node,
//     hvalue_t ctx,
//     hvalue_t choice,
//     bool interrupt,
//     struct state *oldstate,
//     struct context **oldctx,
//     hvalue_t nextvars,
//     int nsteps
// ){
//     // Make a copy of the state
//     PyObject *microsteps = PyList_New(0);

//     struct state *sc = new_alloc(struct state);
//     memcpy(sc, node->state, sizeof(*sc));
//     sc->choosing = 0;

//     struct step step;
//     memset(&step, 0, sizeof(step));
//     step.ctx = value_copy(ctx, NULL);
//     if (step.ctx->terminated || step.ctx->failure != 0) {
//         free(step.ctx);

//         struct microstep_t result = {.microsteps = microsteps, .ctx = ctx};
//         return result;
//     }

//     if (interrupt) {
// 		assert(step.ctx->trap_pc != 0);
//         interrupt_invoke(&step);
//         PyObject *diff = diff_dump(global, oldstate, sc, oldctx, step.ctx, true, false, 0, NULL);
//         PyList_Append(microsteps, diff);
//     }

//     struct dict *infloop = NULL;        // infinite loop detector
//     int instrcnt = 0;
//     for (;;) {
//         int pc = step.ctx->pc;

//         char *print = NULL;
//         struct instr_t *instrs = global->code.instrs;
//         struct op_info *oi = instrs[pc].oi;
//         if (instrs[pc].choose) {
//             step.ctx->stack[step.ctx->sp - 1] = choice;
//             step.ctx->pc++;
//         }
//         else if (instrs[pc].print) {
//             print = value_json(step.ctx->stack[step.ctx->sp - 1]);
//             (*oi->op)(instrs[pc].env, sc, &step, global);
//         }
//         else {
//             (*oi->op)(instrs[pc].env, sc, &step, global);
//         }

//         // Infinite loop detection
//         if (!step.ctx->terminated && step.ctx->failure == 0) {
//             if (infloop == NULL) {
//                 infloop = dict_new(0, NULL, NULL);
//             }

//             int stacksize = step.ctx->sp * sizeof(hvalue_t);
//             int combosize = sizeof(struct combined) + stacksize;
//             struct combined *combo = calloc(1, combosize);
//             combo->state = *sc;
//             memcpy(&combo->context, step.ctx, sizeof(*step.ctx) + stacksize);
//             void **p = dict_insert(infloop, combo, combosize);
//             free(combo);
//             if (*p == (void *) 0) {
//                 *p = (void *) 1;
//             }
//             else {
//                 step.ctx->failure = value_put_atom(&global->values, "infinite loop", 13);
//             }
//         }

//         PyObject *diff = diff_dump(global, oldstate, sc, oldctx, step.ctx, false, global->code.instrs[pc].choose, choice, print);
//         PyList_Append(microsteps, diff);
//         free(print);
//         if (step.ctx->terminated || step.ctx->failure != 0 || step.ctx->stopped) {
//             break;
//         }
//         instrcnt++;
//         if (instrcnt >= nsteps - node->steps) {
//             break;
//         }
//         if (step.ctx->pc == pc) {
//             fprintf(stderr, ">>> %s\n", oi->name);
//         }
//         assert(step.ctx->pc != pc);

//         /* Peek at the next instruction.
//          */
//         oi = global->code.instrs[step.ctx->pc].oi;
//         if (global->code.instrs[step.ctx->pc].choose) {
//             assert(step.ctx->sp > 0);
// #ifdef TODO
//             if (0 && step.ctx->readonly > 0) {    // TODO
//                 value_ctx_failure(step.ctx, &global->values, "can't choose in assertion or invariant");
//                 PyObject *diff = diff_dump(global, oldstate, sc, oldctx, step.ctx, false, global->code.instrs[pc].choose, choice, NULL);
//                 PyList_Append(microsteps, diff);
//                 break;
//             }
// #endif
//             hvalue_t s = step.ctx->stack[step.ctx->sp - 1];
//             if (VALUE_TYPE(s) != VALUE_SET) {
//                 value_ctx_failure(step.ctx, &global->values, "choose operation requires a set");
//                 PyObject *diff = diff_dump(global, oldstate, sc, oldctx, step.ctx, false, global->code.instrs[pc].choose, choice, NULL);
//                 PyList_Append(microsteps, diff);
//                 break;
//             }
//             unsigned int size;
//             hvalue_t *vals = value_get(s, &size);
//             size /= sizeof(hvalue_t);
//             if (size == 0) {
//                 value_ctx_failure(step.ctx, &global->values, "choose operation requires a non-empty set");
//                 PyObject *diff = diff_dump(global, oldstate, sc, oldctx, step.ctx, false, global->code.instrs[pc].choose, choice, NULL);
//                 PyList_Append(microsteps, diff);
//                 break;
//             }
//             if (size == 1) {
//                 choice = vals[0];
//             }
//             else {
//                 break;
//             }
//         }
//     }

//     // Remove old context from the bag
//     hvalue_t count = value_dict_load(sc->ctxbag, ctx);
//     assert(VALUE_TYPE(count) == VALUE_INT);
//     count -= 1 << VALUE_BITS;
//     if (count == VALUE_INT) {
//         sc->ctxbag = value_dict_remove(&global->values, sc->ctxbag, ctx);
//     }
//     else {
//         sc->ctxbag = value_dict_store(&global->values, sc->ctxbag, ctx, count);
//     }

//     hvalue_t after = value_put_context(&global->values, step.ctx);

//     // Add new context to state unless it's terminated or stopped
//     if (step.ctx->stopped) {
//         sc->stopbag = value_bag_add(&global->values, sc->stopbag, after, 1);
//     }
//     else if (!step.ctx->terminated) {
//         sc->ctxbag = value_bag_add(&global->values, sc->ctxbag, after, 1);
//     }

//     // assert(sc->vars == nextvars);
//     ctx = value_put_context(&global->values, step.ctx);

//     free(sc);
//     free(step.ctx);
//     free(step.log);

//     struct microstep_t result = {.microsteps = microsteps, .ctx = ctx};
//     return result;
// }

// char *ctx_status(struct node *node, hvalue_t ctx) {
//     if (node->state->choosing == ctx) {
//         return "choosing";
//     }
//     while (node->state->choosing != 0) {
//         node = node->parent;
//     }
//     struct edge *edge;
//     for (edge = node->fwd; edge != NULL; edge = edge->fwdnext) {
//         if (edge->ctx == ctx) {
//             break;
//         }
//     }
//     if (edge != NULL && edge->dst == node) {
//         return "blocked";
//     }
//     return "runnable";
// }

// PyObject* create_context(
//     struct global_t *global,
//     hvalue_t ctx,
//     int tid,
//     struct node *node
// ) {
//     PyObject *ctx_obj = PyDict_New();
//     char *s, *a;

//     char int_buffer[sizeof(uint64_t)*8+1];
//     PyDict_SetItemString(ctx_obj, "tid", PYSTR(itoa(tid, int_buffer, 10)));
//     memset(int_buffer, 0, sizeof int_buffer);
//     sprintf(int_buffer, "%"PRI_HVAL, ctx);
//     PyDict_SetItemString(ctx_obj, "yhash", PYSTR(int_buffer));

//     struct context *c = value_get(ctx, NULL);

//     s = value_string(c->name);
// 	int len = strlen(s);
//     a = json_escape_value(c->arg);
//     char *str_buffer = malloc(len-2+strlen(a));
//     if (*a == '(') {
//         sprintf(str_buffer, "%.*s%s", len - 2, s + 1, a);
//         PyDict_SetItemString(ctx_obj, "name", PYSTR(str_buffer));
//     }
//     else {
//         sprintf(str_buffer, "%.*s(%s)", len - 2, s + 1, a);
//         PyDict_SetItemString(ctx_obj, "name", PYSTR(str_buffer));
//     }
//     free(str_buffer);
//     free(s);
//     free(a);

//     // assert(VALUE_TYPE(c->entry) == VALUE_PC);   TODO
//     memset(int_buffer, 0, sizeof int_buffer);
//     PyDict_SetItemString(ctx_obj, "entry", PYSTR(itoa((int) (c->entry >> VALUE_BITS), int_buffer, 10)));
//     memset(int_buffer, 0, sizeof int_buffer);
//     PyDict_SetItemString(ctx_obj, "pc", PYSTR(itoa(c->pc, int_buffer, 10)));
//     memset(int_buffer, 0, sizeof int_buffer);
//     PyDict_SetItemString(ctx_obj, "fp", PYSTR(itoa(c->fp, int_buffer, 10)));

// #ifdef notdef
//     {
//         fprintf(file, "STACK %d:\n", c->fp);
//         for (int x = 0; x < c->sp; x++) {
//             fprintf(file, "    %d: %s\n", x, value_string(c->stack[x]));
//         }
//     }
// #endif

//     PyDict_SetItemString(ctx_obj, "trace", create_trace(global, c, c->pc, c->fp, c->vars));

//     if (c->failure != 0) {
//         s = value_string(c->failure);
//         PyDict_SetItemString(ctx_obj, "failure", PYSTR(s));
//         free(s);
//     }

//     if (c->trap_pc != 0) {
//         s = value_string(c->trap_pc);
//         a = value_string(c->trap_arg);
//         char *buffer = malloc(strlen(s) + strlen(a) + 2);
//         if (*a == '(') {
//             sprintf(buffer, "%s%s", s, a);
//             PyDict_SetItemString(ctx_obj, "trap", PYSTR(buffer));
//         }
//         else {
//             sprintf(buffer, "%s(%s)", s, a);
//             PyDict_SetItemString(ctx_obj, "trap", PYSTR(buffer));
//         }
//         free(s);
//         free(buffer);
//     }

//     if (c->interruptlevel) {
//         PyDict_SetItemString(ctx_obj, "interruptlevel", PYSTR("1"));
//     }

//     char buffer[sizeof(int)*8+1];
//     if (c->atomic != 0) {
//         PyDict_SetItemString(ctx_obj, "interruptlevel", PYSTR(itoa(c->atomic, buffer, 10)));
//     }
//     if (c->readonly != 0) {
//         PyDict_SetItemString(ctx_obj, "readonly", PYSTR(itoa(c->readonly, buffer, 10)));
//     }

//     if (c->terminated) {
//         PyDict_SetItemString(ctx_obj, "mode", PYSTR("terminated"));
//     }
//     else if (c->failure != 0) {
//         PyDict_SetItemString(ctx_obj, "mode", PYSTR("failed"));
//     }
//     else if (c->stopped) {
//         PyDict_SetItemString(ctx_obj, "mode", PYSTR("stopped"));
//     }
//     else {
//         PyDict_SetItemString(ctx_obj, "mode", PYSTR(ctx_status(node, ctx)));
//     }

// #ifdef notdef
//     fprintf(file, "          \"stack\": [\n");
//     for (int i = 0; i < c->sp; i++) {
//         s = value_string(c->stack[i]);
//         if (i < c->sp - 1) {
//             fprintf(file, "            \"%s\",\n", s);
//         }
//         else {
//             fprintf(file, "            \"%s\"\n", s);
//         }
//         free(s);
//     }
//     fprintf(file, "          ],\n");
// #endif

//     s = value_json(c->this);

//     PyDict_SetItemString(ctx_obj, "this", PYSTR(s));
//     free(s);

//     return ctx_obj;
// }

// void insert_state(
//     PyObject *step,
//     struct global_t *global,
//     struct node *node
// ) {

// #ifdef notdef
//     PyDict_SetItemString(step, "shared", create_vars(node->state->vars));
// #endif

//     struct state *state = node->state;
//     extern int invariant_cnt(const void *env);
//     struct step inv_step;
//     memset(&inv_step, 0, sizeof(inv_step));
//     inv_step.ctx = new_alloc(struct context);

//     // hvalue_t inv_nv = value_put_atom("name", 4);
//     // hvalue_t inv_tv = value_put_atom("tag", 3);
//     inv_step.ctx->name = value_put_atom(&global->values, "__invariant__", 13);
//     inv_step.ctx->arg = VALUE_LIST;
//     inv_step.ctx->this = VALUE_DICT;
//     inv_step.ctx->vars = VALUE_DICT;
//     inv_step.ctx->atomic = inv_step.ctx->readonly = 1;
//     inv_step.ctx->interruptlevel = false;

//     assert(VALUE_TYPE(state->invariants) == VALUE_SET);
//     unsigned int size;
//     hvalue_t *vals = value_get(state->invariants, &size);
//     size /= sizeof(hvalue_t);
//     int nfailures = 0;

//     PyObject *invfails = PyList_New(size);
//     for (unsigned int i = 0; i < size; i++) {
//         assert(VALUE_TYPE(vals[i]) == VALUE_PC);
//         inv_step.ctx->pc = VALUE_FROM_PC(vals[i]);
//         assert(strcmp(global->code.instrs[inv_step.ctx->pc].oi->name, "Invariant") == 0);
//         int end = invariant_cnt(global->code.instrs[inv_step.ctx->pc].env);
//         bool b = invariant_check(global, state, &inv_step, end);
//         if (inv_step.ctx->failure != 0) {
//             b = false;
//         }
//         if (!b) {
//             PyObject *invfail = PyDict_New();
//             char buffer[sizeof(unsigned int)*8+1];
//             sprintf(buffer, "%u", (unsigned int) VALUE_FROM_PC(vals[i]));
//             PyDict_SetItemString(invfail, "pc", PYSTR(buffer));
//             if (inv_step.ctx->failure == 0) {
//                 PyDict_SetItemString(invfail, "reason", PYSTR("invariant violated"));
//             }
//             else {
//                 char *val = value_string(inv_step.ctx->failure);
// 				int len = strlen(val);
//                 char buffer[len-2];
//                 sprintf(buffer, "%.*s", len-2, val+1);
//                 PyDict_SetItemString(invfail, "reason", PYSTR(buffer));
//                 free(val);
//             }
//             nfailures++;
//         }
//     }
//     PyDict_SetItemString(step, "invfails", invfails);    
//     free(inv_step.ctx);

//     PyObject* contexts = PyList_New(global->nprocesses);
//     for (int i = 0; i < global->nprocesses; i++) {
//         PyObject* ctx = create_context(global, global->processes[i], i, node);
//         PyList_Append(contexts, ctx);
//     }
//     PyDict_SetItemString(step, "contexts", contexts);
// }

// PyObject* create_macrosteps(
//     struct global_t *global,
//     struct node *last,
//     struct node *parent,
//     hvalue_t choice,
//     struct state *oldstate,
//     struct context **oldctx,
//     bool interrupt,
//     int nsteps
// ) {
//     PyListObject* macrosteps = (PyListObject*)PyList_New(10);
//     struct node *node = last;

//     last = parent == NULL ? last->parent : parent;
//     if (last->parent == NULL) {
//         // The parent is null. We are the beginning of the path list.
//     }
//     else {
//         PyObject* post_macrosteps = create_macrosteps(global, last, last->parent, last->choice, oldstate, oldctx, last->interrupt, last->steps);
//         _PyList_Extend(macrosteps, post_macrosteps);
//     }

//     PyObject* step = PyDict_New();
//     char buffer[sizeof(uint64_t)*8+1];
//     itoa(node->id, buffer, 10);
//     PyDict_SetItemString(step, "id", PYSTR(buffer));

//     memset(buffer, 0, sizeof(buffer));
//     itoa(node->len, buffer, 10);
//     PyDict_SetItemString(step, "len", PYSTR(buffer));

//     /* Find the starting context in the list of processes.
//      */
//     hvalue_t ctx = node->before;
//     int pid;
//     for (pid = 0; pid < global->nprocesses; pid++) {
//         if (global->processes[pid] == ctx) {
//             break;
//         }
//     }

//     struct context *context = value_get(ctx, NULL);
//     assert(!context->terminated);
//     char *name = value_string(context->name);
// 	int len = strlen(name);
//     char *arg = json_escape_value(context->arg);
//     // char *c = value_string(choice);

//     itoa(pid, buffer, 10);
//     PyDict_SetItemString(step, "tid", PYSTR(buffer));

//     memset(buffer, 0, sizeof buffer);
//     sprintf(buffer, "%"PRI_HVAL, ctx);
//     PyDict_SetItemString(step, "xhash", PYSTR(buffer));
//     if (*arg == '(') {
//         char buffer[len-2+strlen(arg)];
//         sprintf(buffer, "%.*s%s", len - 2, name + 1, arg);
//         PyDict_SetItemString(step, "name", PYSTR(buffer));
//     }
//     else {
//         char buffer[len+strlen(arg)];
//         sprintf(buffer, "%.*s(%s)", len - 2, name + 1, arg);
//         PyDict_SetItemString(step, "name", PYSTR(buffer));
//     }
//     global->dumpfirst = true;

//     free(name);
//     free(arg);
//     // free(c);
//     memset(*oldctx, 0, sizeof(**oldctx));
//     (*oldctx)->pc = context->pc;

//     // Recreate the steps
//     assert(pid < global->nprocesses);
//     struct microstep_t create_microsteps_result = create_microsteps(
//         global,
//         last,
//         ctx,
//         choice,
//         interrupt,
//         oldstate,
//         oldctx,
//         node->state->vars,
//         nsteps
//     );
//     global->processes[pid] = create_microsteps_result.ctx;
//     PyDict_SetItemString(step, "microsteps", create_microsteps_result.microsteps);

//     /* Match each context to a process.
//      */
//     bool *matched = calloc(global->nprocesses, sizeof(bool));
//     unsigned int nctxs;
//     hvalue_t *ctxs = value_get(node->state->ctxbag, &nctxs);
//     nctxs /= sizeof(hvalue_t);
//     for (unsigned int i = 0; i < nctxs; i += 2) {
//         assert(VALUE_TYPE(ctxs[i]) == VALUE_CONTEXT);
//         assert(VALUE_TYPE(ctxs[i+1]) == VALUE_INT);
//         int cnt = VALUE_FROM_INT(ctxs[i+1]);
//         for (int j = 0; j < cnt; j++) {
//             int k;
//             for (k = 0; k < global->nprocesses; k++) {
//                 if (!matched[k] && global->processes[k] == ctxs[i]) {
//                     matched[k] = true;
//                     break;
//                 }
//             }
//             if (k == global->nprocesses) {
//                 global->processes = realloc(global->processes, (global->nprocesses + 1) * sizeof(hvalue_t));
//                 matched = realloc(matched, (global->nprocesses + 1) * sizeof(bool));
//                 global->processes[global->nprocesses] = ctxs[i];
//                 matched[global->nprocesses] = true;
//                 global->nprocesses++;
//             }
//         }
//     }
//     free(matched);
  
//     insert_state(step, global, node);
//     return (PyObject *)macrosteps;
// }

static int node_cmp(void *n1, void *n2){
    struct node *node1 = n1, *node2 = n2;

    if (node1->len != node2->len) {
        return node1->len - node2->len;
    }
    if (node1->steps != node2->steps) {
        return node1->steps - node2->steps;
    }
    return node1->id - node2->id;
}

static int fail_cmp(void *f1, void *f2){
    struct failure *fail1 = f1, *fail2 = f2;
    return node_cmp(fail1->edge->dst, fail2->edge->dst);
}

// // This routine removes all node that have a single incoming edge and it's
// // an "epsilon" edge (empty print log).  These are essentially useless nodes.
// // Typically about half of the nodes can be removed this way.
// static void destutter1(struct graph_t *graph){
//     for (unsigned int i = 0; i < graph->size; i++) {
//         struct node *n = graph->nodes[i];

//         if (n->bwd != NULL && n->bwd->bwdnext == NULL && n->bwd->nlog == 0) {
//             struct node *parent = n->bwd->src;

//             if (n->final) {
//                 parent->final = true;
//             }

//             // Remove the edge from the parent
//             struct edge **pe, *e;
//             for (pe = &parent->fwd; (e = *pe) != NULL; pe = &e->fwdnext) {
//                 if (e->dst == n && e->nlog == 0) {
//                     *pe = e->fwdnext;
//                     free(e);
//                     break;
//                 }
//             }

//             struct edge *next;
//             for (struct edge *e = n->fwd; e != NULL; e = next) {
//                 // Move the outgoing edge to the parent.
//                 next = e->fwdnext;
//                 e->fwdnext = parent->fwd;
//                 parent->fwd = e;

//                 // Fix the corresponding backwards edge
//                 for (struct edge *f = e->dst->bwd; f != NULL; f = f->bwdnext) {
//                     if (f->src == n && f->nlog == e->nlog &&
//                             memcmp(f->log, e->log, f->nlog * sizeof(*f->log)) == 0) {
//                         f->src = parent;
//                         break;
//                     }
//                 }
//             }
//             n->reachable = false;
//         }
//         else {
//             n->reachable = true;
//         }
//     }
// }


PyObject* create_hco(struct global_t *global) {
    struct minheap *warnings = minheap_create(fail_cmp);
    if (minheap_empty(global->failures)) {
        printf("Check for data races\n");
        for (unsigned int i = 0; i < global->graph.size; i++) {
            struct node *node = global->graph.nodes[i];
            graph_check_for_data_race(node, warnings, &global->values);
            if (!minheap_empty(warnings)) {
                break;
            }
        }
    }

    bool no_issues = minheap_empty(global->failures) && minheap_empty(warnings);

    PyObject* hco = PyDict_New();
    if (no_issues) {
        PyDict_SetItemString(hco, "issue", PYSTR("No issues"));

        destutter1(&global->graph);

        // Output the symbols;
        struct dict *symbols = collect_symbols(&global->graph);
        PyDict_SetItemString(hco, "symbol", create_symbols(symbols));

        const PyObject* nodes_list = PyList_New(global->graph.size);
        for (unsigned int i = 0; i < global->graph.size; i++) {
            struct node *node = global->graph.nodes[i];
            assert(node->id == i);
            if (node->reachable) {
                PyObject *node_obj = PyDict_New();
                char buffer[sizeof(unsigned int)*8+1];
                sprintf(buffer, "%u", node->id);
                PyDict_SetItemString(node_obj, "idx", PYSTR(buffer));
                
                memset(buffer, 0, sizeof(buffer));
                sprintf(buffer, "%u", node->component);
                PyDict_SetItemString(node_obj, "component", PYSTR(buffer));

                PyDict_SetItemString(node_obj,
                    "transitions", create_transitions(symbols, node->fwd));
                if (i == 0) {
                    PyDict_SetItemString(node_obj, "type", PYSTR("initial"));
                }
                else if (node->final) {
                    PyDict_SetItemString(node_obj, "type", PYSTR("terminal"));
                }
                else {
                    PyDict_SetItemString(node_obj, "type", PYSTR("normal"));
                }
            }
        }
    } else {
        // Find shortest "bad" path
        struct failure *bad = NULL;
        if (minheap_empty(global->failures)) {
            bad = minheap_getmin(warnings);
        }
        else {
            bad = minheap_getmin(global->failures);
        }

        switch (bad->type) {
        case FAIL_SAFETY:
            printf("Safety Violation\n");
            PyDict_SetItemString(hco, "issue", PYSTR("Safety violation"));
            break;
        case FAIL_INVARIANT:
            printf("Invariant Violation\n");
            PyDict_SetItemString(hco, "issue", PYSTR("Invariant violation"));
            break;
        case FAIL_BEHAVIOR:
            printf("Behavior Violation: terminal state not final\n");
            PyDict_SetItemString(hco, "issue", PYSTR("Behavior violation: terminal state not final"));
            break;
        case FAIL_TERMINATION:
            printf("Non-terminating state\n");
            PyDict_SetItemString(hco, "issue", PYSTR("Non-terminating state"));
            break;
        case FAIL_BUSYWAIT:
            printf("Active busy waiting\n");
            PyDict_SetItemString(hco, "issue", PYSTR("Active busy waiting"));
            break;
        case FAIL_RACE:
            assert(bad->address != VALUE_ADDRESS);
            char *addr = value_string(bad->address);
            char *json = json_string_encode(addr, strlen(addr));
            printf("Data race (%s)\n", json);

            char *buffer = malloc(strlen(json) + 12);
            sprintf(buffer, "Data race (%s)", json);
            PyDict_SetItemString(hco, "issue", PYSTR(buffer));
            free(addr);
            free(buffer);
            break;
        default:
            printf("main: bad fail type\n");
            return hco;
        }

        // struct state oldstate;
        // memset(&oldstate, 0, sizeof(oldstate));
        // struct context *oldctx = calloc(1, sizeof(*oldctx));
        // global->dumpfirst = true;
        // PyObject* macrosteps = create_macrosteps(global, bad->node, bad->parent, bad->choice, &oldstate, &oldctx, bad->interrupt, bad->node->steps);
        // PyDict_SetItemString(hco, "macrosteps", macrosteps);
        // free(oldctx);
    }
    return hco;
}
