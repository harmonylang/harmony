import pathlib
import json
import sys

def verbose_kv(js):
    return (verbose_string(js["key"]), verbose_string(js["value"]))

def verbose_idx(js):
    return "[" + verbose_string(js) + "]"

def verbose_tuple(v):
    if v == []:
        return "()"
    lst = [ verbose_string(val) for val in v ]
    return "(" + ", ".join(lst) + ")"

def verbose_string(js):
    type = js["type"]
    if type == "address":
        if "func" not in js:
            return "None"
        result = "?"
        func = js["func"]
        args = js["args"]
        if func["type"] == "pc":
            if int(func["value"]) == -1:
                result += args[0]["value"]
                args = args[1:]
            elif int(func["value"]) == -2:
                result += "@" + args[0]["value"]
                args = args[1:]
            else:
                result += verbose_string(func)
        else:
            result += verbose_string(func)
        return result + "".join([ verbose_idx(kv) for kv in args ])
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

def verbose_print_trace(f, trace):
    for i, call in enumerate(trace):
        if i != 0:
            print(" --> ", end="", file=f)
        print("%s"%call["method"], end="", file=f)
    print(file=f)

def get_mode(ctx):
    mode = ctx["mode"]
    if mode == "terminated":
        return mode
    if "atomic" in ctx and int(ctx["atomic"]) > 0:
        mode += " atomic"
    if "readonly" in ctx and int(ctx["readonly"]) > 0:
        mode += " readonly"
    if "interruptlevel" in ctx and int(ctx["interruptlevel"]) > 0:
        mode += " interrupts-disabled"
    return mode

class Summarize:
    def __init__(self):
        self.tid = None
        self.name = None
        self.start = 0
        self.lastmis = {}
        self.shared = {}
        self.step = 0
        self.stack = []
        self.contexts = []
        self.module = None
        self.stmt = None
        self.expr = None

    def dump_contexts(self, f, exclude):
        for ctx in self.contexts:
            if ctx["tid"] != exclude:
                mode = get_mode(ctx)
                print("    T%s: (%s) "%(ctx["tid"], mode), end="", file=f)
                verbose_print_trace(f, ctx["trace"])
                if "next" in ctx:
                    self.about(ctx, "        ", f)

    def about(self, ctx, prefix, f):
        nxt = ctx["next"]
        if nxt["type"] == "Frame":
            print("%sabout to " % prefix, end="", file=f)
            self.aboutFrame(nxt, f)
        elif nxt["type"] == "Load":
            print("%sabout to " % prefix, end="", file=f)
            self.aboutLoad(ctx["pc"], nxt, f)
        elif nxt["type"] == "Store":
            print("%sabout to " % prefix, end="", file=f)
            self.aboutStore(ctx["pc"], nxt, f)
        elif nxt["type"] == "Print":
            print("%sabout to " % prefix, end="", file=f)
            self.aboutPrint(ctx["pc"], nxt, f)
        elif nxt["type"] == "AtomicInc":
            print("%sabout to " % prefix, end="", file=f)
            self.aboutAtomicInc(ctx["pc"], f)
        elif nxt["type"] == "Assert":
            print("%sabout to " % prefix, end="", file=f)
            self.aboutAssert(ctx["pc"], f)
        # else:
        #     print(nxt, file=f)

    def aboutFrame(self, nxt, f):
        print("run method %s with argument %s"%(nxt["name"], verbose_string(nxt["value"])), file=f)

    def aboutLoad(self, pc, nxt, f):
        print("load variable %s in "%nxt["var"], end="", file=f)
        loc = self.locations[int(pc)]
        self.print_loc_basic(loc, f)
        print(file=f)

    def aboutStore(self, pc, nxt, f):
        print("store %s into variable %s in "%(verbose_string(nxt["value"]), nxt["var"]), end="", file=f)
        loc = self.locations[int(pc)]
        self.print_loc_basic(loc, f)
        print(file=f)

    def aboutPrint(self, pc, nxt, f):
        print("print %s in "%verbose_string(nxt["value"]), end="", file=f)
        loc = self.locations[int(pc)]
        self.print_loc_basic(loc, f)
        print(file=f)

    def aboutAtomicInc(self, pc, f):
        loc = self.locations[int(pc)]
        module = self.hvm["modules"][loc["module"]]
        print("execute atomic section in ", end="", file=f)
        loc = self.locations[int(pc)]
        self.print_loc_basic(loc, f)
        print(file=f)

    def aboutAssert(self, pc, f):
        loc = self.locations[int(pc)]
        module = self.hvm["modules"][loc["module"]]
        print("fail assertion %s:%s: %s"%(loc["module"], loc["line"], module["lines"][int(loc["line"]) - 1]), file=f)

    def print_loc_basic(self, loc, f):
        if loc["module"] == "__main__":
            print("line %d" % loc["line"], end="", file=f)
        else:
            print("line %s/%d" % (loc["module"], loc["line"]), end="", file=f)

    def print_loc(self, prefix, loc, f):
        if loc["module"] == "__main__":
            print("%s- Line %d: " % (prefix, loc["line"]), end="", file=f)
        else:
            print("%s- Line %s/%d: " % (prefix, loc["module"], loc["line"]), end="", file=f)

    def path_str(self, path):
        result = path[0]
        for k in path[1:]:
            result += "[" + str(k) + "]"
        return result

    def listcmp(self, path, before, after, loc, f):
        alen = len(after["value"])
        blen = len(before["value"])
        if alen == blen:
            for i in range(blen):
                self.deepcmp(path + [i], before["value"][i], after["value"][i], loc, f)
        elif alen == blen + 1:
            for i in range(blen):
                self.deepcmp(path + [i], before["value"][i], after["value"][i], loc, f)
            self.print_loc("    ", loc, f)
            print("Set %s to %s" % (self.path_str(path + [blen]), verbose_string(after["value"][blen])), file=f)
        else:
            self.print_loc("    ", loc, f)
            print("Set %s to %s" % (self.path_str(path), verbose_string(after)), file=f)

    def dictcmp(self, path, before, after, loc, f):
        if all(kv["key"]["type"] == "atom" for kv in before["value"]) and all(kv["key"]["type"] == "atom" for kv in after["value"]):
            bd = { verbose_string(kv["key"]):kv["value"] for kv in before["value"] }
            ad = { verbose_string(kv["key"]):kv["value"] for kv in after["value"] }
            self.deepdiff(path, bd, ad, loc, f)
            return
        if all(kv["key"]["type"] == "int" for kv in before["value"]) and all(kv["key"]["type"] == "int" for kv in after["value"]):
            bd = { verbose_string(kv["key"]):kv["value"] for kv in before["value"] }
            ad = { verbose_string(kv["key"]):kv["value"] for kv in after["value"] }
            self.deepdiff(path, bd, ad, loc, f)
            return
        self.print_loc("    ", loc, f)
        print("Set %s to %s" % (self.path_str(path), verbose_string(after)), file=f)

    def deepcmp(self, path, before, after, loc, f):
        if before != after:
            if before["type"] == after["type"] == "list":
                self.listcmp(path, before, after, loc, f)
            elif before["type"] == after["type"] == "dict":
                self.dictcmp(path, before, after, loc, f)
            else:
                self.print_loc("    ", loc, f)
                print("Set %s to %s" % (self.path_str(path), verbose_string(after)), file=f)

    def deepdiff(self, path, before, after, loc, f):
        bk = set(before.keys())
        ak = set(after.keys())
        if len(ak - bk) != 0:
            for k in sorted(ak - bk):
                self.print_loc("    ", loc, f)
                print("Initialize %s to %s" % (self.path_str(path + [k]), verbose_string(after[k])), file=f)
        if len(bk - ak) != 0:
            for k in sorted(bk - ak):
                self.print_loc("    ", loc, f)
                print("Delete variable %s" % self.path_str(path + [k]), file=f)
        for k in sorted(ak & bk):
            self.deepcmp(path + [k], before[k], after[k], loc, f)

    def print_macrostep(self, f, mas):
        mis = mas["microsteps"]
        if mas["tid"] != self.tid:
            for ctx in self.contexts:
                if ctx["tid"] == self.tid:
                    if ctx["mode"] == "terminated":
                        print("    Terminated", file=f)
                    else:
                        mode = get_mode(ctx)
                        # if mode != "runnable":
                        #     print("    Mode = %s"%mode, file=f)
                        print("    Preempted in ", end="", file=f)
                        verbose_print_trace(f, ctx["trace"])
                        if "next" in ctx:
                            self.about(ctx, "      ", f)

            self.tid = mas["tid"]
            # print(file=f)
            # print("================================================", file=f)
            print("- Schedule thread T%s: "%mas["tid"], end="", file=f)
            ctx = mas["context"]
            trace = ctx["trace"]
            verbose_print_trace(f, trace)
            if False and len(trace) > 0:
                vars = trace[-1]["vars"]
                if len(vars) > 0:
                    print("method variables:", file=f)
                    for k, v in vars.items():
                        print("  %s: %s"%(k, verbose_string(v)), file=f)
            self.stack = [ verbose_string(v) for v in ctx["stack"] ]
            # if self.contexts != []:
            #     print("other threads:", file=f)
            #     self.dump_contexts(f, self.tid)
            if len(self.shared) != 0:
                print("    Current values of global variables:", file=f)
                for k, v in self.shared.items():
                    print("      %s: %s"%(k, verbose_string(v)), file=f)
            # print("================================================", file=f)
            self.lastmis = mis[0]
            self.start = int(self.lastmis["pc"])
            if "shared" in self.lastmis:
                self.shared = self.lastmis["shared"]
            lastpc = 0
            self.steps = ""
        self.contexts = mas["contexts"]
        for step in mis:
            self.step += 1
            loc = self.locations[int(step["pc"])]

            if "shared" in step and step["shared"] != self.shared:
                self.deepdiff([], self.shared, step["shared"], loc, f)
                # print("  Set global variables in line %d: " % loc["line"], end="", file=f)
                # verbose_print_vars(f, step["shared"])
                self.shared = step["shared"]

            if "interrupt" in step:
                self.print_loc("    ", loc, f)
                print("Interrupted: jump to interrupt handler first", file=f)
            if "choose" in step:
                self.print_loc("    ", loc, f)
                print("Choose %s"%verbose_string(step["choose"]), file=f)
            if "print" in step:
                self.print_loc("    ", loc, f)
                print("Print %s"%verbose_string(step["print"]), file=f)
            # if "trace" in step:
            #     print("  call trace:        ", end="", file=f)
            #     verbose_print_trace(f, step["trace"])
            # if "mode" in step and step["mode"] != "terminated":
            #     print("  New mode:          %s"%step["mode"], file=f)
            if "interruptlevel" in step:
                self.print_loc("    ", loc, f)
                print("Interrupt level: %s"%step["interruptlevel"], file=f)
            if "failure" in step:
                self.print_loc("    ", loc, f)
                if step["failure"].startswith("Harmony"):
                    print("%s"%step["failure"], file=f)
                else:
                    print("Operation failed: %s"%step["failure"], file=f)
            self.lastmis = step

    def run(self, outputfiles, top):
        with open(outputfiles["hco"], encoding='utf-8') as input:
            output = sys.stdout
            # with open("summary.txt", "w", encoding='utf-8') as output:
            print(file=output)
            assert isinstance(top, dict)
            if top["issue"] == "No issues":
                print("No issues were detected with this program.", file=output)
                return True

            if top["issue"] == "Safety violation":
                print("Summary: something went wrong in an execution", file=output)
            elif top["issue"] == "Non-terminating state":
                print("Summary: some execution cannot terminate", file=output)
            else:
                print("Summary:", top["issue"], file=output)

            assert isinstance(top["macrosteps"], list)
            self.hvm = top["hvm"]

            print(file=output)
            print("Here is a summary of an execution that exhibits the issue:", file=output)
            self.locations = self.hvm["locs"]
            for mes in top["macrosteps"]:
                self.print_macrostep(output, mes)

            if top["issue"] == "Non-terminating state":
                print(file=output)
                print("Final state (all threads are terminated or blocked):", file=output)
                print("  Threads:", file=output)
                self.dump_contexts(output, None)
                print("  Variables:", file=output)
                for k, v in self.shared.items():
                    print("    %s: %s"%(k, verbose_string(v)), file=output)

            if len(self.hvm["modules"]) > 1:
                print(file=output)
                print("This program uses the following modules:", file=output)
                for modname in sorted(self.hvm["modules"].keys()):
                    mod = self.hvm["modules"][modname]
                    print("  %s: %s"%(modname, mod["file"]), file=output)

        print(file=output)
        p = pathlib.Path(outputfiles["htm"]).resolve()
        url = "file://" + str(p)
        print("open " + url + " for detailed information", file=output)
        print("alternatively, use the HarmonyGUI", file=output)
