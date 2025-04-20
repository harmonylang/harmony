import json
import os
import queue
from pathlib import Path
from typing import Any, Tuple
from harmony_model_checker.harmony.jsonstring import json_string

class GenHTML:
    def __init__(self):
        self.top = {}
        self.nmegasteps = 0
        self.nmicrosteps = 0
        self.nthreads = 0
        self.vardir = {}
        self_dir = Path(__file__).parent
        self.style = (self_dir / "charm.css").read_text()
        self.js = (self_dir / "charm.js").read_text()
        self.timeWidth = 40
        self.tickers = []

    def file_include(self, name, f):
        with open(name, encoding='utf-8') as g:
            print(g.read(), file=f)

    def html_megastep(self, step, tid, name, microsteps, time, width, f):
        print("<tr id='mes%d'>"%(step-1), file=f)

        # Turn
        print("  <td align='right'>", file=f)
        print("    %d&nbsp;"%step, file=f)
        print("  </td>", file=f)

        # Thread
        print("  <td>", file=f)
        print("    T%s: %s"%(tid, name), file=f, end="")
        print("  </td>", file=f)

        # Execution
        print("  <td>", file=f)
        print("    <table border='0' style='max-width:%dpx; word-wrap: break-word;'>"%(self.timeWidth * 10), file=f)
        nmicrosteps = len(microsteps)
        nrows = (nmicrosteps + self.timeWidth - 1) // self.timeWidth
        print("      <tr><td><canvas id='timeline%d' width='%dpx' height='%dpx'>"%(step-1, self.timeWidth*10, 10*nrows), file=f)
        print("      </canvas></td></tr>", file=f)
        print("      <tr><td><table class='table-transparent' id='thisstep%d'>"%(step-1), file=f)
        for (t, mis) in enumerate(microsteps):
            if "interrupt" in mis and mis["explain"]:
                print("         <tr><td><input type='radio' id='radio%d' onclick='goto_time(%d)'><a onclick='goto_time(%d)'>"%(idx, idx, idx), file=f);
                print("Interrupt", file=f)
                print("</a></td></tr>", file=f)
                continue
            pc = int(mis["pc"])
            op = self.code[pc]["op"]
            idx = len(self.tickers)
            if op in { "Store", "Print", "Choose" }:
                print("         <tr><td><input type='radio' id='radio%d' onclick='goto_time(%d)'><a onclick='goto_time(%d)'>"%(idx, idx, idx), file=f);
                exp = mis["explain2"]["args"]
                if op == "Store":
                    if len(exp) == 0:
                        print("Store with bad address", file=f)
                    else:
                        assert len(exp) == 2, mis["explain2"]
                        print("Set <span id='var%d'>%s</span> to <span id='val%d'>%s</span>"%(idx, json_string(exp[1])[1:], idx, json_string(exp[0])), file=f)
                elif op == "Print":
                    print("Print <span id='val%d'>%s</span>"%(idx, json_string(exp[0])), file=f)
                elif op == "Choose":
                    print("Choose <span id='val%d'>%s</span>"%(idx, json_string(mis["choose"])), file=f)
                print("</a></td></tr>", file=f)
                self.tickers.append(time+t)
        print("      </table></td></tr>", file=f)
        print("      <tr><td id='nextstep%d'></td></tr>"%(step-1), file=f)
        print("    </table>", file=f)
        print("  </td>", file=f)

        # PC
        print("  <td align='center'><div id='PC%d'>"%(step-1), file=f)
        print("  </div></td>", file=f)

        # Shared variables
        for i in range(width):
          print("  <td align='center'>", file=f)
          print("  </td>", file=f)

        # Output
        print("  <td>", file=f)
        print("    <table id='log%d' border='1'>"%(step-1), file=f)
        print("    </table>", file=f)
        print("  </td>", file=f)
        print("</tr>", file=f)

    def vardim(self, d):
        if isinstance(d, dict):
            if d == {}:
                return (1, 0)
            totalwidth = 0
            maxheight = 0
            for k in sorted(d.keys()):
                (w, h) = self.vardim(d[k])
                totalwidth += w
                if h + 1 > maxheight:
                    maxheight = h + 1
            return (totalwidth, maxheight)
        else:
            return (1, 0)

    def varhdr(self, d: dict, name, nrows, f):
        q: 'queue.Queue[Tuple[dict, int]]' = queue.Queue()
        level = 0
        q.put((d, level))
        while not q.empty():
            (nd, nl) = q.get()
            if nl > level:
                print("</tr><tr>", file=f)
                level = nl
            if isinstance(nd, dict):
                for k in sorted(nd.keys()):
                    (w,h) = self.vardim(nd[k])
                    if k[0] == '"':
                        key = k[1:-1]
                    else:
                        key = k
                    if h == 0:
                        print("<td align='center' style='font-style: italic' colspan='%d' rowspan='%d'>%s</td>"%(w,nrows-nl,key), file=f)
                    else:
                        print("<td align='center' style='font-style: italic' colspan='%d'>%s</td>"%(w,key), file=f)
                    q.put((nd[k], nl+1))

    def html_top(self, f):
        if "macrosteps" not in self.top:
            print("<table border='1'>", file=f)
            print("  <thead>", file=f)
            print("    <tr>", file=f)
            print("      <th colspan='4' style='color:red;'>", file=f)
            print("        Issue: %s"%self.top["issue"], file=f)
            print("      </th>", file=f)
            print("    </tr>", file=f)
            print("  </thead>", file=f)
            print("</table>", file=f)
            return

        (width, height) = self.vardim(self.vardir)
        print("<table border='1'>", file=f)
        print("  <thead>", file=f)
        print("    <tr>", file=f)
        print("      <th colspan='4'>", file=f)
        print("        <table border='0'><tr><td>", file=f)
        print("          <button id='details-button' type='button' onclick='toggle_details()'>Hide details</button>", file=f)
        print("        </td><td style='color:red;'>", file=f)
        print("          &nbsp;&nbsp;&nbsp;&nbsp;<a onclick='explain_issue(\"%s\")'>Issue: %s <sup>&#9432;</sup></a></span>"%(self.top["issue"], self.top["issue"]), file=f)
        print("        </td></tr></table>", file=f)
        # if "invpc" in self.top:
        #     print("        (Line %d)"%self.top["hvm"]["locs"][self.top["invpc"]]["line"], file=f)
        print("      </th>", file=f)
        print("      <th align='center' colspan='%d'>"%width, file=f)
        print("        Shared Variables", file=f)
        print("      </th>", file=f)
        print("      <th align='center' colspan='%d'>"%width, file=f)
        print("        Output", file=f)
        print("      </th>", file=f)
        print("    </tr>", file=f)

        print("    <tr>", file=f)
        print("      <th align='center' rowspan='%d'>"%height, file=f)
        print("        <a onclick='explain_turn()'>Turn<sup>&#9432;</sup></a></span>", file=f)
        print("      </th>", file=f)
        print("      <th align='center' rowspan='%d'>"%height, file=f)
        print("        Thread", file=f)
        print("      </th>", file=f)
        print("      <th align='center' rowspan='%d'>"%height, file=f)
        print("        Execution", file=f)
        print("      </th>", file=f)
        print("      <th align='center' rowspan='%d'><div id='PChdr'>"%height, file=f)
        print("        &nbsp;PC&nbsp;", file=f)
        print("      </div></th>", file=f)
        self.varhdr(self.vardir, "", height, f)
        print("    </tr>", file=f)
        print("  </thead>", file=f)

        print("  <tbody id='mestable'><form>", file=f)
        assert isinstance(self.top["macrosteps"], list)
        nsteps = 0
        tid = None
        name = None
        microsteps = []
        time = 0
        for mas in self.top["macrosteps"]:
            if tid == mas["tid"]:
                microsteps += mas["microsteps"]
            else:
                if tid is not None:
                    self.html_megastep(nsteps, tid, name, microsteps, time, width, f)
                    time += len(microsteps)
                nsteps += 1
                tid = mas["tid"]
                name = mas["name"]
                microsteps = mas["microsteps"]
        self.html_megastep(nsteps, tid, name, microsteps, time, width, f)
        print("  </form></tbody>", file=f)
        print("</table>", file=f)

    def html_botleft(self, f):
        print("<div id='HVMcode'>", file=f)
        print(" <h3 align='center'>Harmony bytecode</h3>", file=f)
        print(" <div id='table-wrapper'>", file=f)
        print("  <div id='table-scroll'>", file=f)
        print("    <table border='1'>", file=f)
        print("      <tbody>", file=f)
        alter = False
        pretty = self.top["hvm"]["pretty"]
        for pc, instr in enumerate(pretty):
            # if str(pc) in self.top["locations"]:  TODO: why was this here??
            alter = not alter
            print("        <tr id='P%d'>"%pc, file=f)
            print("          <td align='right'>", file=f)
            print("            <a name='P%d'>%d</a>&nbsp;"%(pc, pc), file=f)
            print("          </td>", file=f)
            print("          <td style='background-color: %s;'>"%("#E6E6E6" if alter else "white"), file=f)
            print("            <span title='%s' id='C%d'>"%(instr[1], pc), file=f)
            print("              %s"%instr[0], file=f)
            print("            </span>", file=f)
            print("          </td>", file=f)
            print("        </tr>", file=f)
        print("      </body>", file=f)
        print("    </table>", file=f)
        print("  </div>", file=f)
        print(" </div>", file=f)
        print("</div>", file=f)

    # output a filename of f1 relative to f2
    def pathdiff(self, f1, f2):
        return os.path.relpath(f1, start=os.path.dirname(f2))

    def html_botright(self, f, outputfiles):
        if self.nthreads == 0:
            png = outputfiles["png"]
            if png is not None:
                if png[0] == "/":
                    print("      <img src='%s' alt='DFA image'>"%png, file=f)
                else:
                    assert outputfiles["htm"] is not None
                    print("      <img src='%s' alt='DFA image'>"%self.pathdiff(png, outputfiles["htm"]), file=f)
            return
        print("<table border='1'", file=f)
        print("  <thead>", file=f)
        print("    <tr>", file=f)
        print("      <th colspan='4'>Threads</th>", file=f)
        print("    </tr>", file=f)
        print("    <tr>", file=f)
        print("      <th>", file=f)
        print("        &nbsp;ID&nbsp;", file=f)
        print("      </th>", file=f)
        print("      <th>", file=f)
        print("        &nbsp;<a onclick='explain_status()'>Status <sup>&#9432;</sup></a>", file=f)
        print("      </th>", file=f)
        print("      <th>", file=f)
        print("        &nbsp;<a onclick='explain_stacktrace()'>Stack Trace <sup>&#9432;</sup></a>", file=f)
        print("      </th>", file=f)
        print("      <th id='StackTopHdr'>", file=f)
        print("        &nbsp;Stack Top&nbsp;", file=f)
        print("      </th>", file=f)
        print("    </tr>", file=f)
        print("  </thead>", file=f)
        print("  <tbody id='threadtable'>", file=f)
        maxtid = 0
        for i in range(self.nthreads):
            print("    <tr id='thread%d'>"%i, file=f)
            print("      <td align='center'>", file=f)
            print("        T%d"%i, file=f)
            print("      </td>", file=f)
            print("      <td align='center'>", file=f)
            print("        init", file=f)
            print("      </td>", file=f)
            print("      <td>", file=f)
            print("        <table id='threadinfo%d' border='1'>"%i, file=f)
            print("        </table>", file=f)
            print("      </td>", file=f)
            print("      <td align='left' id='stacktop%d'>"%i, file=f)
            print("      </td>", file=f)
            print("    </tr>", file=f)
        print("  </tbody>", file=f)
        print("</table>", file=f)

    def html_outer(self, f, outputfiles):
        print("<table>", file=f)
        print("  <tr>", file=f)
        print("    <td colspan='2'>", file=f)
        self.html_top(f)
        print("    </td>", file=f)
        print("  </tr>", file=f)
        print("  <tr><td colspan='2'></td></tr>", file=f)
        print("  <tr>", file=f)
        print("    <td colspan='2'>", file=f)
        print("      <h3 style='color:blue;'>", file=f)
        print("        <div id='coderow'>", file=f)
        print("        </div>", file=f)
        print("      </h3>", file=f)
        print("    </td>", file=f)
        print("  </tr>", file=f)
        print("  <tr><td></td><td></td></tr>", file=f)
        print("  <tr>", file=f)
        print("    <td valign='top'>", file=f)
        self.html_botleft(f)
        print("    </td>", file=f)
        print("    <td valign='top' class='dynamic-hidden-col'>", file=f)
        self.html_botright(f, outputfiles)
        print("    </td>", file=f)
        print("  </tr>", file=f)
        print("</table>", file=f)

    def vardir_dump(self, d, path, index, f):
        if isinstance(d, dict) and d != {}:
            for k in sorted(d.keys()):
                index = self.vardir_dump(d[k], path + [k], index, f)
            return index
        if index > 0:
            print(",", file=f)
        print("  " + str(path), end="", file=f)
        return index + 1

    def html_script(self, f, outputfiles):
        print("<script>", file=f)
        print("var nthreads = %d;"%self.nthreads, file=f)
        print("var nmegasteps = %d;"%self.nmegasteps, file=f)
        print("var vardir = [", file=f)
        self.vardir_dump(self.vardir, [], 0, f)
        print(file=f)
        print("];", file=f)
        print("var state =", file=f)
        self.file_include(outputfiles["hco"], f)
        print(";", file=f)
        print("var tickers = %s;"%self.tickers, file=f)
        print(self.js, file=f)
        # file_include("charm.js", f)
        print("</script>", file=f)

    def html_body(self, f, outputfiles):
        print("<body>", file=f)
        self.html_outer(f, outputfiles)
        self.html_script(f, outputfiles)
        print("</body>", file=f)

    def html_head(self, f):
        print("<head>", file=f)
        print("  <meta charset='UTF-8'></meta>", file=f)
        print("  <style>", file=f)
        print(self.style, file=f)
        print("  </style>", file=f)
        print("</head>", file=f)

    def html(self, f, outputfiles):
        print("<html>", file=f)
        self.html_head(f)
        self.html_body(f, outputfiles)
        print("</html>", file=f)

    def var_convert(self, v):
        if v["type"] != "dict":
            return json_string(v)
        for kv in v["value"]:
            k = kv["key"]
            if k["type"] != "atom" and k["type"] != "int" and k["type"] != "bool":
                return json_string(v)
        d = {}
        for kv in v["value"]:
            k = json_string(kv["key"])
            d[k] = self.var_convert(kv["value"])
        return d

    def dict_merge(self, vardir, d):
        for (k, v) in d.items():
            if not isinstance(v, dict):
                vardir[k] = v
            else:
                if k not in vardir:
                    vardir[k] = {}
                elif not isinstance(vardir[k], dict):
                    continue
                self.dict_merge(vardir[k], v)

    def vars_add(self, vardir, shared):
        d = {}
        for (k, v) in shared.items():
            val = self.var_convert(v)
            # if val != {}:
            d[k] = val
        self.dict_merge(vardir, d)

    def run(self, outputfiles):
        # First figure out how many megasteps there are and how many threads
        lasttid = -1
        with open(outputfiles["hco"], encoding='utf-8') as f:
            self.top = json.load(f, strict=False)
            self.code = self.top["hvm"]["code"]
            assert isinstance(self.top, dict)
            if "macrosteps" in self.top:
                macrosteps = self.top["macrosteps"]
                for mas in macrosteps:
                    tid = int(mas["tid"])
                    if tid >= self.nthreads:
                        self.nthreads = tid + 1
                    if tid != lasttid:
                        self.nmegasteps += 1
                        lasttid = tid
                    self.nmicrosteps += len(mas["microsteps"])
                    for mis in mas["microsteps"]:
                        if "shared" in mis:
                            self.vars_add(self.vardir, mis["shared"])
                    for ctx in mas["contexts"]:
                        tid = int(ctx["tid"])
                        if tid >= self.nthreads:
                            self.nthreads = tid + 1

        with open(outputfiles["htm"], "w", encoding='utf-8') as out:
            self.html(out, outputfiles)
