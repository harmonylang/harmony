
#include "Python.h"

int get_number() {
        return 1;
}

static PyModuleDef mod_def = {
        PyModuleDef_HEAD_INIT,
        "charm",
        NULL,
        -1,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL
};

PyObject* PyInit_charm(void)
{
        return PyModule_Create(&mod_def);
};
