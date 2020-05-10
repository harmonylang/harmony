import cxl

# check to see if this state is bad
def mutex(state):
    x = 0
    for ctx in state.ctxbag.keys():
        if ctx.pc > 0:
            op = state.code[ctx.pc - 1]
            if isinstance(op, cxl.LabelOp) and op.label[0] == "cs":
                x += 1
    return x <= 1

def main():
    cxl.run(mutex, [ (("producer", 0), "produced"), (("consumer", 1), "consumed") ])

if __name__ == "__main__":
    main()
