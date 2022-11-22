import json

def verbose_kv(js):
    return (verbose_string(js["key"]), verbose_string(js["value"]))

def verbose_idx(js):
    return "[" + verbose_string(js) + "]"

def verbose_string(js):
    type = js["type"]
    if type == "address":
        if "func" not in js:
            return "None"
        result = "?"
        func = js["func"]
        args = js["args"]
        if func["type"] == "pc":
            if int(func["value"]) in { -1, -2 }:
                result += args[0]["value"]
                args = args[1:]
            elif int(func["value"]) == -3:
                result += "this." + args[0]["value"]
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
    if "atomic" in ctx and int(ctx["atomic"]) > 0:
        mode += " atomic"
    if "readonly" in ctx and int(ctx["readonly"]) > 0:
        mode += " readonly"
    if "interruptlevel" in ctx and int(ctx["interruptlevel"]) > 0:
        mode += " interrupts-disabled"
    return mode

class Verbose:
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
                print("  T%s: pc=%s %s "%(ctx["tid"], ctx["pc"], mode), end="", file=f)
                verbose_print_trace(f, ctx["trace"])
                if "next" in ctx:
                    print("    about to ", end="", file=f)
                    self.about(ctx, f)

    def about(self, ctx, f):
        nxt = ctx["next"]
        if nxt["type"] == "Frame":
            self.aboutFrame(nxt, f)
        elif nxt["type"] == "Load":
            self.aboutLoad(nxt, f)
        elif nxt["type"] == "Store":
            self.aboutStore(nxt, f)
        elif nxt["type"] == "Print":
            self.aboutPrint(nxt, f)
        elif nxt["type"] == "AtomicInc":
            self.aboutAtomicInc(ctx["pc"], f)
        elif nxt["type"] == "Assert":
            self.aboutAssert(ctx["pc"], f)
        else:
            print(nxt, file=f)

    def aboutFrame(self, nxt, f):
        print("run method %s with argument %s"%(nxt["name"], verbose_string(nxt["value"])), file=f)

    def aboutLoad(self, nxt, f):
        print("load variable %s"%nxt["var"], file=f)

    def aboutStore(self, nxt, f):
        print("store %s into variable %s"%(verbose_string(nxt["value"]), nxt["var"]), file=f)

    def aboutPrint(self, nxt, f):
        print("print %s"%verbose_string(nxt["value"]), file=f)

    def aboutAtomicInc(self, pc, f):
        loc = self.locations[int(pc)]
        module = self.hvm["modules"][loc["module"]]
        print("execute %s:%s: %s"%(loc["module"], loc["line"], module["lines"][int(loc["line"]) - 1]), file=f)

    def aboutAssert(self, pc, f):
        loc = self.locations[int(pc)]
        module = self.hvm["modules"][loc["module"]]
        print("fail assertion %s:%s: %s"%(loc["module"], loc["line"], module["lines"][int(loc["line"]) - 1]), file=f)
    def print_macrostep(self, f, mas):
        mis = mas["microsteps"]
        if mas["tid"] != self.tid:
            self.tid = mas["tid"]
            print(file=f)
            print("================================================", file=f)
            print("Running thread T%s: "%mas["tid"], end="", file=f)
            ctx = mas["context"]
            trace = ctx["trace"]
            verbose_print_trace(f, trace)
            if len(trace) > 0:
                vars = trace[-1]["vars"]
                if len(vars) > 0:
                    print("method variables:", file=f)
                    for k, v in vars.items():
                        print("  %s: %s"%(k, verbose_string(v)), file=f)
            mode = get_mode(ctx)
            print("mode: ", mode, file=f)
            self.stack = [ verbose_string(v) for v in ctx["stack"] ]
            print("stack:", self.stack, file=f)
            if self.contexts != []:
                print("other threads:", file=f)
                self.dump_contexts(f, self.tid)
            if len(self.shared) != 0:
                print("shared variables:", file=f)
                for k, v in self.shared.items():
                    print("  %s: %s"%(k, verbose_string(v)), file=f)
            print("state id: %s"%mas["id"], file=f)
            print("================================================", file=f)
            self.lastmis = mis[0]
            self.start = int(self.lastmis["pc"])
            if "shared" in self.lastmis:
                self.shared = self.lastmis["shared"]
            lastpc = 0
            self.steps = ""
        self.contexts = mas["contexts"]
        for step in mis:
            self.step += 1
            print(file=f)
            print("Step %d:"%self.step, file=f)
            print("  program counter:  ", step["pc"], file=f)
            print("  hvm code:          %s"%step["code"], file=f)
            # if (int(step["npc"]) != int(step["pc"]) + 1):
            #     print("  pc after:         ", step["npc"], file=f)
            if "interrupt" in step:
                print("  interrupted:       jump to interrupt handler first", file=f)
            else:
                print("  explanation:       %s"%step["explain"], file=f)
            loc = self.locations[int(step["pc"])]
            if loc["module"] != self.module:
                print("  module:            %s"%loc["module"], file=f)
                self.module = loc["module"]
            stmt = loc["stmt"]
            if stmt != self.stmt:
                print("  start statement:   line=%d column=%d"%(stmt[0], stmt[1]), file=f)
                print("  end statement:     line=%d column=%d"%(stmt[2], stmt[3]), file=f)
                self.stmt = stmt
            expr = tuple(int(loc[x]) for x in [ "line", "column", "endline", "endcolumn" ])
            if expr != self.expr:
                spaces = 0
                code = loc["code"]
                while spaces < len(code) and code[spaces] == ' ':
                    spaces += 1
                print("  source code:       %s"%code[spaces:], file=f)
                if stmt[0] == stmt[2] == expr[0] == expr[2]:
                    for _ in range(expr[1] + 20 - spaces):
                        print(" ", end="", file=f)
                    for _ in range(expr[3] - expr[1] + 1):
                        print("^", end="", file=f)
                    print(file=f)
                self.expr = expr
            else:
                print("  start expression:  line=%d column=%d"%(expr[0], expr[1]), file=f)
                print("  end expression:    line=%d column=%d"%(expr[2], expr[3]), file=f)
            # if "choose" in step:
            #     print("  chosen value:      %s"%verbose_string(step["choose"]), file=f)
            # if "print" in step:
            #     print("  print value:       %s"%verbose_string(step["print"]), file=f)
            if "shared" in step:
                print("  shared variables:  ", end="", file=f)
                verbose_print_vars(f, step["shared"])
                self.shared = step["shared"]
            if "local" in step:
                print("  method variables:  ", end="", file=f)
                verbose_print_vars(f, step["local"])
            if "trace" in step:
                print("  call trace:        ", end="", file=f)
                verbose_print_trace(f, step["trace"])
            if "mode" in step:
                print("  new mode:          %s"%step["mode"], file=f)
            if "interruptlevel" in step:
                print("  interrupt level:   %s"%step["interruptlevel"], file=f)
            stack_changed = False
            if "pop" in step:
                pop = int(step["pop"])
                if pop > 0:
                    stack_changed = True
                    self.stack = self.stack[:-int(step["pop"])]
            if "push" in step:
                push = [ verbose_string(v) for v in step["push"] ]
                if push != []:
                    stack_changed = True
                    self.stack += push
            if stack_changed:
                print("  stack:             [%s]"%", ".join(self.stack), file=f)
            if "failure" in step:
                print("  operation failed:  %s"%step["failure"], file=f)
            self.lastmis = step

    def print_macrostep(self, f, mas):
        mis = mas["microsteps"]
        if mas["tid"] != self.tid:
            self.tid = mas["tid"]
            print(file=f)
            print("================================================", file=f)
            print("Running thread T%s: "%mas["tid"], end="", file=f)
            ctx = mas["context"]
            trace = ctx["trace"]
            verbose_print_trace(f, trace)
            if len(trace) > 0:
                vars = trace[-1]["vars"]
                if len(vars) > 0:
                    print("method variables:", file=f)
                    for k, v in vars.items():
                        print("  %s: %s"%(k, verbose_string(v)), file=f)
            mode = get_mode(ctx)
            print("mode: ", mode, file=f)
            self.stack = [ verbose_string(v) for v in ctx["stack"] ]
            print("stack:", self.stack, file=f)
            if self.contexts != []:
                print("other threads:", file=f)
                self.dump_contexts(f, self.tid)
            if len(self.shared) != 0:
                print("shared variables:", file=f)
                for k, v in self.shared.items():
                    print("  %s: %s"%(k, verbose_string(v)), file=f)
            print("state id: %s"%mas["id"], file=f)
            print("================================================", file=f)
            self.lastmis = mis[0]
            self.start = int(self.lastmis["pc"])
            if "shared" in self.lastmis:
                self.shared = self.lastmis["shared"]
            lastpc = 0
            self.steps = ""
        self.contexts = mas["contexts"]
        for step in mis:
            self.step += 1
            print(file=f)
            print("Step %d:"%self.step, file=f)
            print("  program counter:  ", step["pc"], file=f)
            print("  hvm code:          %s"%step["code"], file=f)
            # if (int(step["npc"]) != int(step["pc"]) + 1):
            #     print("  pc after:         ", step["npc"], file=f)
            if "interrupt" in step:
                print("  interrupted:       jump to interrupt handler first", file=f)
            else:
                print("  explanation:       %s"%step["explain"], file=f)
            loc = self.locations[int(step["pc"])]
            if loc["module"] != self.module:
                print("  module:            %s"%loc["module"], file=f)
                self.module = loc["module"]
            stmt = loc["stmt"]
            if stmt != self.stmt:
                print("  start statement:   line=%d column=%d"%(stmt[0], stmt[1]), file=f)
                print("  end statement:     line=%d column=%d"%(stmt[2], stmt[3]), file=f)
                self.stmt = stmt
            expr = tuple(int(loc[x]) for x in [ "line", "column", "endline", "endcolumn" ])
            if expr != self.expr:
                spaces = 0
                module = self.hvm["modules"][loc["module"]]
                code = module["lines"][int(loc["line"]) - 1]
                while spaces < len(code) and code[spaces] == ' ':
                    spaces += 1
                print("  source code:       %s"%code[spaces:], file=f)
                if stmt[0] == stmt[2] == expr[0] == expr[2]:
                    for _ in range(expr[1] + 20 - spaces):
                        print(" ", end="", file=f)
                    for _ in range(expr[3] - expr[1] + 1):
                        print("^", end="", file=f)
                    print(file=f)
                self.expr = expr
            else:
                print("  start expression:  line=%d column=%d"%(expr[0], expr[1]), file=f)
                print("  end expression:    line=%d column=%d"%(expr[2], expr[3]), file=f)
            # if "choose" in step:
            #     print("  chosen value:      %s"%verbose_string(step["choose"]), file=f)
            # if "print" in step:
            #     print("  print value:       %s"%verbose_string(step["print"]), file=f)
            if "shared" in step:
                print("  shared variables:  ", end="", file=f)
                verbose_print_vars(f, step["shared"])
                self.shared = step["shared"]
            if "local" in step:
                print("  method variables:  ", end="", file=f)
                verbose_print_vars(f, step["local"])
            if "trace" in step:
                print("  call trace:        ", end="", file=f)
                verbose_print_trace(f, step["trace"])
            if "mode" in step:
                print("  new mode:          %s"%step["mode"], file=f)
            if "interruptlevel" in step:
                print("  interrupt level:   %s"%step["interruptlevel"], file=f)
            stack_changed = False
            if "pop" in step:
                pop = int(step["pop"])
                if pop > 0:
                    stack_changed = True
                    self.stack = self.stack[:-int(step["pop"])]
            if "push" in step:
                push = [ verbose_string(v) for v in step["push"] ]
                if push != []:
                    stack_changed = True
                    self.stack += push
            if stack_changed:
                print("  stack:             [%s]"%", ".join(self.stack), file=f)
            if "failure" in step:
                print("  operation failed:  %s"%step["failure"], file=f)
            self.lastmis = step

    def run(self, outputfiles, behavior):
        with open(outputfiles["hco"], encoding='utf-8') as input:
          with open(outputfiles["hvb"], "w", encoding='utf-8') as output:
            top = json.load(input)
            assert isinstance(top, dict)
            if top["issue"] == "No issues":
                print("No issues were detected with this program.", file=output)
                return True

            print("Issue:", top["issue"], file=output)
            assert isinstance(top["macrosteps"], list)
            self.hvm = top["hvm"]

            print(file=output)
            print("Modules:", file=output)
            for modname, mod in self.hvm["modules"].items():
                print("  %s: %s"%(modname, mod["file"]), file=output)

            self.locations = self.hvm["locs"]
            for mes in top["macrosteps"]:
                self.print_macrostep(output, mes)

            print(file=output)
            print("================================================", file=output)
            print("Final state", file=output)
            print("================================================", file=output)
            print("Threads:", file=output)
            self.dump_contexts(output, None)
            print("Variables:", file=output)
            for k, v in self.shared.items():
                print("  %s: %s"%(k, verbose_string(v)), file=output)
