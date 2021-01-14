var boxSize = 10;
var currentTime = 0;
var totalTime = 0;
var microsteps = [];
var megasteps = []
var threads = [];
var curMegaStep = 0;
var mestable = document.getElementById("mestable");
var threadtable = document.getElementById("threadtable");

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
  for (var i = 0; i < megasteps.length; i++) {
    var mes = megasteps[i];
    if (mes.startTime + mes.nsteps >= currentTime) {
      return i;
    }
  }
  alert("currentMegaStep");
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
    return json_string_dict(obj.value);
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

function stringify(obj) {
  var result = "";
  for (var k in obj) {
    if (result != "") {
      result += ", ";
    }
    result += k + ": " + json_string(obj[k]);
  }
  return result;
}

function getShared(time) {
  var shared = "";
  for (var mesidx = 0; mesidx < state.megasteps.length; mesidx++) {
    var mes = state.megasteps[mesidx];
    for (var misidx = 0; misidx < mes.microsteps.length; misidx++) {
      if (time == 0) {
        return shared;
      }
      if (mes.microsteps[misidx].hasOwnProperty("shared")) {
        shared = stringify(mes.microsteps[misidx].shared);
      }
      time -= 1;
    }
  }
  return shared;
}

function stackTrace(table, trace, failure) {
  table.innerHTML = "";
  for (var i = 0; i < trace.length; i++) {
    var row = table.insertRow();

    var mcell = row.insertCell();
    var mtext = document.createTextNode(trace[i].method);
    mcell.appendChild(mtext);

    var vcell = row.insertCell();
    // var vtext = document.createTextNode(stringify(trace[i].vars));
    // vcell.appendChild(vtext);
    vcell.innerHTML = "yyy";
  }
  if (failure != null) {
    var row = table.insertRow();
    var fcell = row.insertCell();
    fcell.innerHTML = failure;
    fcell.colSpan = 2;
    fcell.style.color = "red";
  }
}

function drawTimeLines() {
  for (var i = 0;; i++) {
    var y = document.getElementById("threadinfo" + i);
    if (y == null) {
        break;
    }
    stackTrace(y, [], null);

    var z = document.getElementById("threadtable").rows[i+1].cells;
    z[1].innerHTML = "init"
  }
  for (var i = 0; i < megasteps.length; i++) {
    var mes = megasteps[i];
    drawTimeLine(mes);
    var microsteps = state.megasteps[i].microsteps;
    var x = document.getElementById("mestable").rows[i+2].cells;
    var y = document.getElementById("threadinfo" + mes.tid);
    var z = document.getElementById("threadtable").rows[mes.tid+1].cells;
    if (mes.startTime < currentTime) {
      if (currentTime < mes.startTime + mes.nsteps) {
        x[2].innerHTML = microsteps[currentTime - mes.startTime].pc;
        x[3].innerHTML = getShared(currentTime);
        stackTrace(y,
            mes.microsteps[currentTime - mes.startTime].trace,
            mes.microsteps[currentTime - mes.startTime].failure);
        z[1].innerHTML = mes.microsteps[currentTime - mes.startTime].mode;
      }
      else {
        x[2].innerHTML = microsteps[microsteps.length-1].npc;
        x[3].innerHTML = getShared(mes.startTime + mes.nsteps);
        stackTrace(y,
            mes.microsteps[mes.nsteps-1].trace,
            mes.microsteps[mes.nsteps-1].failure);
        z[1].innerHTML = mes.microsteps[mes.nsteps-1].mode;
      }
    }
    else {
      x[2].innerHTML = ""
      x[3].innerHTML = ""
    }
  }
}

function handleClick(e, mesIdx) {
  var x = Math.floor(e.offsetX / boxSize);
  var y = Math.floor(e.offsetY / boxSize);
  currentTime = megasteps[mesIdx].startTime + y*30 + x + 1;
  run_microsteps()
}

function init_megastep(i) {
  var mes = megasteps[i];
  mes.startTime = currentTime;
  mes.canvas.addEventListener('mousedown', function(e){handleClick(e, i)});
  currentTime += mes.nsteps;

  // Copy over the microsteps.
  var mis = [];
  var stack = [];
  for (var misidx = 0; misidx < mes.nsteps; misidx++) {
    mis[misidx] = { stack: [] };

    if (0) {
        // Reconstruct the stack        (TODO: don't actually need this)
        if (state.megasteps[i].microsteps[misidx].hasOwnProperty("pop")) {
          stack.length -= parseInt(state.megasteps[i].microsteps[misidx].pop);
        }
        if (state.megasteps[i].microsteps[misidx].hasOwnProperty("push")) {
          stack[stack.length] = state.megasteps[i].microsteps[misidx].push;
        }
        for (var idx = 0; idx < stack.length; idx++) {
          mis[misidx].stack[idx] = stack[idx];
        }
    }

    // Copy over the fp or inherit from prior slot
    if (state.megasteps[i].microsteps[misidx].hasOwnProperty("fp")) {
      mis[misidx].fp = parseInt(state.megasteps[i].microsteps[misidx].fp);
    }
    else {
      mis[misidx].fp = misidx == 0 ? 0 : mis[misidx - 1].fp;
    }

    // Copy over the stack trace or inherit from prior slot
    if (state.megasteps[i].microsteps[misidx].hasOwnProperty("trace")) {
      mis[misidx].trace = state.megasteps[i].microsteps[misidx].trace;
    }
    else {
      mis[misidx].trace = misidx == 0 ? [] : mis[misidx - 1].trace;
    }

    // Update local variables
    if (mis[misidx].trace.length > 0 && state.megasteps[i].microsteps[misidx].hasOwnProperty("local")) {
      // deep copy first
      mis[misidx].trace = JSON.parse(JSON.stringify(mis[misidx].trace))
      mis[misidx].trace[0].vars = state.megasteps[i].microsteps[misidx].local;
    }

    // Also get the failure if any
    if (state.megasteps[i].microsteps[misidx].hasOwnProperty("failure")) {
      mis[misidx].failure = state.megasteps[i].microsteps[misidx].failure;
    }
    else {
      mis[misidx].failure = null
    }

    // Also get the mode if any
    if (state.megasteps[i].microsteps[misidx].hasOwnProperty("mode")) {
      mis[misidx].mode = state.megasteps[i].microsteps[misidx].mode;
    }
    else {
      mis[misidx].mode = "running";
    }
  }
  mes.microsteps = mis;
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
      currentTime = mes.startTime;
      run_microsteps();
      break;
    case 'ArrowDown':
      var mesidx = currentMegaStep();
      var mes = megasteps[mesidx];
      if (currentTime == mes.startTime + mes.nsteps &&
                          mesidx < megasteps.length - 1) {
          mes = megasteps[mesidx + 1];
      }
      currentTime = mes.startTime + mes.nsteps;
      run_microsteps();
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
  megasteps[curMegaStep].nsteps++;
  microsteps[t] = {
    mesidx: curMegaStep,
    masidx: masidx,
    misidx: misidx,
    tid: parseInt(mas.tid),
    pc: parseInt(mis.pc)
  };

  if (mis.hasOwnProperty("npc")) {
    microsteps[t].npc = mis.npc;
  }
  else {
    microsteps[t].npc = mis.pc;
  }

  if (mis.hasOwnProperty("fp")) {
    microsteps[t].fp = mis.fp;
  }
  else {
    microsteps[t].fp = t == 0 ? 0 : microsteps[t-1].fp;
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
  if (false && microsteps[t].trace.length > 0 && mis.hasOwnProperty("local")) {
    // deep copy first
    microsteps[t].trace = JSON.parse(JSON.stringify(microsteps[t].trace))
    microsteps[t].trace[0].vars = mis.local;
  }

  if (mis.hasOwnProperty("shared")) {
    microsteps[t].shared = stringify(mis.shared);
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
  var mes = mestable.rows[mis.mesidx + 2];
  mes.cells[3].innerHTML = mis.npc;
  mes.cells[4].innerHTML = mis.shared;

  stackTrace(threads[mis.tid].tracetable, mis.trace, null);
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
}

for (var tid = 0; tid < nthreads; tid++) {
  threads[tid] = {
    status: "normal",
    stacktrace: [],
    tracetable: document.getElementById("threadinfo" + tid)
  };
}
for (let i = 0; i < nmegasteps; i++) {
  var canvas = document.getElementById("timeline" + i);
  megasteps[i] = { canvas: canvas, startTime: 0, nsteps: 0 };
  canvas.addEventListener('mousedown', function(e){handleClick(e, i)});
}
for (var j = 0; j < state.macrosteps.length; j++) {
  init_macrostep(j);
}

currentTime = totalTime = microsteps.length;
run_microsteps();
document.addEventListener('keydown', handleKeyPress);
