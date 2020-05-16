import sys
import cxl

# check to see if this state is bad
def invariant(state):
    return True

def main():
    (code, labels, mustreach) = cxl.compile(sys.stdin, "<stdin>")
    cxl.run(code, labels, invariant, mustreach)

if __name__ == "__main__":
    main()
