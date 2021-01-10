var boxSize = 10;
var currentTime = 0;
var totalTime = 0;
var threads = [];

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
    var vtext = document.createTextNode(stringify(trace[i].vars));
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
  drawTimeLines()
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
      drawTimeLines();
      break;
    case 'ArrowRight':
      if (currentTime < totalTime) {
        currentTime += 1;
      }
      drawTimeLines();
      break;
    case 'ArrowUp':
      var mesidx = currentMegaStep();
      var mes = megasteps[mesidx];
      currentTime = mes.startTime;
      drawTimeLines();
      break;
    case 'ArrowDown':
      var mesidx = currentMegaStep();
      var mes = megasteps[mesidx];
      if (currentTime == mes.startTime + mes.nsteps &&
                          mesidx < megasteps.length - 1) {
          mes = megasteps[mesidx + 1];
      }
      currentTime = mes.startTime + mes.nsteps;
      drawTimeLines();
      break;
    default:
      // alert("unknown key " + e.code);
  }
}

for (var i = 0; i < megasteps.length; i++) {
  init_megastep(i);
totalTime = currentTime;
drawTimeLines();
document.addEventListener('keydown', handleKeyPress);
