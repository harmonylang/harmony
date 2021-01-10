import json

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

def html_megastep(step, mas):
    print("<td>")
    print("  T%s: %s"%(mas["tid"], mas["name"]), end="")
    print("</td>")

    print("<td>")
    time = len(mas["microsteps"])
    nrows = (time + 29) // 30
    print("  <canvas id='timeline%d' width='300px' height='%dpx'>"%(step, 10*nrows))
    print("  </canvas>")
    print("</td>")

    print("<td align='center'>");
    print(mas["microsteps"][time - 1]["npc"])
    print("</td>")

    # print_vars(mas["shared"])
    print("<td>");
    print("</td>")

def html_top(top):
    print("<table border='1' id='mestable'>")
    print("  <thead>")
    print("    <tr>")
    print("      <th colspan='3' style='color:red;'>")
    print("        Issue:", top["issue"])
    print("      </th>")
    print("      <th rowspan='2' align='center'>")
    print("        Shared Variables")
    print("      </th>")
    print("    </tr>")

    print("    <tr>")
    print("      <th align='center'>")
    print("        Thread")
    print("      </th>")
    print("      <th align='center'>")
    print("        Steps")
    print("      </th>")
    print("      <th align='center'>")
    print("        &nbsp;PC&nbsp;")
    print("      </th>")
    print("    </tr>")
    print("  </thead>")

    print("  <tbody>")
    assert isinstance(top["megasteps"], list)
    for step, mes in enumerate(top["megasteps"]):
        print("    <tr>")
        html_megastep(step, mes)
        print("    </tr>")
    print("  </tbody>")
    print("</table>")

def html_bottom(top):
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
    for mes in top["megasteps"]:
        if int(mes["tid"]) > maxtid:
            maxtid = int(mes["tid"])
    for i in range(maxtid + 1):
        print("    <tr>")
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

def html_outer(top):
    print("<table>")
    print("  <tr>")
    print("    <td>")
    html_top(top)
    print("    </td>")
    print("  </tr>")
    print("  <tr>")
    print("    <td>")
    print("      &nbsp;")
    print("    </td>")
    print("  </tr>")
    print("  <tr>")
    print("    <td>")
    html_bottom(top)
    print("    </td>")
    print("  </tr>")
    print("</table>")

def html_script(top):
    print("<script>")
    print("var megasteps = [")
    for step, mes in enumerate(top["megasteps"]):
        print("  {")
        print("    canvas: document.getElementById('timeline%d'),"%step)
        print("    tid: %s,"%mes["tid"])
        print("    nsteps: %d"%len(mes["microsteps"]))
        print("  },")
    print("];")
    print("var state =")
    file_include("charm.json")
    print(";")
    file_include("charm.js")
    print("}")
    print("</script>")

def html_body():
    print("<body>")
    with open("charm.json") as f:
        top = json.load(f)
        assert isinstance(top, dict)
        html_outer(top)
        html_script(top)
    print("</body>")

def html():
    print("<html>")
    html_body()
    print("</html>")

html()
