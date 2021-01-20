import json
import queue

class GenHTML:
    def __init__(self):
        self.top = {}
        self.nmegasteps = 0
        self.nmicrosteps = 0
        self.nthreads = 0
        self.vardir = {}

        self.style = """
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
        self.js = """
var boxSize = 10;
var currentTime = 0;
var totalTime = 0;
var microsteps = [];
var megasteps = []
var threads = [];
var curMegaStep = 0;
var mestable = document.getElementById("mestable");
var threadtable = document.getElementById("threadtable");
var coderow = document.getElementById("coderow");
var container = document.getElementById('table-scroll');
var currOffset = 0;
var currCloc = null;

function drawTimeLine(mes) {
  var c = mes.canvas.getContext("2d");
  c.beginPath();
  c.clearRect(0, 0, mes.canvas.width, mes.canvas.height);
  var t = mes.startTime;
  var yboxes = Math.floor((mes.nsteps + 29) / 30);
  for (var y = 0; y < yboxes; y++) {
    var xboxes = y < yboxes - 1 ? 30 : (mes.nsteps % 30);
    for (var x = 0; x < xboxes; x++) {
      c.fillStyle = t < currentTime ? "orange" : "white";
      c.fillRect(x * boxSize, y * boxSize, boxSize, boxSize);
      c.rect(x * boxSize, y * boxSize, boxSize, boxSize);
      c.stroke();
      t += 1;
    }
  }
}

function currentMegaStep() {
  if (currentTime == totalTime) {
    return microsteps[currentTime - 1].mesidx;
  }
  return microsteps[currentTime].mesidx;
}

function json_string_set(obj) {
  var result = "";
  for (var i = 0; i < obj.length; i++) {
    if (result != "") {
      result += ", ";
    }
    result += json_string(obj[i]);
  }
  return "{ " + result + " }";
}

function json_string_dict(obj) {
  if (obj.length == 0) {
    return "()"
  }
  var result = "";
  for (var i = 0; i < obj.length; i++) {
    if (result != "") {
      result += ", ";
    }
    var kv = obj[i];
    var k = json_string(kv.key);
    var v = json_string(kv.value);
    result += k + ": " + v;
  }
  return "dict{ " + result + " }";
}

function json_string_address(obj) {
  result = "?" + obj[0].value;
  for (var i = 1; i < obj.length; i++) {
    if (obj[i].type == "atom") {
      result += "." + obj[i].value;
    }
    else {
      result += "[" + json_string(obj[i]) + "]";
    }
  }
  return result;
}

function json_string(obj) {
  switch (obj.type) {
  case "bool": case "int":
    return obj.value;
    break;
  case "atom":
    return "." + obj.value;
  case "set":
    return json_string_set(obj.value);
  case "dict":
    return json_string_dict(obj.value);
  case "pc":
    return "PC(" + obj.value + ")"
  case "address":
    return json_string_address(obj.value);
  default:
    return JSON.stringify(obj);
  }
}

function stringify_vars(obj) {
  var result = "";
  for (var k in obj) {
    if (result != "") {
      result += ", ";
    }
    result += k + ": " + json_string(obj[k]);
  }
  return result;
}

function convert_var(obj) {
  if (obj.type != "dict") {
    return json_string(obj);
  }
  result = {};
  for (var i = 0; i < obj.value.length; i++) {
    var kv = obj.value[i];
    var k = json_string(kv.key);
    result[k] = convert_var(kv.value);
  }
  return result;
}

function convert_vars(obj) {
  var result = {};
  for (var k in obj) {
    result[k] = convert_var(obj[k]);
  }
  return result;
}

function stackTrace(table, trace, failure) {
  table.innerHTML = "";
  for (var i = 0; i < trace.length; i++) {
    var row = table.insertRow();

    var mcell = row.insertCell();
    mcell.innerHTML = trace[i].method;
    switch (trace[i].calltype) {
    case "process":
        mcell.style.color = "blue";
        break;
    case "normal":
        mcell.style.color = "black";
        break;
    case "interrupt":
        mcell.style.color = "orange";
        break;
    default:
        mcell.style.color = "red";
    }

    var vcell = row.insertCell();
    var vtext = document.createTextNode(stringify_vars(trace[i].vars));
    vcell.appendChild(vtext);
  }
  if (failure != null) {
    var row = table.insertRow();
    var fcell = row.insertCell();
    fcell.innerHTML = failure;
    fcell.colSpan = 2;
    fcell.style.color = "red";
  }
}

function handleClick(e, mesIdx) {
  var x = Math.floor(e.offsetX / boxSize);
  var y = Math.floor(e.offsetY / boxSize);
  currentTime = megasteps[mesIdx].startTime + y*30 + x + 1;
  run_microsteps()
}

var noloc = { file: "", line: "", code: "" };

function getCode(pc) {
  var locs = state.locations;
  while (pc >= 0) {
    s = "" + pc;
    if (locs.hasOwnProperty(s)) {
      return locs[s];
    }
    pc--;
  }
  return noloc;
}

function handleKeyPress(e) {
  switch (e.key) {
    case '0':
      currentTime = 0;
      run_microsteps();
      break;
    case 'ArrowLeft':
      if (currentTime > 0) {
        currentTime -= 1;
      }
      run_microsteps();
      break;
    case 'ArrowRight':
      if (currentTime < totalTime) {
        currentTime += 1;
      }
      run_microsteps();
      break;
    case 'ArrowUp':
      var mesidx = currentMegaStep();
      var mes = megasteps[mesidx];
      if (currentTime == mes.startTime && mesidx > 0) {
          mes = megasteps[mesidx - 1];
      }
      currentTime = mes.startTime;
      run_microsteps();
      break;
    case 'ArrowDown':
      var mesidx = currentMegaStep();
      var mes = megasteps[mesidx];
      currentTime = mes.startTime + mes.nsteps;
      if (currentTime > totalTime) {
        currentTime = totalTime;
      }
      run_microsteps();
      break;
    case 'Enter':
      if (currentTime < totalTime) {
        var cloc = getCode(microsteps[currentTime].pc);
        while (++currentTime < totalTime) {
          var nloc = getCode(microsteps[currentTime].pc);
          if (nloc != cloc) {
            break;
          }
        }
        run_microsteps();
      }
      break;
    default:
      // alert("unknown key " + e.code);
  }
}

function init_microstep(masidx, misidx) {
  var mas = state.macrosteps[masidx];
  var mis = mas.microsteps[misidx];
  var t = microsteps.length;
  if (t > 0 && microsteps[t - 1].tid != mas.tid) {
    curMegaStep++;
    megasteps[curMegaStep].startTime = t;
  }
  var mes = megasteps[curMegaStep];
  mes.nsteps++;
  microsteps[t] = {
    mesidx: curMegaStep,
    masidx: masidx,
    misidx: misidx,
    tid: parseInt(mas.tid),
    pc: parseInt(mis.pc),
    invfails: misidx == mas.microsteps.length - 1 ? mas.invfails : [],
    contexts: mas.contexts
  };

  if (mis.hasOwnProperty("npc")) {
    microsteps[t].npc = mis.npc;
  }
  else {
    microsteps[t].npc = mis.pc;
  }

  microsteps[t].code = getCode(microsteps[t].npc);

  microsteps[t].cloc = document.getElementById('C' + microsteps[t].npc);
  var npc = microsteps[t].npc - 4;
  if (npc < 0) {
    npc = 0;
  }
  microsteps[t].offset = document.getElementById('P' + npc);

  if (mis.hasOwnProperty("mode")) {
    microsteps[t].mode = mis.mode;
  }
  else {
    microsteps[t].mode = misidx == 0 ? "running" : microsteps[t-1].mode;
  }

  if (mis.hasOwnProperty("atomic")) {
    microsteps[t].atomic = mis["atomic"];
  }
  else if (misidx == 0) {
    microsteps[t].atomic = 0;
  }
  else {
    microsteps[t].atomic = microsteps[t-1].atomic;
  }

  if (mis.hasOwnProperty("readonly")) {
    microsteps[t].readonly = mis["readonly"];
  }
  else if (misidx == 0) {
    microsteps[t].readonly = 0;
  }
  else {
    microsteps[t].readonly = microsteps[t-1].readonly;
  }

  if (mis.hasOwnProperty("interruptlevel")) {
    microsteps[t].interruptlevel = mis["interruptlevel"];
  }
  else if (misidx == 0) {
    microsteps[t].interruptlevel = 0;
  }
  else {
    microsteps[t].interruptlevel = microsteps[t-1].interruptlevel;
  }

  if (mis.hasOwnProperty("choose")) {
    microsteps[t].choose = "chose " + json_string(mis["choose"]);
  }
  else {
    microsteps[t].choose = null;
  }

  if (mis.hasOwnProperty("failure")) {
    microsteps[t].failure = mis.failure;
    microsteps[t].cloc = null;
  }
  else {
    microsteps[t].failure = null;
  }

  if (mis.hasOwnProperty("trace")) {
    microsteps[t].trace = mis.trace;
  }
  else if (misidx == 0) {
    microsteps[t].trace = [];
  }
  else {
    microsteps[t].trace = microsteps[t-1].trace;
  }

  // Update local variables
  if (microsteps[t].trace.length > 0 && mis.hasOwnProperty("local")) {
    // deep copy first
    microsteps[t].trace = JSON.parse(JSON.stringify(microsteps[t].trace))
    microsteps[t].trace[0].vars = mis.local;
  }

  if (mis.hasOwnProperty("shared")) {
    microsteps[t].shared = convert_vars(mis.shared);
  }
  else if (t == 0) {
    microsteps[t].shared = {};
  }
  else {
    microsteps[t].shared = microsteps[t-1].shared;
  }
}

function init_macrostep(i) {
  var mas = state.macrosteps[i];
  for (var j = 0; j < mas.microsteps.length; j++) {
    init_microstep(i, j);
  }
}

function get_shared(shared, path) {
  if (!shared.hasOwnProperty(path[0])) {
    return "";
  }
  if (path.length == 1) {
    return shared[path[0]];
  }
  return get_shared(shared[path[0]], path.slice(1));
}

function get_status(ctx) {
  var status = ctx.mode;
  if (status != "terminated") {
    if (ctx.atomic > 0) {
      status += " atomic";
    }
    if (ctx.readonly > 0) {
      status += " read-only";
    }
    if (ctx.interruptlevel > 0) {
      status += " interrupts-disabled";
    }
  }
  return status;
}

function run_microstep(t) {
  var mis = microsteps[t];
  var mesrow = mestable.rows[mis.mesidx];
  mesrow.cells[3].innerHTML = mis.npc;

  for (var i = 0; i < vardir.length; i++) {
    mesrow.cells[i + 4].innerHTML = get_shared(mis.shared, vardir[i])
  }

  if (mis.failure != null) {
    stackTrace(threads[mis.tid].tracetable, mis.trace, mis.failure);
  }
  else {
    stackTrace(threads[mis.tid].tracetable, mis.trace, mis.choose);
  }

  for (var ctx = 0; ctx < mis.contexts.length; ctx++) {
    var tid = parseInt(mis.contexts[ctx].tid);
    threadtable.rows[tid + 1].cells[1].innerHTML = get_status(mis.contexts[ctx]);
  }
  var mes = megasteps[mis.mesidx];
  if (t != mes.startTime + mes.nsteps - 1) {
    threadtable.rows[mis.tid + 1].cells[1].innerHTML = get_status(mis);
  }

  if (mis.invfails.length > 0) {
    inv = mis.invfails[0];
    code = getCode(inv.pc);
    coderow.style.color = "red";
    coderow.innerHTML = code.file + ":" + code.line + "&nbsp;&nbsp;&nbsp;" + code.code + " (" + inv.reason + ")";
    mis.cloc = null;
  }
  else {
    coderow.style.color = "blue";
    coderow.innerHTML = mis.code.file + ":" + mis.code.line + "&nbsp;&nbsp;&nbsp;" + mis.code.code;
  }

  currCloc = mis.cloc;
  currOffset = mis.offset;
}

function run_microsteps() {
  coderow.innerHTML = "";
  if (currCloc != null) {
    currCloc.style.color = "black";
    currCloc = null;
  }
  for (var i = 0; i < nmegasteps; i++) {
    mestable.rows[i].cells[3].innerHTML = "";
    for (var j = 0; j < vardir.length; j++) {
      mestable.rows[i].cells[j + 4].innerHTML = "";
    }
  }
  for (var i = 0; i < nthreads; i++) {
    threadtable.rows[i + 1].cells[1].innerHTML = "init";
    stackTrace(threads[i].tracetable, [], null);
  }
  for (var t = 0; t < currentTime; t++) {
    run_microstep(t);
  }
  for (var i = 0; i < nmegasteps; i++) {
    drawTimeLine(megasteps[i]);
  }
  container.scrollTop = currOffset.offsetTop;

  if (currCloc != null) {
    currCloc.style.color = "red";
  }

  var curmes = microsteps[currentTime == 0 ? 0 : (currentTime-1)].mesidx;
  for (var mes = 0; mes < nmegasteps; mes++) {
    var row = document.getElementById("mes" + mes)
    if (mes == curmes) {
      row.style = 'background-color: #A5FF33;';
    }
    else {
      row.style = 'background-color: white;';
    }
  }

  var curtid = microsteps[currentTime == 0 ? 0 : (currentTime-1)].tid;
  for (var tid = 0; tid < nthreads; tid++) {
    var row = document.getElementById("thread" + tid)
    if (tid == curtid) {
      row.style = 'background-color: #A5FF33;';
    }
    else {
      row.style = 'background-color: white;';
    }
  }
}

// Initialization starts here

for (var tid = 0; tid < nthreads; tid++) {
  threads[tid] = {
    status: "normal",
    stacktrace: [],
    tracetable: document.getElementById("threadinfo" + tid)
  };
}
for (let i = 0; i < nmegasteps; i++) {
  var canvas = document.getElementById("timeline" + i);
  megasteps[i] = {
    canvas: canvas,
    startTime: 0,
    nsteps: 0,
    contexts: []
  };
  canvas.addEventListener('mousedown', function(e){handleClick(e, i)});
}
for (var j = 0; j < state.macrosteps.length; j++) {
  init_macrostep(j);
}

currentTime = totalTime = microsteps.length;
run_microsteps();
document.addEventListener('keydown', handleKeyPress);
        """

    def json_kv(self, js):
        return json_string(js["key"]) + ": " + json_string(js["value"])

    def json_idx(self, js):
        if js["type"] == "atom":
            return json_string(js)
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
            return "{ " + ", ".join(v) + " }"
        if type == "dict":
            if v == []:
                return "()"
            return "dict{ " + ", ".join([ self.json_kv(kv) for kv in v ]) + " }" 
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
        totalwidth = 0
        maxheight = 0
        if isinstance(d, dict):
            for k in sorted(d.keys()):
                (w, h) = self.vardim(d[k])
                totalwidth += w
                if h + 1 > maxheight:
                    maxheight = h + 1
        else:
            return (1, 0)
        return (totalwidth, maxheight)

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
        print("<table border='1' id='threadtable'>", file=f)
        print("  <thead>", file=f)
        print("    <tr>", file=f)
        print("      <th>", file=f)
        print("        Thread", file=f)
        print("      </th>", file=f)
        print("      <th>", file=f)
        print("        Status", file=f)
        print("      </th>", file=f)
        print("      <th>", file=f)
        print("        Stack Trace", file=f)
        print("      </th>", file=f)
        print("    </tr>", file=f)
        print("  </thead>", file=f)
        print("  <tbody>", file=f)
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
        print("  <tr>", file=f)
        print("    <td colspan='2'>", file=f)
        print("      <h3 style='color:blue;' id='coderow'>CODE GOES HERE</h3>", file=f)
        print("    </td>", file=f)
        print("  </tr>", file=f)
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
        if isinstance(d, dict):
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
            elif v != {}:
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
            glob = GenHTML()
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

if __name__ == "__main__":
    gh = GenHTML()
    gh.run()
