import sys
import cxl

# check to see if this state is bad
def invariant(state):
    return True

def main():
    (code, labels) = cxl.compile(sys.stdin, "<stdin>")
    dine = labels["dine"]
    cxl.run(code, labels, invariant,
        [ (("diner", p), dine) for p in range(1, 6) ])

if __name__ == "__main__":
    main()
