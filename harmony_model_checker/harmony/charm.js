var boxSize = 10;
var timeWidth = 40;
var currentTime = 0;
var totalTime = 0;
var microsteps = [];
var megasteps = []
var threads = [];
var curMegaStep = 0;
var mestable = document.getElementById("mestable");
var threadtable = document.getElementById("threadtable");
var coderow = document.getElementById("coderow");
// var hvmrow = document.getElementById("hvmrow");
var container = document.getElementById('table-scroll');
var currOffset = 0;
var currCloc = null;

// printing contexts
var contexts = {};
var ctxGen = 0;

function json_string_list(obj) {
  var result = "";
  for (var i = 0; i < obj.length; i++) {
    if (result != "") {
      result += ", ";
    }
    result += json_string(obj[i]);
  }
  return "[ " + result + " ]";
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
    return "{:}"
  }

  var islist = true;
  for (var i = 0; i < obj.length; i++) {
    if (obj[i].key.type != "int" || obj[i].key.value != i.toString()) {
      islist = false;
      break;
    }
  }

  var result = "";
  if (islist) {
    for (var i = 0; i < obj.length; i++) {
      if (i != 0) {
        result += ", ";
      }
      result += json_string(obj[i].value);
    }
    if (obj.length == 1) {
      result += ",";
    }
    return "[" + result + "]";
  }

  for (var i = 0; i < obj.length; i++) {
    if (result != "") {
      result += ", ";
    }
    var kv = obj[i];
    var k = json_string(kv.key);
    var v = json_string(kv.value);
    result += k + ": " + v;
  }
  return "{ " + result + " }";
}

function json_string_address(func, args) {
  var result = "?";
  var index = 0;
  if (func.type == "pc") {
    if (func.value == -1 || func.value == -2) {
      result += args[0].value;
      index = 1;
    }
    else if (func.value == -3) {
      result += "this." + args[0].value;
      index = 1;
    }
    else {
      result += json_string(func);
    }
  }
  else {
    result += json_string(func);
  }
  for (var i = index; i < args.length; i++) {
    result += "[" + json_string(args[i]) + "]";
  }
  return result;
}

function json_string_context(obj) {
  // TODO.  Is JSON.stringify deterministic (same context --> same string)?
  var key = JSON.stringify(obj);
  if (!(key in contexts)) {
    contexts[key] = ++ctxGen;
  }
  var output = '<span title="CONTEXT\n';
  if ("id" in obj) {
    output += "id: " + json_string(obj["id"]) + "\n";
  }
  output += "pc: " + json_string(obj["pc"]) + "\n";
  output += "vars: " + stringify_vars(obj["vars"]) + "\n";
  var atomic = "atomic" in obj && obj["atomic"]["value"] == "True";
  var stopped = "stopped" in obj && obj["stopped"]["value"] == "True";
  if (atomic || stopped) {
    output += "mode:"
    if (atomic) output += " atomic";
    if (stopped) output += " stopped";
    output += "\n";
  }
  output += "sp: " + json_string(obj["sp"]);
  return output + '" style="color:blue">C' + contexts[key] + '</span>';

  // var pc = json_string(obj.pc);
  // return "CTX(" + pc + ")";
}

function json_string(obj) {
  switch (obj.type) {
  case "bool": case "int":
    return obj.value;
  case "atom":
    return '"' + obj.value + '"';
  case "set":
    return json_string_set(obj.value);
  case "list":
    return json_string_list(obj.value);
  case "dict":
    return json_string_dict(obj.value);
  case "pc":
    return "PC(" + obj.value + ")"
  case "address":
    if ("func" in obj) {
      return json_string_address(obj.func, obj.args);
    }
    return "None";
  case "context":
    return json_string_context(obj.value);
  default:
    return JSON.stringify(obj);
  }
}

var noloc = { file: "", line: "", code: "" };

function getCode(pc) {
  var loc = state.hvm.locs[pc];
  var module = state.hvm.modules[loc.module];
  loc.file = module.file;
  loc.code = module.lines[loc.line - 1];
  return loc;
//  var locs = state.locations;
//  while (pc >= 0) {
//    s = "" + pc;
//    if (locs.hasOwnProperty(s)) {
//      return locs[s];
//    }
//    pc--;
//  }
//  return noloc;
}

function drawTimeLine(mes) {
  var c = mes.canvas.getContext("2d");
  c.beginPath();
  c.clearRect(0, 0, mes.canvas.width, mes.canvas.height);
  var t = mes.startTime;
  var yboxes = Math.floor((mes.nsteps + timeWidth - 1) / timeWidth);
  var nsteps = mes.nsteps;
  for (var y = 0; y < yboxes; y++) {
    var xboxes = nsteps > timeWidth ? timeWidth : nsteps;
    for (var x = 0; x < xboxes; x++) {
      c.fillStyle = t < currentTime ? "orange" : "white";
      c.fillRect(x * boxSize, y * boxSize, boxSize, boxSize);
      c.rect(x * boxSize, y * boxSize, boxSize, boxSize);
      c.stroke();
      t += 1;
    }
    nsteps -= xboxes;
  }
  mes.nextstep.innerHTML = "";
  return t;
}

function updateStatus(mes) {
  for (var i = 0; i < mes.contexts.length; i++) {
    var c = mes.contexts[i];
    if (c.tid == mes.tid) {
      if (c.mode == "terminated") {
        mes.nextstep.innerHTML = "terminated"
      }
      else if (c.hasOwnProperty("next")) {
        switch (c.next.type) {
        case "Continue":
          var loc = getCode(c.pc);
          mes.nextstep.innerHTML = "stopped in " + '<a href="' + loc.file + '">' + loc.module + "</a>:" + loc.line;
          break;
        case "Store":
          mes.nextstep.innerHTML = "about to store " + json_string(c.next.value) + " in variable " + c.next.var;
          break;
        case "Load":
          mes.nextstep.innerHTML = "about to load variable " + c.next.var;
          break;
        case "Assert":
          var loc = getCode(c.pc);
          mes.nextstep.innerHTML = "assertion failed in " + '<a href="' + loc.file + '">' + loc.module + "</a>:" + loc.line + ":" + loc.code;
          mes.nextstep.style.color = "red";
          break;
        case "AtomicInc":
          var loc = getCode(c.pc);
          mes.nextstep.innerHTML = "about to execute in " + '<a href="' + loc.file + '">' + loc.module + "</a>:" + loc.line + ":" + loc.code;
          break;
        case "Print":
          mes.nextstep.innerHTML = "about to print " + json_string(c.next.value);
          break;
        default:
           mes.nextstep.innerHTML = "about to " + state.hvm.pretty[c.pc][1];
        }
      }
      break;
    }
  }
}

function currentMegaStep() {
  if (currentTime == totalTime) {
    return microsteps[currentTime - 1].mesidx;
  }
  return microsteps[currentTime].mesidx;
}

function stringify_vars(obj) {
  var result = "";
  for (var k in obj) {
    if (false && k == "result" && obj[k].type == "address" && !("func" in obj)) {
      continue;
    }
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
  if (obj.value.length == 0) {
    return "";
  }
  var result = {};
  for (var i = 0; i < obj.value.length; i++) {
    var kv = obj.value[i];
    var k = json_string(kv.key);      // TODO.  convert_var???
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

function stackTrace(tid, trace, failure) {
  var table = threads[tid].tracetable;
  table.innerHTML = "";
  if (trace.length == 0) {
    var row = table.insertRow();
    var mcell = row.insertCell();
    mcell.innerHTML = threads[tid].name;
  }
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
    // var vtext = document.createTextNode(stringify_vars(trace[i].vars));
    var vtext = document.createElement("div");
    vtext.innerHTML = stringify_vars(trace[i].vars);
    vcell.appendChild(vtext);
  }
  if (false && failure != null) {
    var row = table.insertRow();
    var fcell = row.insertCell();
    fcell.innerHTML = failure;
    fcell.colSpan = 2;
    fcell.style.color = "red";
  }
}

function addToLog(step, entry) {
  var table = megasteps[step].log;
  var row = table.insertRow();
  var mcell = row.insertCell();
  mcell.innerHTML = entry;
}

function handleClick(e, mesIdx) {
  var x = Math.floor(e.offsetX / boxSize);
  var y = Math.floor(e.offsetY / boxSize);
  currentTime = megasteps[mesIdx].startTime + y*timeWidth + x + 1;
  run_microsteps();
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
          if (nloc.file != cloc.file || nloc.line != cloc.line || nloc.code != cloc.code) {
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
  var tid = mas.tid;
  var t = microsteps.length;
  megasteps[curMegaStep].contexts = mas.contexts;
  if (t > 0 && microsteps[t - 1].tid != tid) {
    curMegaStep++;
    megasteps[curMegaStep].startTime = t;
    megasteps[curMegaStep].tid = tid;
  }
  var mes = megasteps[curMegaStep];
  mes.nsteps++;
  microsteps[t] = {
    mesidx: curMegaStep,
    masidx: masidx,
    misidx: misidx,
    tid: parseInt(tid),
    pc: parseInt(mis.pc),
    // invfails: misidx == mas.microsteps.length - 1 ? mas.invfails : [],
    contexts: mas.contexts,
    hvm: mis.code,
    explain: mis.explain
  };
  if (misidx != 0) {
    previous = microsteps[t-1];
  }
  else {
    ctx = mas.context;
    previous = { mode: ctx.mode, };
    if (ctx.hasOwnProperty("atomic")) {
      previous.atomic = ctx["atomic"];
    }
    else {
      previous.atomic = 0;
    }
    if (ctx.hasOwnProperty("readonly")) {
      previous.readonly = ctx["readonly"];
    }
    else {
      previous.readonly = 0;
    }
    if (ctx.hasOwnProperty("interruptlevel")) {
      previous.interruptlevel = ctx["interruptlevel"];
    }
    else {
      previous.interruptlevel = 0;
    }
    if (ctx.hasOwnProperty("trace")) {
      previous.trace = ctx.trace;
    }
    else {
      previous.trace = [];
    }
    if (ctx.hasOwnProperty("fp")) {
      previous.fp = ctx.fp;
    }
    else {
      previous.fp = 0;
    }
    if (ctx.hasOwnProperty("stack")) {
      previous.stack = ctx.stack.map(x => json_string(x));
    }
    else {
      previous.stack = [];
    }
    if (mas.hasOwnProperty("shared")) {
      previous.shared = convert_vars(mas.shared);
    }
    else {
      previous.shared = {};
    }
  }

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
    microsteps[t].mode = previous.mode;
  }

  if (mis.hasOwnProperty("atomic")) {
    microsteps[t].atomic = mis["atomic"];
  }
  else {
    microsteps[t].atomic = previous.atomic;
  }

  if (mis.hasOwnProperty("readonly")) {
    microsteps[t].readonly = mis["readonly"];
  }
  else {
    microsteps[t].readonly = previous.readonly;
  }

  if (mis.hasOwnProperty("interruptlevel")) {
    microsteps[t].interruptlevel = mis["interruptlevel"];
  }
  else {
    microsteps[t].interruptlevel = previous.interruptlevel;
  }

  if (mis.hasOwnProperty("choose")) {
    microsteps[t].choose = "chose " + json_string(mis["choose"]);
  }
  else {
    microsteps[t].choose = null;
  }
  if (mis.hasOwnProperty("print")) {
    microsteps[t].print = json_string(mis["print"]);
  }
  else {
    microsteps[t].print = null;
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
  else {
    microsteps[t].trace = previous.trace;
  }

  // Update local variables
  var trl = microsteps[t].trace.length; 
  if (trl > 0 && mis.hasOwnProperty("local")) {
    // deep copy first
    microsteps[t].trace = JSON.parse(JSON.stringify(microsteps[t].trace));
    microsteps[t].trace[trl - 1].vars = mis.local;
  }

  if (mis.hasOwnProperty("shared")) {
    microsteps[t].shared = convert_vars(mis.shared);
  }
  else {
    microsteps[t].shared = previous.shared;
  }

  if (mis.hasOwnProperty("fp")) {
    microsteps[t].fp = mis.fp;
  }
  else {
    microsteps[t].fp = previous.fp;
  }
  if (mis.hasOwnProperty("pop")) {
    var n = parseInt(mis.pop);
    microsteps[t].stack = previous.stack.slice(0,
                              previous.stack.length - n);
  }
  else {
    microsteps[t].stack = previous.stack;
  }
  if (mis.hasOwnProperty("push")) {
    var vals = mis.push.map(x => json_string(x));
    microsteps[t].stack = microsteps[t].stack.concat(vals);
  }
}

function init_macrostep(i) {
  var mas = state.macrosteps[i];
  for (var j = 0; j < mas.microsteps.length; j++) {
    init_microstep(i, j);
  }
  for (var ctx = 0; ctx < mas.contexts.length; ctx++) {
    var tid = parseInt(mas.contexts[ctx].tid);
    threads[tid].name = mas.contexts[ctx].name;
  }
}

function dict_convert(d) {
  if (typeof d === "string") {
    return d;
  }
  result = "";
  for (var k in d) {
    if (result != "") {
      result += ", ";
    }
    result += dict_convert(k) + ":" + dict_convert(d[k]);;
  }
  return "{" + result + "}";
}

function get_shared(shared, path) {
  if (!shared.hasOwnProperty(path[0])) {
    return "";
  }
  if (path.length == 1) {
    return dict_convert(shared[path[0]]);
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

function escapeHTML(s) {
  return s
     .replace(/&/g, "&amp;")
     .replace(/</g, "&lt;")
     .replace(/>/g, "&gt;")
     .replace(/"/g, "&quot;")
     .replace(/'/g, "&#039;");
}

function run_microstep(t) {
  var mis = microsteps[t];
  var mes = megasteps[mis.mesidx];
  var mesrow = mestable.rows[mis.mesidx];
  mesrow.cells[3].innerHTML = mis.npc;

  for (var i = 0; i < vardir.length; i++) {
    mesrow.cells[i + 4].innerHTML = get_shared(mis.shared, vardir[i]);
  }

  if (mis.failure != null) {
    stackTrace(mis.tid, mis.trace, mis.failure);
  }
  else if (mis.print != null) {
    stackTrace(mis.tid, mis.trace, "print " + mis.print);
    addToLog(mis.mesidx, mis.print);
  }
  else {
    stackTrace(mis.tid, mis.trace, mis.choose);
  }

  for (var ctx = 0; ctx < mis.contexts.length; ctx++) {
    var cv = mis.contexts[ctx];
    var tid = parseInt(cv.tid);
    threads[tid].name = cv.name;
    threadtable.rows[tid].cells[1].innerHTML = get_status(cv);
    threadtable.rows[tid].cells[3].innerHTML = cv.stack.slice(cv.fp).map(x => json_string(x));
  }
  if (t != mes.startTime + mes.nsteps - 1) {
    threadtable.rows[mis.tid].cells[1].innerHTML = get_status(mis);
  }
  threadtable.rows[mis.tid].cells[3].innerHTML = mis.stack.slice(mis.fp);

//  if (mis.invfails.length > 0) {
//    var inv = mis.invfails[0];
//    code = getCode(inv.pc);
//    coderow.style.color = "red";
//    coderow.innerHTML = '<a href="' + code.file + '">' + code.module + "</a>:" + code.line + "&nbsp;&nbsp;&nbsp;" + escapeHTML(code.code) + " (" + inv.reason + ")";
//    mis.cloc = null;
//  }
//  else
    {
    coderow.style.color = "blue";
    if (t+1 < microsteps.length) {
      var nmis = microsteps[t+1];
      code = getCode(nmis.pc);
      var l1 = parseInt(code.line);
      var l2 = parseInt(code.endline);
      if (l1 == l2 && l1 == code.stmt[0] && l2 == code.stmt[2]) {
        var c1 = parseInt(code.column) - 1;
        var c2 = parseInt(code.endcolumn);
        var s1 = code.code.slice(0, c1);
        var s2 = code.code.slice(c1, c2);
        var s3 = code.code.slice(c2);
        coderow.innerHTML = '<a href="' + code.file + '">' + code.module + "</a>:" + code.line + "&nbsp;&nbsp;&nbsp;" + escapeHTML(s1) + "<span style='color:green'>" + escapeHTML(s2) + "</span>" + escapeHTML(s3);
      }
      else {
        coderow.innerHTML = '<a href="' + code.file + '">' + code.module + "</a>:" + code.line + "&nbsp;&nbsp;&nbsp;" + escapeHTML(code.code);
      }
    }
  }

  if (mis.failure != null) {
    mes.nextstep.innerHTML = '<span style="color:red">' + mis.failure + '</span>';
  }
  else if (t+1 < microsteps.length) {
    var nmis = microsteps[t+1];
    if (nmis.tid == mis.tid) {
        mes.nextstep.innerHTML = "next: " + nmis.explain;
    }
    else {
        updateStatus(mes);
    }

    // hvmrow.innerHTML = "T" + nmis.tid + "/" + nmis.pc + ": " + nmis.hvm + " (" + nmis.explain + ")"
    currCloc = document.getElementById('C' + nmis.pc);
    currOffset = document.getElementById('P' + nmis.pc);
  }
  else {
    currCloc = null;
    currOffset = mis.offset;
    updateStatus(mes);
  }
}

function run_microsteps() {
  coderow.innerHTML = "";
  // hvmrow.innerHTML = "";
  if (currCloc != null) {
    currCloc.style.color = "black";
  }
  currCloc = document.getElementById('C0');
  currOffset = document.getElementById('P0');
  for (var i = 0; i < nmegasteps; i++) {
    mestable.rows[i].cells[3].innerHTML = "";
    for (var j = 0; j < vardir.length; j++) {
      mestable.rows[i].cells[j + 4].innerHTML = "";
    }
    megasteps[i].log.innerHTML = "";
  }
  for (var tid = 0; tid < nthreads; tid++) {
    threadtable.rows[tid].cells[1].innerHTML = "init";
    stackTrace(tid, [], null);
    threadtable.rows[tid].cells[3].innerHTML = threads[tid].stack;
  }

  for (var i = 0; i < nmegasteps; i++) {
    drawTimeLine(megasteps[i]);
  }
  for (var t = 0; t < currentTime; t++) {
    run_microstep(t);
  }
  if (currentTime < microsteps.length && (currentTime == 0 ||
            microsteps[currentTime - 1].tid != microsteps[currentTime].tid)) {
    var mis = microsteps[currentTime];
    var mes = megasteps[mis.mesidx];
    mes.nextstep.innerHTML = "next: " + mis.explain;
    var mesrow = mestable.rows[mis.mesidx];
    mesrow.cells[3].innerHTML = mis.pc;

    if (mis.mesidx > 0) {
      var oldrow = mestable.rows[mis.mesidx - 1];
      for (var i = 0; i < vardir.length; i++) {
        mesrow.cells[i + 4].innerHTML = oldrow.cells[i + 4].innerHTML;
      }
    }
  }
  container.scrollTop = currOffset.offsetTop;

  if (currCloc != null) {
    currCloc.style.color = "red";
  }

  var curmes = currentTime < totalTime ? microsteps[currentTime].mesidx : -1;
  for (var mes = 0; mes < nmegasteps; mes++) {
    var row = document.getElementById("mes" + mes);
    if (mes == curmes) {
      row.style = 'background-color: #A5FF33;';
    }
    else {
      row.style = 'background-color: white;';
    }
  }

  var curtid = currentTime < totalTime ? microsteps[currentTime].tid : -1;
  for (var tid = 0; tid < nthreads; tid++) {
    var row = document.getElementById("thread" + tid);
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
    name: "T" + tid,
    status: "normal",
    stack: [],
    stacktrace: [],
    tracetable: document.getElementById("threadinfo" + tid)
  };
}
threads[0].stack = [ "()" ]
for (let i = 0; i < nmegasteps; i++) {
  var canvas = document.getElementById("timeline" + i);
  var nextstep = document.getElementById("nextstep" + i); 
  megasteps[i] = {
    canvas: canvas,
    nextstep: nextstep,
    startTime: 0,
    nsteps: 0,
    contexts: [],
    tid: 0,
    log: document.getElementById("log" + i)
  };
  canvas.addEventListener('mousedown', function(e){handleClick(e, i)});
}
for (var j = 0; j < state.macrosteps.length; j++) {
  init_macrostep(j);
}

currentTime = totalTime = microsteps.length;
run_microsteps();
document.addEventListener('keydown', handleKeyPress);
