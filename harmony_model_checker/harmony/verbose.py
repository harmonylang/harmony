import json

def verbose_kv(js):
    return (verbose_string(js["key"]), verbose_string(js["value"]))

def verbose_idx(js):
    return "[" + verbose_string(js) + "]"

def verbose_string(js):
    type = js["type"]
    v = js["value"]
    if type == "bool":
        return v
    if type == "int":
        return str(v) if isinstance(v, int) else v
    if type == "atom":
        return json.dumps(v, ensure_ascii=False)
    if type == "set":
        if v == []:
            return "{}"
        lst = [ verbose_string(val) for val in v ]
        return "{ " + ", ".join(lst) + " }"
    if type == "list":
        if v == []:
            return "[]"
        lst = [ verbose_string(val) for val in v ]
        return "[ " + ", ".join(lst) + " ]"
    if type == "dict":
        if v == []:
            return "{:}"
        lst = [ verbose_kv(kv) for kv in v ]
        keys = [ k for k,v in lst ]
        if keys == [str(i) for i in range(len(v))]:
            return "[ " + ", ".join([v for k,v in lst]) + " ]" 
        else:
            return "{ " + ", ".join([k + ": " + v for k,v in lst]) + " }" 
    if type == "pc":
        return "PC(%s)"%v
    if type == "address":
        if v == []:
            return "None"
        return "?" + v[0]["value"] + "".join([ verbose_idx(kv) for kv in v[1:] ])
    if type == "context":
        return "CONTEXT(" + str(v["pc"]) + ")"

def verbose_print_vars(f, d):
    print("{", end="", file=f)
    first = True
    for k, v in d.items():
        if first:
            first = False
        else:
            print(",", end="", file=f)
        print(" %s: %s"%(k, verbose_string(v)), end="", file=f)
    print(" }", file=f)

class Verbose:
    def __init__(self):
        self.tid = None
        self.name = None
        self.start = 0
        self.interrupted = False
        self.lastmis = {}
        self.shared = {}
        self.failure = ""

    def print_macrostep(self, f, mas):
        mis = mas["microsteps"]
        if mas["tid"] != self.tid:
            print(file=f)
            print("================================================", file=f)
            print("Running thread T%s: %s "%(mas["tid"], mas["name"]), file=f)
            print("================================================", file=f)
            self.interrupted = False
            self.lastmis = mis[0]
            self.start = int(self.lastmis["pc"])
            if "shared" in self.lastmis:
                self.shared = self.lastmis["shared"]
            lastpc = 0
            self.steps = ""
        for step in mis:
            print(file=f)
            print("  program counter:  ", step["pc"], file=f)
            print("  code:              %s"%step["code"], file=f)
            # if (int(step["npc"]) != int(step["pc"]) + 1):
            #     print("  pc after:         ", step["npc"], file=f)
            if self.interrupted:
                print("  interrupted:       jump to interrupt handler first", file=f)
            else:
                print("  explanation:       %s"%step["explain"], file=f)
            # if "choose" in step:
            #     print("  chosen value:      %s"%verbose_string(step["choose"]), file=f)
            # if "print" in step:
            #     print("  print value:       %s"%verbose_string(step["print"]), file=f)
            if "shared" in step:
                print("  shared variables:  ", end="", file=f)
                verbose_print_vars(f, step["shared"])
            if "local" in step:
                print("  method variables:  ", end="", file=f)
                verbose_print_vars(f, step["local"])
            if "failure" in step:
                print("  operation failed:  %s"%step["failure"], file=f)
            self.lastmis = step

    def run(self, outputfiles, behavior):
        with open(outputfiles["hco"], encoding='utf-8') as input:
          with open(outputfiles["hvb"], "w", encoding='utf-8') as output:
            top = json.load(input)
            assert isinstance(top, dict)
            if top["issue"] == "No issues":
                return True

            print("Issue:", top["issue"], file=output)
            assert isinstance(top["macrosteps"], list)
            for mes in top["macrosteps"]:
                self.print_macrostep(output, mes)
            print(self.failure, file=output)
            return False
