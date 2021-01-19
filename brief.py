import json

def json_kv(js):
    return (json_string(js["key"]), json_string(js["value"]))

def json_idx(js):
    if js["type"] == "atom":
        return json_string(js)
    return "[" + json_string(js) + "]"

def json_string(js):
    type = js["type"]
    v = js["value"]
    if type in { "bool", "int" }:
        return v
    if type == "atom":
        return "." + v
    if type == "set":
        if v == []:
            return "{}"
        return "{ " + ", ".join(v) + " }"
    if type == "dict":
        if v == []:
            return "()"
        lst = [ json_kv(kv) for kv in v ]
        keys = [ k for k,v in lst ]
        if keys == [str(i) for i in range(len(v))]:
            return "[ " + ", ".join([v for k,v in lst]) + " ]" 
        else:
            return "dict{ " + ", ".join([k + ": " + v for k,v in lst]) + " }" 
    if type == "pc":
        return "PC(%s)"%v
    if type == "address":
        if v == []:
            return "None"
        return "?" + v[0]["value"] + "".join([ json_idx(kv) for kv in v[1:] ])
    if type == "context":
        return "CONTEXT(" + json_string(v["name"]) + ")"

def print_vars(d):
    print("{", end="")
    first = True
    for k, v in d.items():
        if first:
            first = False
        else:
            print(",", end="")
        print(" %s: %s"%(k, json_string(v)), end="")
    print(" }")

def print_range(start, end):
    return "%d-%d"%(start, end)

tid = None
name = None
start = 0
steps = ""
interrupted = False
lastmis = {}
shared = {}
failure = ""

def flush():
    global tid, name, steps, start, lastmis, shared

    if tid != None:
        print("T%s: %s ["%(tid, name), end="")
        if steps != "":
            steps += ","
        steps += print_range(start, int(lastmis["pc"]))
        print(steps + "] ", end="");
        print_vars(shared);

def print_macrostep(mas):
    global tid, name, start, steps, lastmis, interrupted, shared, failure

    mis = mas["microsteps"]
    if mas["tid"] != tid:
        flush()
        tid = mas["tid"]
        name = mas["name"]
        interrupted = False
        lastmis = mis[0]
        start = int(lastmis["pc"])
        if "shared" in lastmis:
            shared = lastmis["shared"]
        lastpc = 0
        steps = ""
        begin = 1
    else:
        begin = 0
    for i in range(begin, len(mis)):
        if "shared" in mis[i]:
            shared = mis[i]["shared"]
        if interrupted:
            if steps != "":
                steps += ","
            steps += print_range(start, int(lastmis["pc"]))
            start = int(mis[i]["pc"])
            steps += ",interrupt"
        elif "choose" in mis[i]:
            if steps != "":
                steps += ","
            steps += print_range(start, int(mis[i]["pc"]))
            steps += "(choose %s)"%json_string(mis[i]["choose"])
            start = int(mis[i]["pc"]) + 1
        elif int(mis[i]["pc"]) != int(lastmis["pc"]) + 1:
            if steps != "":
                steps += ","
            steps += print_range(start, int(lastmis["pc"]))
            start = int(mis[i]["pc"])
        lastmis = mis[i]
        if "failure" in lastmis:
            failure = lastmis["failure"]

with open("charm.json") as f:
    top = json.load(f)
    assert isinstance(top, dict)
    # print("Issue:", top["issue"])
    assert isinstance(top["macrosteps"], list)
    for mes in top["macrosteps"]:
        print_macrostep(mes)
    flush()
    print(failure)
