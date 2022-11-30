def json_idx(js):
    if js["type"] == "atom":
        return json_string(js)
    return "[" + json_string(js) + "]"

def json_string(js):
    type = js["type"]
    if type == "address":
        if "func" not in js:
            return "None"
        result = "?"
        func = js["func"]
        args = js["args"]
        if func["type"] == "pc":
            if int(func["value"]) == -1:
                result += args[0]["value"]
                args = args[1:]
            elif int(func["value"]) == -2:
                result += "@" + args[0]["value"]
                args = args[1:]
            else:
                result += json_string(func)
        else:
            result += json_string(func)
        return result + "".join([ json_idx(kv) for kv in args ])
    v = js["value"]
    if type in { "bool", "int" }:
        return v
    if type == "atom":
        return '"' + v + '"'
    if type == "list":
        if v == []:
            return "[]"
        return "[ " + ", ".join([ json_string(val) for val in v]) + " ]"
    if type == "set":
        if v == []:
            return "{}"
        return "{ " + ", ".join([ json_string(val) for val in v]) + " }"
    if type == "dict":
        if v == []:
            return "{:}"
        lst = [ (json_string(js["key"]), json_string(js["value"])) for js in v ]
        if [ k for k,_ in lst ] == [ str(i) for i in range(len(v)) ]:
            return "[ " + ", ".join([ x for _,x in lst ]) + " ]" 
        return "{ " + ", ".join([ k + ": " + x for k,x in lst ]) + " }" 
    if type == "pc":
        return "PC(%s)"%v
    if type == "address":
        if v == []:
            return "None"
        return "?" + v[0]["value"] + "".join([ json_idx(kv) for kv in v[1:] ])
    if type == "context":
        return "CONTEXT(" + str(v["pc"]) + ")"
    assert False
