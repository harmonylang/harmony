import json
import os
import queue
from pathlib import Path

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

    def file_include(self, name, f):
        with open(name, encoding='utf-8') as g:
            print(g.read(), file=f)

    def html_megastep(self, step, tid, name, nmicrosteps, width, f):
        print("<tr id='mes%d'>"%(step-1), file=f)
        print("  <td align='right'>", file=f)
        print("    %d&nbsp;"%step, file=f)
        print("  </td>", file=f)

        print("  <td>", file=f)
        print("    T%s: %s"%(tid, name), file=f, end="")
        print("  </td>", file=f)

        print("  <td>", file=f)
        time = nmicrosteps
        nrows = (time + 29) // 30
        print("    <canvas id='timeline%d' width='300px' height='%dpx'>"%(step-1, 10*nrows), file=f)
        print("    </canvas>", file=f)
        print("  </td>", file=f)

        print("  <td align='center'>", file=f)
        print("  </td>", file=f)

        for i in range(width):
          print("  <td align='center'>", file=f)
          print("  </td>", file=f)

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

    def varhdr(self, d, name, nrows, f):
        q = queue.Queue()
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
            print("        Issue:", self.top["issue"], file=f)
            print("      </th>", file=f)
            print("    </tr>", file=f)
            print("</table>", file=f)
            return

        (width, height) = self.vardim(self.vardir)
        print("<table border='1'>", file=f)
        print("  <thead>", file=f)
        print("    <tr>", file=f)
        print("      <th colspan='4' style='color:red;'>", file=f)
        print("        Issue:", self.top["issue"], file=f)
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
        print("        Turn", file=f)
        print("      </th>", file=f)
        print("      <th align='center' rowspan='%d'>"%height, file=f)
        print("        Thread", file=f)
        print("      </th>", file=f)
        print("      <th align='center' rowspan='%d'>"%height, file=f)
        print("        Instructions Executed", file=f)
        print("      </th>", file=f)
        print("      <th align='center' rowspan='%d'>"%height, file=f)
        print("        &nbsp;PC&nbsp;", file=f)
        print("      </th>", file=f)
        self.varhdr(self.vardir, "", height, f)
        print("    </tr>", file=f)
        print("  </thead>", file=f)

        print("  <tbody id='mestable'>", file=f)
        assert isinstance(self.top["macrosteps"], list)
        nsteps = 0
        tid = None
        name = None
        nmicrosteps = 0
        for mas in self.top["macrosteps"]:
            if tid == mas["tid"]:
                nmicrosteps += len(mas["microsteps"])
            else:
                if tid != None:
                    self.html_megastep(nsteps, tid, name, nmicrosteps, width, f)
                nsteps += 1
                tid = mas["tid"]
                name = mas["name"]
                nmicrosteps = len(mas["microsteps"])
        self.html_megastep(nsteps, tid, name, nmicrosteps, width, f)
        print("  </tbody>", file=f)
        print("</table>", file=f)

    def html_botleft(self, f):
        print("<div id='table-wrapper'>", file=f)
        print("  <div id='table-scroll'>", file=f)
        print("    <table border='1'>", file=f)
        print("      <tbody>", file=f)
        alter = False
        for pc, instr in enumerate(self.top["code"]):
            if str(pc) in self.top["locations"]:
                alter = not alter
            print("        <tr id='P%d'>"%pc, file=f)
            print("          <td align='right'>", file=f)
            print("            <a name='P%d'>%d</a>&nbsp;"%(pc, pc), file=f)
            print("          </td>", file=f)
            print("          <td style='background-color: %s;'>"%("#E6E6E6" if alter else "white"), file=f)
            print("            <span title='%s' id='C%d'>"%(self.top["explain"][pc], pc), file=f)
            print("              %s"%instr, file=f)
            print("            </span>", file=f)
            print("          </td>", file=f)
            print("        </tr>", file=f)
        print("      </body>", file=f)
        print("    </table>", file=f)
        print("  </div>", file=f)
        print("</div>", file=f)

    # output a filename of f1 relative to f2
    def pathdiff(self, f1, f2):
        return os.path.relpath(f1, start=os.path.dirname(f2))

    def html_botright(self, f, outputfiles):
        if self.nthreads == 0:
            png = outputfiles["png"]
            if png != None:
                if png[0] == "/":
                    print("      <img src='%s' alt='DFA image'>"%png, file=f)
                else:
                    assert outputfiles["htm"] != None
                    print("      <img src='%s' alt='DFA image'>"%self.pathdiff(png, outputfiles["htm"]), file=f)
            return
        print("<table border='1'", file=f)
        print("  <thead>", file=f)
        print("    <tr>", file=f)
        print("      <th colspan='4'>Threads</th>", file=f)
        print("    </tr>", file=f)
        print("    <tr>", file=f)
        print("      <th>", file=f)
        print("        ID", file=f)
        print("      </th>", file=f)
        print("      <th>", file=f)
        print("        Status", file=f)
        print("      </th>", file=f)
        print("      <th>", file=f)
        print("        Stack Trace", file=f)
        print("      </th>", file=f)
        print("      <th>", file=f)
        print("        Stack Top", file=f)
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
            print("      <td align='left'>", file=f)
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
        print("  <tr><td></td></tr>", file=f)
        print("  <tr>", file=f)
        print("    <td colspan='2'>", file=f)
        print("      <h3 style='color:blue;'>", file=f)
        print("        <div id='coderow'>", file=f)
        print("        </div>", file=f)
        print("      </h3>", file=f)
        print("    </td>", file=f)
        print("  </tr>", file=f)
        print("  <tr><td></td></tr>", file=f)
        print("  <tr>", file=f)
        print("    <td valign='top'>", file=f)
        self.html_botleft(f)
        print("    </td>", file=f)
        print("    <td valign='top'>", file=f)
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
            if val != {}:
                d[k] = val
        self.dict_merge(vardir, d)

    def run(self, outputfiles):
        # First figure out how many megasteps there are and how many threads
        lasttid = -1
        with open(outputfiles["hco"], encoding='utf-8') as f:
            self.top = json.load(f)
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
