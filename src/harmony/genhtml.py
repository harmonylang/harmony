class GenHTML:
    def __init__(self):
        self.top = {}
        self.nmegasteps = 0
        self.nmicrosteps = 0
        self.nthreads = 0
        self.vardir = {}

        self.style = """
m4_include(charm.css)
        """
        self.js = """
m4_include(charm.js)
        """

    def json_kv(self, js):
        return self.json_string(js["key"]) + ": " + self.json_string(js["value"])

    def json_idx(self, js):
        if js["type"] == "atom":
            return self.json_string(js)
        return "[" + self.json_string(js) + "]"

    def json_string(self, js):
        type = js["type"]
        v = js["value"]
        if type in { "bool", "int" }:
            return v
        if type == "atom":
            return "." + v
        if type == "set":
            if v == []:
                return "{}"
            return "{ " + ", ".join([ self.json_string(val) for val in v]) + " }"
        if type == "dict":
            if v == []:
                return "()"
            return "{ " + ", ".join([ self.json_kv(kv) for kv in v ]) + " }" 
        if type == "pc":
            return "PC(%s)"%v
        if type == "address":
            if v == []:
                return "None"
            return "?" + v[0]["value"] + "".join([ self.json_idx(kv) for kv in v[1:] ])
        if type == "context":
            return "CONTEXT(" + self.json_string(v["name"]) + ")"
        assert False

    def file_include(self, name, f):
        with open(name) as g:
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

        print("  <td align='center'>", file=f);
        print("  </td>", file=f)

        for i in range(width):
          print("  <td align='center'>", file=f)
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
                    if h == 0:
                        print("<td align='center' style='font-style: italic' colspan='%d' rowspan='%d'>%s</td>"%(w,nrows-nl,k), file=f)
                    else:
                        print("<td align='center' style='font-style: italic' colspan='%d'>%s</td>"%(w,k), file=f)
                    q.put((nd[k], nl+1))

    def html_top(self, f):
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
        print("    </tr>", file=f)

        print("    <tr>", file=f)
        print("      <th align='center' rowspan='%d'>"%height, file=f)
        print("        Step", file=f)
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
        alter = False;
        for pc, instr in enumerate(self.top["code"]):
            if str(pc) in self.top["locations"]:
                alter = not alter;
            print("        <tr id='P%d'>"%pc, file=f)
            print("          <td align='right'>", file=f)
            print("            <a name='P%d'>%d</a>&nbsp;"%(pc, pc), file=f)
            print("          </td>", file=f)
            print("          <td style='background-color: %s;'>"%("#E6E6E6" if alter else "white"), file=f)
            print("            <span title='%s' id='C%d'>"%(self.top["explain"][pc], pc), file=f)
            print("              %s"%instr, file=f);
            print("            </span>", file=f)
            print("          </td>", file=f)
            print("        </tr>", file=f)
        print("      </body>", file=f)
        print("    </table>", file=f)
        print("  </div>", file=f)
        print("</div>", file=f)

    def html_botright(self, f):
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

    def html_outer(self, f):
        print("<table>", file=f)
        print("  <tr>", file=f)
        print("    <td colspan='2'>", file=f)
        self.html_top(f)
        print("    </td>", file=f)
        print("  </tr>", file=f)
        print("  <tr><td></td></tr>", file=f)
        print("  <tr>", file=f)
        print("    <td colspan='2'>", file=f)
        print("      <h3 style='color:blue;' id='coderow'>CODE GOES HERE</h3>", file=f)
        print("    </td>", file=f)
        print("  </tr>", file=f)
        print("  <tr><td></td></tr>", file=f)
        print("  <tr>", file=f)
        print("    <td valign='top'>", file=f)
        self.html_botleft(f)
        print("    </td>", file=f)
        print("    <td valign='top'>", file=f)
        self.html_botright(f)
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

    def html_script(self, f):
        print("<script>", file=f)
        print("var nthreads = %d;"%self.nthreads, file=f)
        print("var nmegasteps = %d;"%self.nmegasteps, file=f)
        print("var vardir = [", file=f)
        self.vardir_dump(self.vardir, [], 0, f)
        print(file=f)
        print("];", file=f)
        print("var state =", file=f)
        self.file_include("charm.json", f)
        print(";", file=f)
        print(self.js, file=f)
        # file_include("charm.js", f)
        print("</script>", file=f)

    def html_body(self, f):
        print("<body>", file=f)
        self.html_outer(f)
        self.html_script(f)
        print("</body>", file=f)

    def html_head(self, f):
        print("<head>", file=f)
        print("  <style>", file=f)
        print(self.style, file=f)
        print("  </style>", file=f)
        print("</head>", file=f)

    def html(self, f):
        print("<html>", file=f)
        self.html_head(f)
        self.html_body(f)
        print("</html>", file=f)

    def var_convert(self, v):
        if v["type"] != "dict":
            return self.json_string(v)
        d = {}
        for kv in v["value"]:
            k = self.json_string(kv["key"])
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
            d[k] = self.var_convert(v)
        self.dict_merge(vardir, d)

    def run(self):
        # First figure out how many megasteps there are and how many threads
        lasttid = -1
        with open("charm.json") as f:
            self.top = json.load(f)
            assert isinstance(self.top, dict)
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

        with open("harmony.html", "w") as out:
            self.html(out)
