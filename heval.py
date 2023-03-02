import sys, json

def heval_kv(js):
    return (heval_string(js["key"]), heval_string(js["value"]))

def heval_idx(js):
    return "[" + heval_string(js) + "]"

def heval_string(js):
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
                result += heval_string(func)
        else:
            result += heval_string(func)
        return result + "".join([ heval_idx(kv) for kv in args ])
    v = js["value"]
    if type == "bool":
        return v
    if type == "int":
        return str(v) if isinstance(v, int) else v
    if type == "atom":
        return json.dumps(v, ensure_ascii=False)
    if type == "set":
        if v == []:
            return "{}"
        lst = [ heval_string(val) for val in v ]
        return "{ " + ", ".join(lst) + " }"
    if type == "list":
        if v == []:
            return "[]"
        lst = [ heval_string(val) for val in v ]
        return "[ " + ", ".join(lst) + " ]"
    if type == "dict":
        if v == []:
            return "{:}"
        lst = [ heval_kv(kv) for kv in v ]
        keys = [ k for k,v in lst ]
        if keys == [str(i) for i in range(len(v))]:
            return "[ " + ", ".join([v for k,v in lst]) + " ]" 
        else:
            return "{ " + ", ".join([k + ": " + v for k,v in lst]) + " }" 
    if type == "pc":
        return "PC(%s)"%v
    if type == "context":
        return "CONTEXT(" + str(v["pc"]) + ")"

with open(sys.argv[1], encoding='utf-8') as f:
    top = json.load(f, strict=False)
    print(heval_string(top["symbols"]["1"]))
