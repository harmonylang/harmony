import sys
import cxl

# check to see if this state is bad
def mutex(state):
    cs = state.labels["cs"]
    cnt = 0
    for (ctx, n) in state.ctxbag.items():
        if ctx.pc == cs:
            cnt += n
    return cnt <= 1

def main():
    (code, labels) = cxl.compile(sys.stdin, "<stdin>")
    cs = labels["cs"]
    cxl.run(code, labels, mutex, [ (("p", 0), cs), (("p", 1), cs) ])

if __name__ == "__main__":
    main()
