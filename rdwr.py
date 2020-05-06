import cxl

# check to see if this state is bad
def mutex(state):
    nrds = 0
    nwrs = 0
    for ctx in state.contexts.values():
        if ctx.pc > 0:
            op = state.code[ctx.pc - 1]
            if isinstance(op, cxl.LabelOp):
                if op.label[0] == "rcs":
                    nrds += 1
                elif op.label[0] == "wcs":
                    nwrs += 1
    return (nrds == 0 and nwrs <= 1) or nwrs == 0

def main():
    cxl.run(mutex, [ (("thread", 0), "rcs"), (("thread", 1), "rcs"),
                   (("thread", 2), "wcs"), (("thread", 3), "wcs") ])

if __name__ == "__main__":
    main()
