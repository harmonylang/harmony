import sys
import subprocess

def contents(name):
    with open(name, "rb") as fd:
        c = fd.read()
        for i in range(len(c)):
            # if i % 32 == 0:
            #     print("      ", end="")
            print("%02x"%c[i], end="")
            if i % 32 == 31:
                print()
        print()

def file(name):
    print("  <file>")
    print("    <name>")
    print("      %s"%name)
    print("    </name>")
    print("    <contents>")
    contents(name)
    print("    </contents>")
    print("  </file>")


git_vn = subprocess.check_output("git log --pretty=format:'' | wc -l | sed 's/[ \t]//g'", shell=True, text=True).strip()

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<files version="1.2.%s">'%git_vn)
with open(sys.argv[1]) as fd:
    lines = fd.readlines()
    for line in lines:
        file(line.strip())
print("</files>")
