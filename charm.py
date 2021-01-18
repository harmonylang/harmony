import json
import queue

class Glob:
    def __init__(self, top):
        self.top = top                  # charm.json
        self.nmegasteps = 0
        self.nmicrosteps = 0
        self.nthreads = 0
        self.vardir = {}

style = """
#table-wrapper {
  position:relative;
}
#table-scroll {
  height:200px;
  overflow:auto;  
}
#table-wrapper table {
  width:100%;
}
#table-wrapper table * {
  color:black;
}
#table-wrapper table thead th .text {
  position:absolute;   
  top:-20px;
  z-index:2;
  height:20px;
  width:35%;
  border:1px solid red;
}
table {
    border-collapse: collapse;
    border-style: hidden;
}
table td, table th {
    border: 1px solid black;
}
"""

def json_kv(js):
    return json_string(js["key"]) + ": " + json_string(js["value"])

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
        return "dict{ " + ", ".join([ json_kv(kv) for kv in v ]) + " }" 
    if type == "pc":
        return "PC(%s)"%v
    if type == "address":
        if v == []:
            return "None"
        return "?" + v[0]["value"] + "".join([ json_idx(kv) for kv in v[1:] ])
    if type == "context":
        return "CONTEXT(" + json_string(v["name"]) + ")"
    assert False

def print_vars(d):
    print("<td>")
    first = True
    for k, v in d.items():
        if first:
            first = False
        else:
            print(",", end="")
        print(" %s: %s"%(k, json_string(v)), end="")
    print("</td>")

def print_range(mis, start, end, first):
    if not first:
        print(",", end="")
    if start + 1 == end:
        print("%s"%mis[start]["pc"], end="")
    else:
        print("%s-%s"%(mis[start]["pc"], mis[end-1]["pc"]), end="")

if False:
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
            print("(choose %s)"%json_string(mis[i]["choose"]), end="")
        elif int(mis[i]["pc"]) != int(mis[i-1]["pc"]) + 1:
            print_range(mis, start, i, first)
            first = False
            start = i
    print_range(mis, start, len(mis), first)
    print("] ", end="")

def file_include(name):
    with open(name) as f:
        print(f.read())

def html_megastep(glob, step, tid, name, nmicrosteps, width):
    print("<tr id='mes%d'>"%(step-1))
    print("  <td align='right'>")
    print("    %d&nbsp;"%step)
    print("  </td>")

    print("  <td>")
    print("    T%s: %s"%(tid, name), end="")
    print("  </td>")

    print("  <td>")
    time = nmicrosteps
    nrows = (time + 29) // 30
    print("    <canvas id='timeline%d' width='300px' height='%dpx'>"%(step-1, 10*nrows))
    print("    </canvas>")
    print("  </td>")

    print("  <td align='center'>");
    print("  </td>")

    # print_vars(mas["shared"])
    for i in range(width):
      print("  <td>")
      print("  </td>")
    print("</tr>")

def vardim(d):
    totalwidth = 0
    maxheight = 0
    if isinstance(d, dict):
        for k in sorted(d.keys()):
            (w, h) = vardim(d[k])
            totalwidth += w
            if h + 1 > maxheight:
                maxheight = h + 1
    else:
        return (1, 0)
    return (totalwidth, maxheight)

def varhdr(d, name, nrows):
    q = queue.Queue()
    level = 0
    q.put((d, level))
    while not q.empty():
        (nd, nl) = q.get()
        if nl > level:
            print("</tr><tr>")
            level = nl
        if isinstance(nd, dict):
            for k in sorted(nd.keys()):
                (w,h) = vardim(nd[k])
                if h == 0:
                    print("<td align='center' style='font-style: italic' colspan='%d' rowspan='%d'>%s</td>"%(w,nrows-nl,k))
                else:
                    print("<td align='center' style='font-style: italic' colspan='%d'>%s</td>"%(w,k))
                q.put((nd[k], nl+1))

def html_top(glob):
    (width, height) = vardim(glob.vardir)
    print("<table border='1'>")
    print("  <thead>")
    print("    <tr>")
    print("      <th colspan='4' style='color:red;'>")
    print("        Issue:", glob.top["issue"])
    print("      </th>")
    print("      <th align='center' colspan='%d'>"%width)
    print("        Shared Variables")
    print("      </th>")
    print("    </tr>")

    print("    <tr>")
    print("      <th align='center' rowspan='%d'>"%height)
    print("        Step")
    print("      </th>")
    print("      <th align='center' rowspan='%d'>"%height)
    print("        Thread")
    print("      </th>")
    print("      <th align='center' rowspan='%d'>"%height)
    print("        Instructions")
    print("      </th>")
    print("      <th align='center' rowspan='%d'>"%height)
    print("        &nbsp;PC&nbsp;")
    print("      </th>")
    varhdr(glob.vardir, "", height)
    print("    </tr>")
    print("  </thead>")

    print("  <tbody id='mestable'>")
    assert isinstance(glob.top["macrosteps"], list)
    nsteps = 0
    tid = None
    name = None
    nmicrosteps = 0
    for mas in glob.top["macrosteps"]:
        if tid == mas["tid"]:
            nmicrosteps += len(mas["microsteps"])
        else:
            if tid != None:
                html_megastep(glob, nsteps, tid, name, nmicrosteps, width)
            nsteps += 1
            tid = mas["tid"]
            name = mas["name"]
            nmicrosteps = len(mas["microsteps"])
    html_megastep(glob, nsteps, tid, name, nmicrosteps, width)
    print("  </tbody>")
    print("</table>")

def html_botleft(glob):
    print("<div id='table-wrapper'>")
    print("  <div id='table-scroll'>")
    print("    <table border='1'>")
    print("      <tbody>")
    for pc, instr in enumerate(glob.top["code"]):
        print("        <tr id='P%d'>"%pc)
        print("          <td align='right'>")
        print("            <a name='P%d'>%d</a>&nbsp;"%(pc, pc))
        print("          </td>")
        print("          <td>")
        print("            <span title='%s' id='C%d'>"%(glob.top["explain"][pc], pc))
        print("              %s"%instr);
        print("            </span>")
        print("          </td>")
        print("        </tr>")
    print("      </body>")
    print("    </table>")
    print("  </div>")
    print("</div>")

def html_botright(glob):
    print("<table border='1' id='threadtable'>")
    print("  <thead>")
    print("    <tr>")
    print("      <th>")
    print("        Thread")
    print("      </th>")
    print("      <th>")
    print("        Status")
    print("      </th>")
    print("      <th>")
    print("        Stack Trace")
    print("      </th>")
    print("    </tr>")
    print("  </thead>")
    print("  <tbody>")
    maxtid = 0
    for i in range(glob.nthreads):
        print("    <tr id='thread%d'>"%i)
        print("      <td align='center'>")
        print("        T%d"%i)
        print("      </td>")
        print("      <td align='center'>")
        print("        init")
        print("      </td>")
        print("      <td>")
        print("        <table id='threadinfo%d' border='1'>"%i)
        print("        </table>")
        print("      </td>")
        print("    </tr>")
    print("  </tbody>")
    print("</table>")

def html_outer(glob):
    print("<table>")
    print("  <tr>")
    print("    <td colspan='2'>")
    html_top(glob)
    print("    </td>")
    print("  </tr>")
    print("  <tr>")
    print("    <td colspan='2'>")
    print("      <h2 style='color:blue;' id='coderow'>CODE GOES HERE</h2>")
    print("    </td>")
    print("  </tr>")
    print("  <tr>")
    print("    <td valign='top'>")
    html_botleft(glob)
    print("    </td>")
    print("    <td valign='top'>")
    html_botright(glob)
    print("    </td>")
    print("  </tr>")
    print("</table>")

def vardir_dump(d, path, index):
    if isinstance(d, dict):
        for k in sorted(d.keys()):
            index = vardir_dump(d[k], path + [k], index)
        return index
    if index > 0:
        print(",")
    print("  " + str(path), end="")
    return index + 1

def html_script(glob):
    print("<script>")
    print("var nthreads = %d;"%glob.nthreads)
    print("var nmegasteps = %d;"%glob.nmegasteps)
    print("var vardir = [")
    vardir_dump(glob.vardir, [], 0)
    print()
    print("];")
    print("var state =")
    file_include("charm.json")
    print(";")
    file_include("charm.js")
    print("</script>")

def html_body(glob):
    print("<body>")
    html_outer(glob)
    html_script(glob)
    print("</body>")

def html_head():
    print("<head>")
    print("  <style>")
    print(style)
    print("  </style>")
    print("</head>")

def html(glob):
    print("<html>")
    html_head()
    html_body(glob)
    print("</html>")

def var_convert(v):
    if v["type"] != "dict":
        return json_string(v)
    d = {}
    for kv in v["value"]:
        k = json_string(kv["key"])
        d[k] = var_convert(kv["value"])
    return d

def dict_merge(vardir, d):
    for (k, v) in d.items():
        if not isinstance(v, dict):
            vardir[k] = v
        elif v != {}:
            if k not in vardir:
                vardir[k] = {}
            elif not isinstance(vardir[k], dict):
                continue
            dict_merge(vardir[k], v)

def vars_add(vardir, shared):
    d = {}
    for (k, v) in shared.items():
        d[k] = var_convert(v)
    dict_merge(vardir, d)

def main():
    # First figure out how many megasteps there are and how many threads
    lasttid = -1
    with open("charm.json") as f:
        glob = Glob(json.load(f))
        assert isinstance(glob.top, dict)
        macrosteps = glob.top["macrosteps"]
        for mas in macrosteps:
            tid = int(mas["tid"])
            if tid >= glob.nthreads:
                glob.nthreads = tid + 1
            if tid != lasttid:
                glob.nmegasteps += 1
                lasttid = tid
            glob.nmicrosteps += len(mas["microsteps"])
            for mis in mas["microsteps"]:
                if "shared" in mis:
                    vars_add(glob.vardir, mis["shared"])

    html(glob)

main()
