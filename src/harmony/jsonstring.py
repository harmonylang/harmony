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
        return '"' + v + '"'
    if type == "set":
        if v == []:
            return "{}"
        return "{ " + ", ".join([ json_string(val) for val in v]) + " }"
    if type == "dict":
        if v == []:
            return "()"
        return "{ " + ", ".join([ json_kv(kv) for kv in v ]) + " }" 
    if type == "pc":
        return "PC(%s)"%v
    if type == "address":
        if v == []:
            return "None"
        return "?" + v[0]["value"] + "".join([ json_idx(kv) for kv in v[1:] ])
    if type == "context":
        return "CONTEXT(" + json_string(v["name"]) + ")"
    assert False
