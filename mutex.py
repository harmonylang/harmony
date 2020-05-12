import sys
import cxl

# check to see if this state is bad
def mutex(state):
    cs = state.labels["cs"]
    cnt = 0
    for ctx in state.ctxbag.keys():
        for pc in ctx.steps:
            if pc == cs:
                cnt += 1
                break
    return cnt <= 1

def main():
    (code, labels) = cxl.compile(sys.stdin, "<stdin>")
    pc = labels["cs"]
    cxl.run(code, labels, mutex, [ (("p", 0), pc), (("p", 1), pc) ])

if __name__ == "__main__":
    main()
