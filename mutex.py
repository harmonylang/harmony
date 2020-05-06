import cxl

# check to see if this state is bad
def mutex(state):
    x = 0
    for ctx in state.contexts.values():
        if ctx.pc > 0:
            op = state.code[ctx.pc]
            if isinstance(op, cxl.LabelOp) and op.label[0] == "cs":
                x += 1
    return x <= 1

def main():
    cxl.run(mutex, [ (("thread", 0), "cs"), (("thread", 1), "cs") ])

if __name__ == "__main__":
    main()
