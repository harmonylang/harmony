import json

def print_vars(d):
    print("{", end="")
    first = True
    for item in d.items():
        if first:
            first = False
        else:
            print(",", end="")
        print(" %s: %s"%item, end="")
    print(" }")

def print_range(mis, start, end, first):
    if not first:
        print(",", end="")
    if start + 1 == end:
        print("%s"%mis[start]["pc"], end="")
    else:
        print("%s-%s"%(mis[start]["pc"], mis[end-1]["pc"]), end="")

def print_megastep(mas):
    print("T%s: %s ["%(mas["tid"], mas["name"]), end="")
    mis = mas["microsteps"]
    start = 0
    first = True
    for i in range(1, len(mis)):
        if "interrupt" in mis[i-1]:
            print_range(mis, start, i-1, first)
            first = False
            start = i
            print(",interrupt", end="")
        elif "choose" in mis[i]:
            print_range(mis, start, i+1, first)
            first = False
            start = i+1
            print("(choose %s)"%mis[i]["choose"], end="")
        elif int(mis[i]["pc"]) != int(mis[i-1]["pc"]) + 1:
            print_range(mis, start, i, first)
            first = False
            start = i
    print_range(mis, start, len(mis), first)
    print("] ", end="")
    print_vars(mas["shared"])

with open("charm.json") as f:
    top = json.load(f)
    assert isinstance(top, dict)
    print("Issue:", top["issue"])
    assert isinstance(top["megasteps"], list)
    for mes in top["megasteps"]:
        print_megastep(mes)
