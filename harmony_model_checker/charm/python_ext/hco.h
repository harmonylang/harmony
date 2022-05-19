#ifndef SRC_HCO_H
#define SRC_HCO_H

#include "Python.h"

struct push_t {
    const char* type;
    const char* value;
};

struct trace_t {
    const char* pc;
    const char* xpc;
    const char* method;
    const char* calltype;
};

struct microstep_t {
    void* shared;
    const char* npc;
    const char* fp;
};

struct hco_t {
    const char* issue;
    struct {} symbols;
    struct {
        unsigned int idx;
        unsigned int component;
        bool* transitions;
        const char* initial;
    }* nodes;
    const char** code;
    const char** explain;
    struct {
        unsigned int code_idx;
        struct {
            const char* file;
            unsigned int line;
            const char* code;
        } location;
    }* locations;
};

PyObject* create_hco();

#endif // SRC_HCO_H
