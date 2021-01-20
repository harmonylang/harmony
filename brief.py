import json

def brief_kv(js):
    return (brief_string(js["key"]), brief_string(js["value"]))

def brief_idx(js):
    if js["type"] == "atom":
        return brief_string(js)
    return "[" + brief_string(js) + "]"

def brief_string(js):
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
        lst = [ brief_kv(kv) for kv in v ]
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
        return "?" + v[0]["value"] + "".join([ brief_idx(kv) for kv in v[1:] ])
    if type == "context":
        return "CONTEXT(" + brief_string(v["name"]) + ")"

def brief_print_vars(d):
    print("{", end="")
    first = True
    for k, v in d.items():
        if first:
            first = False
        else:
            print(",", end="")
        print(" %s: %s"%(k, brief_string(v)), end="")
    print(" }")

def brief_print_range(start, end):
    if start == end:
        return "%d"%(start)
    if start + 1 == end:
        return "%d,%d"%(start, end)
    return "%d-%d"%(start, end)

class Brief:
    def __init__(self):
        self.tid = None
        self.name = None
        self.start = 0
        self.steps = ""
        self.interrupted = False        # TODO
        self.lastmis = {}
        self.shared = {}
        self.failure = ""

    def flush(self):
        if self.tid != None:
            print("T%s: %s ["%(self.tid, self.name), end="")
            if self.steps != "":
                self.steps += ","
            self.steps += brief_print_range(self.start, int(self.lastmis["pc"]))
            print(self.steps + "] ", end="");
            brief_print_vars(self.shared);

    def print_macrostep(self, mas):
        mis = mas["microsteps"]
        if mas["tid"] != self.tid:
            self.flush()
            self.tid = mas["tid"]
            self.name = mas["name"]
            self.interrupted = False
            self.lastmis = mis[0]
            self.start = int(self.lastmis["pc"])
            if "shared" in self.lastmis:
                self.shared = self.lastmis["shared"]
            lastpc = 0
            self.steps = ""
            begin = 1
        else:
            begin = 0
        for i in range(begin, len(mis)):
            if "shared" in mis[i]:
                self.shared = mis[i]["shared"]
            if self.interrupted:
                if self.steps != "":
                    self.steps += ","
                self.steps += brief_print_range(self.start, int(self.lastmis["pc"]))
                self.start = int(mis[i]["pc"])
                self.steps += ",interrupt"
            elif "choose" in mis[i]:
                if self.steps != "":
                    self.steps += ","
                self.steps += brief_print_range(self.start, int(mis[i]["pc"]))
                self.steps += "(choose %s)"%brief_string(mis[i]["choose"])
                self.start = int(mis[i]["pc"]) + 1
            elif int(mis[i]["pc"]) != int(self.lastmis["pc"]) + 1:
                if self.steps != "":
                    self.steps += ","
                self.steps += brief_print_range(self.start, int(self.lastmis["pc"]))
                self.start = int(mis[i]["pc"])
            self.lastmis = mis[i]
            if "failure" in self.lastmis:
                self.failure = self.lastmis["failure"]

    def run(self):
        with open("charm.json") as f:
            top = json.load(f)
            assert isinstance(top, dict)
            # print("Issue:", top["issue"])
            assert isinstance(top["macrosteps"], list)
            for mes in top["macrosteps"]:
                self.print_macrostep(mes)
            self.flush()
        print(self.failure)

if __name__ == "__main__":
    b = Brief()
    b.run()
