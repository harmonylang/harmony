import json
import copy
from harmony_model_checker.harmony.verbose import verbose_string

"""
Takes in filenames. Returns summary in string.
"""
def summaryMain(filenames, hco):
    # hco = {}
    hvm = {}
    summaryMain.microSteps = []
    # summaryMain.stackTraceList is a list of string with length <number of threads>. Each entry is the stack trace for each thread
    summaryMain.stackTraceList = []
    # summaryMain.stackTraceTextList contains stack trace to display at each microstep
    summaryMain.stackTraceTextList = []
    # summaryMain.threadMode is a list of thread modes at each microstep
    summaryMain.threadMode = []
    summaryMain.threadNumber = -1
    summaryMain.threadNames = []

    def constructMicrosteps():
        summaryMain.microSteps = []
        # initialize summaryMain.threadNumber to be number of threads
        summaryMain.threadNumber = len(hco['macrosteps'][-1]['contexts']) # fix bug - change 0 to -1
        # initialize summaryMain.microSteps
        for macroStep in hco['macrosteps']:
            for microStep in macroStep['microsteps']:
                cpMicroStep = dict(microStep)
                cpMicroStep['tid'] = macroStep['tid']
                cpMicroStep['name'] = macroStep['name']
                # cpMicroStep['invfails'] = macroStep['invfails']
                cpMicroStep['contexts'] = macroStep['contexts']
                cpMicroStep['context'] = macroStep['context']
                summaryMain.microSteps.append(cpMicroStep)
        # initialize summaryMain.stackTraceList
        summaryMain.stackTraceList = []
        summaryMain.stackTraceTextList = []
        for i in range(summaryMain.threadNumber):
            summaryMain.stackTraceList.append("")
        # initialize 
        for i in range(len(summaryMain.microSteps)):
            summaryMain.stackTraceTextList.append("")
            
        
    def constructStackTraceTextList():
        assert len(summaryMain.stackTraceList) == summaryMain.threadNumber
        assert len(summaryMain.stackTraceTextList) == len(summaryMain.microSteps)
        # base case for i = 0 to fix the initial stack trace
        assert 'contexts' in hco['macrosteps'][0]
        for thread in hco['macrosteps'][0]['contexts']:
            tid = int(thread['tid'])
            assert 'trace' in thread
            trace = thread['trace']
            traceLine = ""
            assert len(trace) > 0
            for j in range(len(trace) - 1):
                traceLine = traceLine + trace[j]['method'] + ' -> '
            traceLine += trace[len(trace) - 1]['method']
            summaryMain.stackTraceList[tid] = traceLine
        summaryMain.stackTraceTextList[0] = []
        for stackTraceLine in summaryMain.stackTraceList:
            summaryMain.stackTraceTextList[0].append(stackTraceLine)
        # other microsteps for i > 0
        for i in range(1, len(summaryMain.microSteps)):
            if 'trace' in summaryMain.microSteps[i]:
                # there is a change in stack trace
                trace = summaryMain.microSteps[i]['trace']
                traceLine = ""
                if(len(trace) > 0):
                    for j in range(len(trace) - 1):
                        traceLine = traceLine + trace[j]['method'] + ' -> '
                    traceLine = traceLine + trace[len(trace) - 1]['method']
                tid = int(summaryMain.microSteps[i]['tid'])
                summaryMain.stackTraceList[tid] = traceLine
                # update the ith entry in summaryMain.stackTraceTextList
                summaryMain.stackTraceTextList[i] = []
                for stackTraceLine in summaryMain.stackTraceList:
                    summaryMain.stackTraceTextList[i].append(stackTraceLine)
            else:
                # there is no change in stack trace
                summaryMain.stackTraceTextList[i] = copy.deepcopy(summaryMain.stackTraceTextList[i - 1])
            # print failure in stack trace (commented out since already covered by next)
            # if 'failure' in summaryMain.microSteps[i]:
            #     tid = int(summaryMain.microSteps[i]['tid'])
            #     summaryMain.stackTraceTextList[i][tid] += f" -> {summaryMain.microSteps[i]['failure']}!"
            
        # add "about to" information to the end of stack trace line
        i = 0
        for macrostep in hco['macrosteps']:
            i += len(macrostep['microsteps']) - 1
            assert 'contexts' in macrostep
            for context in macrostep['contexts']:
                if 'next' in context and int(context['tid']) == int(summaryMain.microSteps[i]['tid']):
                    tid = int(summaryMain.microSteps[i]['tid'])
                    summaryMain.stackTraceTextList[i][tid] += f" ({about(context)})"
                    tmp = i + 1
                    while tmp < len(summaryMain.microSteps) and int(summaryMain.microSteps[tmp]['tid']) != tid:
                        summaryMain.stackTraceTextList[tmp][tid] += f" ({about(context)})"
                        tmp += 1
            i += 1

        for i in range(len(summaryMain.stackTraceTextList)):
            for j in range(len(summaryMain.stackTraceTextList[i])):
                summaryMain.stackTraceTextList[i][j] = f"[{summaryMain.threadMode[i][j]}] " + summaryMain.stackTraceTextList[i][j] 
        
        # construct thread names
        for t_name in summaryMain.stackTraceTextList[-1]:
            summaryMain.threadNames.append(getThreadName(t_name))

    def constructStackTopDisplay():
        """
        construct stackTopDisplay
        """
        stacks = []
        stackTopDisplay = []
        for i in range(summaryMain.threadNumber):
            stacks.append([])
        # default stack for each thread
        for t in range(summaryMain.threadNumber):
            i = 0
            while i < len(summaryMain.microSteps) and int(summaryMain.microSteps[i]['tid']) != t:
                i += 1
            # fix bug for threads that don't run
            if i == len(summaryMain.microSteps):
                continue
            stacks[t] = summaryMain.microSteps[i]['context']['stack']
        framePointer = -1
        for i in range(len(summaryMain.microSteps)):
            tid = int(summaryMain.microSteps[i]['tid'])
            # update frame pointer
            if 'fp' in summaryMain.microSteps[i]:
                framePointer = int(summaryMain.microSteps[i]['fp'])
            # pop items first
            if 'pop' in summaryMain.microSteps[i]:
                assert len(stacks[tid]) >= int(summaryMain.microSteps[i]['pop'])
                for j in range(int(summaryMain.microSteps[i]['pop'])):
                    del stacks[tid][-1]
            if 'push' in summaryMain.microSteps[i]:
                for variable in summaryMain.microSteps[i]['push']:
                    stacks[tid].append(variable)
            # update stackTopDisplay
            stackTopDisplay.append([])
            for k in range(framePointer, len(stacks[tid])):
                stackTopDisplay[i].append(stacks[tid][k])

    def constructThreadMode():
        # initialize summaryMain.threadMode
        for i in range(len(summaryMain.microSteps)):
            summaryMain.threadMode.append([])
            for j in range(summaryMain.threadNumber):
                summaryMain.threadMode[i].append("runnable")
        # construct thread mode for each microstep
        i = 0
        for macrostep in hco['macrosteps']:
            if i > 0:
                summaryMain.threadMode[i] = copy.deepcopy(summaryMain.threadMode[i - 1])
            if 'contexts' in macrostep:
                for context in macrostep['contexts']:
                    if 'mode' in context:
                        summaryMain.threadMode[i][int(context['tid'])] = 'runnable' if context['mode'] == 'choosing' else context['mode'] # change choosing to runnable
            if ('context' in macrostep) and ('mode' in macrostep['context']):
                summaryMain.threadMode[i][int(macrostep['context']['tid'])] = 'runnable' if macrostep['context']['mode'] == 'choosing' else macrostep['context']['mode']
            for j in range(len(macrostep['microsteps'])):
                if j > 0:
                    summaryMain.threadMode[i] = copy.deepcopy(summaryMain.threadMode[i - 1])
                if 'mode' in macrostep['microsteps'][j]:
                    summaryMain.threadMode[i][int(summaryMain.microSteps[i]['tid'])] = 'runnable' if macrostep['microsteps'][j]['mode'] == 'choosing' else macrostep['microsteps'][j]['mode']
                if j < len(macrostep['microsteps']) - 1:
                    i += 1
            if 'contexts' in macrostep:
                for context in macrostep['contexts']:
                    if 'mode' in context:
                        summaryMain.threadMode[i][int(context['tid'])] = 'runnable' if context['mode'] == 'choosing' else context['mode']
            i += 1
        # for k in range(len(summaryMain.threadMode)):
        #     print(summaryMain.threadMode[k])
        

    def friendlyOutput():
        issueText = hco["issue"]
        # output = f"{issueText}\n"
        output = ""
        if issueText == "No issues":
            output += "Congratulations, your program has no issues!\n"
            return
        elif issueText == "Safety violation":
            output += "Unfortunately, there exists some state in your program that violates a safety property. \n"
            output += "Here is a shortest execution trace summary that exhibits the issue:\n"
        elif issueText == "Invariant violation":
            output += "Unfortunately, an invariant in your program can violate. \n"
            output += "Here is a shortest execution trace summary that exhibits the issue:\n"
        elif issueText == "Finally predicate violation":
            output += "Unfortunately, the finally assertion in your program can fail. \n"
            output += "Here is a shortest execution trace summary that exhibits the issue:\n"
        elif issueText == "Behavior Violation: terminal state not final":
            pass
        elif issueText == "Non-terminating state":
            output += "Unfortunately, there exists some case where your program can't terminate. \n"
            output += "Here is a shortest execution trace summary that exhibits the issue:\n"
        elif issueText == "Active busy waiting":
            output += "Unfortunately, there is active busy waiting in your program. That is, a thread is waiting for a condition while changing the state. \n"
            output += "Here is a shortest execution trace summary that exhibits the issue:\n"
        elif "Data race" in issueText:
            output += f"Unfortunately, there is a data race in your program on {getDataRaceTarget(issueText)}. \n"
            output += "Here is a shortest execution trace summary that exhibits the issue:\n"
        else:
            print(issueText)
            raise Exception("issue match failure")
        output += friendlyTrace()
        output += "\n"
        output += "More detailed information can be found in htm output or HarmonyGUI.\n"
        return output
    

    def friendlyTrace():
        trace = ""
        counter = 0
        subCounter = 0
        trace += f"{counter}. Program starts with the initial thread T{int(summaryMain.microSteps[0]['tid'])} {summaryMain.threadNames[0]} at line {getStartLine(0)}.\n"
        for i in range(len(summaryMain.microSteps)):
            if (i == len(summaryMain.microSteps) - 1):
                break
            if (summaryMain.microSteps[i]['tid'] != summaryMain.microSteps[i + 1]['tid']):
                prev_tid = int(summaryMain.microSteps[i]['tid'])
                prev_tname = summaryMain.threadNames[prev_tid]
                next_tid = int(summaryMain.microSteps[i + 1]['tid'])
                next_tname = summaryMain.threadNames[next_tid]
                i_line_prev = i
                while (getTid(i) != getTid(i_line_prev) or getModule(i_line_prev) != "__main__"):
                    i_line_prev -= 1

                i_line_next = i + 1
                while (getTid(i + 1) != getTid(i_line_next) or getModule(i_line_next) != "__main__"):
                    i_line_next -= 1
                counter += 1
                subCounter = 0
                # last thread just terminated
                if getStatus(summaryMain.stackTraceTextList[i][prev_tid]) == "terminated":
                    trace += f"{counter}. At line {getEndLine(i_line_prev)}, T{prev_tid} {prev_tname} terminates. Context switch to T{next_tid} {next_tname} at line {getStartLine(i_line_next)}.\n"
                # last thread is about to do sth
                elif getAboutTo(summaryMain.stackTraceTextList[i][prev_tid]) != "":
                    aboutTo = getAboutTo(summaryMain.stackTraceTextList[i][prev_tid])
                    trace += f"{counter}. At line {getEndLine(i_line_prev)}, T{prev_tid} {prev_tname} is {aboutTo}. Context switch to T{next_tid} {next_tname} at line {getStartLine(i_line_next)}.\n"
                # nothing special
                else:
                    trace += f"{counter}. At line {getEndLine(i_line_prev)}, T{prev_tid} {prev_tname} is preempted. Context switch to T{next_tid} {next_tname} at line {getStartLine(i_line_next)}.\n"
        
            if i < len(summaryMain.microSteps):
                sharedVariableListBefore = getSharedVariable(i)
                sharedVariableListAfter =  getSharedVariable(i + 1)

                prev_tid = int(summaryMain.microSteps[i]['tid'])
                prev_tname = summaryMain.threadNames[prev_tid]
                i_line_prev = i
                while (getTid(i) != getTid(i_line_prev) or getModule(i_line_prev) != "__main__"):
                    i_line_prev -= 1
                    
                if sharedVariableListBefore != sharedVariableListAfter:
                    for variableName, variable in sharedVariableListAfter.items():
                        if (sharedVariableListBefore == None) or (variableName not in sharedVariableListBefore):
                            subCounter += 1
                            trace += (f"    At line {getEndLine(i_line_prev)}, T{prev_tid} {prev_tname} initializes shared variable <{variableName}> to {verbose_string(variable)}. \n")
                        elif sharedVariableListBefore[variableName] != sharedVariableListAfter[variableName]:
                            variableBefore = sharedVariableListBefore[variableName]
                            subCounter += 1
                            lst = getDifferentEntryTrace(variableBefore, variable)
                            if len(lst) > 0:
                                traceStr = ""
                                for e in lst:
                                    traceStr += f"[{e if isinstance(e, int) else verbose_string(e)}]"
                                trace += (f"    At line {getEndLine(i_line_prev)}, T{prev_tid} updates {variableName + traceStr} to {entryChangeTo(lst, variable)}. Shared variable <{variableName}> becomes {verbose_string(variable)}. \n")
                            else: # len(lst) == 0
                                trace += (f"    At line {getEndLine(i_line_prev)}, T{prev_tid} updates shared variable <{variableName}> to {verbose_string(variable)}. \n")
                        

        # a failure in the end
        if 'failure' in summaryMain.microSteps[len(summaryMain.microSteps) - 1]:
            counter += 1
            i_failure = len(summaryMain.microSteps) - 1
            prev_tid = getTid(i_failure)
            prev_tname = summaryMain.threadNames[prev_tid]
            failure_msg = summaryMain.microSteps[i_failure]['failure']
            trace += f"{counter}. At line {getEndLine(i_failure)} of T{prev_tid} {prev_tname}, {failure_msg}\n"
        return trace

    def getTid(i):
        return int(summaryMain.microSteps[i]['tid'])

    def getPc(i):
        return int(summaryMain.microSteps[i]["pc"])
    
    # return example: {'module': 'synch', 'endline': 34, 'stmt': [34, 1, 34, 21], 'line': 34, 'endcolumn': 21, 'column': 1}
    def getModule(i):
        return hvm['locs'][getPc(i)]['module']
    
    def getEndLine(i):
        return hvm['locs'][getPc(i)]['endline']
    
    def getStartLine(i):
        return hvm['locs'][getPc(i)]['line']

    def getStatus(s):
        start = s.find("[")
        end = s.find("]")
        return s[start + 1:end]
    
    # example return: "" or "about to execute atomic section"
    def getAboutTo(s):
        start = s.find("(about to")
        if start < 0:
            return ""
        return s[(start + 1):-1]

    def getThreadName(s):
        start = s.find("]")
        end = s.find(")")
        return s[(start + 2):(end + 1)]
    
    def getDataRaceTarget(s):
        return s[11:-1]

    def getSharedVariable(microStepPointer):
        # clear all displayed content
        if microStepPointer == 0:
            return None
        microStepPointer -= 1
        # find current shared variable state
        mostRecentSharedVariablePointer = microStepPointer
        while 'shared' not in summaryMain.microSteps[mostRecentSharedVariablePointer]:
            mostRecentSharedVariablePointer -= 1
            if mostRecentSharedVariablePointer < 0:
                return
            
        microstep = summaryMain.microSteps[mostRecentSharedVariablePointer]
        sharedVariableList = microstep['shared']
        return sharedVariableList

    def getDifferentEntryTrace(variableBefore, variableAfter):
        res = []
        if (variableBefore['type'] == variableAfter['type'] == 'list'): # list case
            # must have exactly one entry differ
            if (len(variableBefore['value']) == len(variableAfter['value'])) and len(variableBefore['value']) > 0:
                differCount = 0
                candidateAppend = None
                for i in range(len(variableBefore['value'])):
                    if variableBefore['value'][i] != variableAfter['value'][i]:
                        differCount += 1
                        candidateAppend = i
                if differCount == 1:
                    res.append(candidateAppend)
                    return (res + getDifferentEntryTrace(variableBefore['value'][candidateAppend], variableAfter['value'][candidateAppend]))
                
        elif (variableBefore['type'] == variableAfter['type'] == 'dict'): # dict case
            # must have exactly one entry differ
            if (len(variableBefore['value']) == len(variableAfter['value'])) and len(variableBefore['value']) > 0:
                differCount = 0
                candidateKey = None
                candidateValue = None
                matched = []
                for i in range(len(variableBefore['value'])):
                    if variableBefore['value'][i] not in variableAfter['value']:
                        differCount += 1
                        candidateKey = variableBefore['value'][i]['key']
                        candidateValue = variableBefore['value'][i]['value']
                    else:
                        matched.append(variableBefore['value'][i])
                if differCount == 1:
                    assert len(matched) == (len(variableBefore['value']) - 1)
                    for i in range(len(variableAfter)):
                        if variableAfter['value'][i] not in matched:
                            assert variableAfter['value'][i] not in variableBefore['value']
                            # assert variableAfter['value'][i]['key'] == candidateKey and variableAfter['value'][i]['value'] != candidateValue
                            if (variableAfter['value'][i]['key'] == candidateKey) and (variableAfter['value'][i]['value'] != candidateValue):
                                res.append(candidateKey)
                                return (res + getDifferentEntryTrace(candidateValue, variableAfter['value'][i]['value']))
                            break
        return res
    
    def entryChangeTo(lst, variableAfter):
        cur = copy.deepcopy(variableAfter)
        for e in lst:
            if isinstance(e, int): # list
                assert cur['type'] == 'list'
                cur = cur['value'][e]
            else: # dict
                assert cur['type'] == 'dict'
                for kv in cur['value']:
                    if kv['key'] == e:
                        cur = kv['value']
                        break
        return verbose_string(cur)

    def about(ctx):
        nxt = ctx["next"]
        if nxt["type"] == "Frame":
            return f"about to run method {nxt['name']} with argument {verbose_string(nxt['value'])}"
        elif nxt["type"] == "Load":
            return f"about to load variable {nxt['var']}"
        elif nxt["type"] == "Store":
            return f"about to store: {nxt['var']}<-{verbose_string(nxt['value'])}"
        elif nxt["type"] == "Print":
            return f"about to print {verbose_string(nxt['value'])}"
        elif nxt["type"] == "AtomicInc":
            return "about to execute atomic section"
        elif nxt["type"] == "Assert":
            return "assertion failed"
        else:
            return f"about to {nxt['type']}"
        
    # with open(filenames['hco'], 'r') as hcoFile:
    #     hco = json.load(hcoFile, strict=False)
    if True:
        hvm = hco['hvm']

        # construct summaryMain.microSteps to be a list of microsteps
        constructMicrosteps()
        # construct summaryMain.threadMode
        constructThreadMode()
        # construct stackTraceText to be stack trace to display at each microstep
        constructStackTraceTextList()
        # construct stackTopDisplay
        constructStackTopDisplay()

        return friendlyOutput()
