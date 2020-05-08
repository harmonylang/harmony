import cxl

# check to see if this state is bad
def mutex(state):
    nrds = 0
    nwrs = 0
    for ctx in state.ctxbag.keys():
        if ctx.pc > 0:
            op = state.code[ctx.pc - 1]
            if isinstance(op, cxl.LabelOp):
                if op.label[0] == "rcs":
                    nrds += 1
                elif op.label[0] == "wcs":
                    nwrs += 1
    return (nrds == 0 and nwrs <= 1) or nwrs == 0

def main():
    cxl.run(mutex, [
        (("reader", 0), "rcs"),
        (("reader", 1), "rcs"),
        (("writer", 0), "wcs"),
        (("writer", 1), "wcs")
    ])

if __name__ == "__main__":
    main()
