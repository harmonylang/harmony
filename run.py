import sys
import cxl

# check to see if this state is bad
def mutex(state):
    return True

def main():
    (code, labels) = cxl.compile(sys.stdin, "<stdin>")
    cxl.run(code, labels, mutex, [])

if __name__ == "__main__":
    main()
