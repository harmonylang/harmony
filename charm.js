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

function drawTimeLine(mes) {
  var c = mes.canvas.getContext("2d");
  c.beginPath();
  c.clearRect(0, 0, mes.canvas.width, mes.canvas.height);
  var t = mes.startTime;
  var yboxes = Math.floor((mes.nsteps + 29) / 30);
  for (var y = 0; y < yboxes; y++) {
    var xboxes = y < yboxes - 1 ? 30 : (mes.nsteps % 30);
    for (var x = 0; x < xboxes; x++) {
      if (t >= currentTime) {
        c.fillStyle = "white";
        c.fillRect(x * boxSize, y * boxSize, boxSize, boxSize);
        c.rect(x * boxSize, y * boxSize, boxSize, boxSize);
        c.stroke();
      }
      else {
        c.fillStyle = "black";
        c.fillRect(x * boxSize, y * boxSize, boxSize, boxSize);
      }
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
  return "{ " + result + " }";
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

function stackTrace(table, trace, failure) {
  table.innerHTML = "";
  for (var i = 0; i < trace.length; i++) {
    var row = table.insertRow();

    var mcell = row.insertCell();
    var mtext = document.createTextNode(trace[i].method);
    mcell.appendChild(mtext);

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

function handleKeyPress(e) {
  switch (e.key) {
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
    default:
      // alert("unknown key " + e.code);
  }
}

function getCode(pc) {
  locs = state.locations;
  while (pc >= 0 ) {
    s = "" + pc;
    if (locs.hasOwnProperty(s)) {
      return locs[s];
    }
    pc -= 1;
  }
  return { file: "", line: "", code: "" };
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
    contexts: mas.contexts
  };

  if (mis.hasOwnProperty("npc")) {
    microsteps[t].npc = mis.npc;
  }
  else {
    microsteps[t].npc = mis.pc;
  }

  microsteps[t].code = getCode(microsteps[t].npc);
  var rowToScrollTo = document.getElementById('P' + microsteps[t].npc);
  microsteps[t].offset = rowToScrollTo.offsetTop; 

  if (mis.hasOwnProperty("mode")) {
    microsteps[t].mode = mis.mode;
  }
  else {
    microsteps[t].mode = t == mes.startTime ? "running" : microsteps[t-1].mode;
  }

  if (mis.hasOwnProperty("failure")) {
    microsteps[t].failure = mis.failure;
  }
  else {
    microsteps[t].failure = null;
  }

  if (mis.hasOwnProperty("trace")) {
    microsteps[t].trace = mis.trace;
  }
  else if (t == 0) {
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
    microsteps[t].shared = stringify_vars(mis.shared);
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

function run_microstep(t) {
  var mis = microsteps[t];
  var mesrow = mestable.rows[mis.mesidx + 2];
  mesrow.cells[3].innerHTML = mis.npc;
  mesrow.cells[4].innerHTML = mis.shared;

  stackTrace(threads[mis.tid].tracetable, mis.trace, mis.failure);

  for (var ctx = 0; ctx < mis.contexts.length; ctx++) {
    var tid = parseInt(mis.contexts[ctx].tid);
    threadtable.rows[tid + 1].cells[1].innerHTML = mis.contexts[ctx].mode;
  }
  var mes = megasteps[mis.mesidx];
  if (t != mes.startTime + mes.nsteps - 1) {
    threadtable.rows[mis.tid + 1].cells[1].innerHTML = mis.mode;
  }

  coderow.innerHTML = mis.code.file + "/" + mis.code.line + ": " + mis.code.code;

  // window.location.href = "#P" + mis.npc;
  currOffset = mis.offset;
}

function run_microsteps() {
  for (var i = 0; i < nmegasteps; i++) {
    mestable.rows[i + 2].cells[3].innerHTML = "";
    mestable.rows[i + 2].cells[4].innerHTML = "";
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
  container.scrollTop = currOffset;
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
