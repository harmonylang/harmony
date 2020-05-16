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
    finish = labels["finish"]
    cxl.run(code, labels, mutex, [ (("__main__", 0), finish) ])

if __name__ == "__main__":
    main()
