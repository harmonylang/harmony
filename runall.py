import subprocess
import time
import json
import os.path

tests = [
    { "args": "code/triangle.hny", "issue": "No issues", "nstates": 13 },
    { "args": "code/prog1.hny", "issue": "No issues", "nstates": 2 },
    { "args": "code/prog2.hny", "issue": "Safety violation", "nstates": 11 },
    { "args": "code/Up.hny", "issue": "Safety violation", "nstates": 44 },
    { "args": "code/Upf.hny", "issue": "Finally predicate violation", "nstates": 13 },
    { "args": "code/UpEnter.hny", "issue": "Non-terminating state", "nstates": 59 },
    { "args": "code/csbarebones.hny", "issue": "Safety violation", "nstates": 5 },
    { "args": "code/cs.hny", "issue": "Safety violation", "nstates": 11 },
    { "args": "code/naiveLock.hny", "issue": "Safety violation", "nstates": 34 },
    { "args": "code/naiveFlags.hny", "issue": "Non-terminating state", "nstates": 45 },
    { "args": "code/naiveTurn.hny", "issue": "Non-terminating state", "nstates": 28 },
    { "args": "code/Peterson.hny", "issue": "No issues", "nstates": 104 },
    { "args": "code/PetersonBroken.hny", "issue": "Safety violation", "nstates": 126 },
    { "args": "code/PetersonInductive.hny", "issue": "No issues", "nstates": 104 },
    { "args": "code/csonebit.hny", "issue": "Active busy waiting", "nstates": 73 },
    { "args": "code/PetersonMethod.hny", "issue": "No issues", "nstates": 104 },
    { "args": "code/hanoi.hny", "issue": "Safety violation", "nstates": 28 },
    { "args": "code/clock.hny", "issue": "Safety violation", "nstates": 5462 },
    { "args": "code/cssynch.hny", "issue": "No issues", "nstates": 35 },
    { "args": "-msynch=synchS code/cssynch.hny", "issue": "No issues", "nstates": 58 },
    { "args": "-msynch=ticket code/cssynch.hny", "issue": "No issues", "nstates": 458 },
    { "args": "code/UpLock.hny", "issue": "No issues", "nstates": 48 },
    { "args": "-msynch=synchS code/UpLock.hny", "issue": "No issues", "nstates": 58 },
    { "args": "code/spinlock.hny", "issue": "No issues", "nstates": 473 },
    { "args": "code/xy.hny", "issue": "Safety violation", "nstates": 19 },
    { "args": "code/atm.hny", "issue": "Invariant violation", "nstates": 1832 },
    { "args": "code/queuedemo.hny", "issue": "No issues", "nstates": 80 },
    { "args": "code/setobjtest.hny", "issue": "No issues", "nstates": 217 },
    { "args": "-msetobj=linkedlist code/setobjtest.hny", "issue": "No issues", "nstates": 9495 },
    { "args": "code/qtestseq.hny", "issue": "No issues", "nstates": 600 },
    { "args": "-mqueueconc=queueMS code/qtestseq.hny", "issue": "No issues", "nstates": 702 },
    { "args": "code/qtest1.hny", "issue": "No issues", "nstates": 202 },
    { "args": "code/qtest2.hny", "issue": "No issues", "nstates": 55 },
    { "args": "code/qtest3.hny", "issue": "No issues", "nstates": 3225 },
    { "args": "code/qtest4.hny", "issue": "No issues", "nstates": 10 },
    { "args": "code/qtestconc.hny", "issue": "No issues", "nstates": 1879206 },
    { "args": "-msynch=synchS code/qtestconc.hny", "issue": "No issues", "nstates": 3430951 },
    { "args": "-o queue4.hfa code/qtestpar.hny", "issue": "No issues", "nstates": 3385 },
    { "args": "-B queue4.hfa -m queue=queueconc code/qtestpar.hny", "issue": "No issues", "nstates": 66530 },
    { "args": "-o queue4.hfa code/qtestpar.hny", "issue": "No issues", "nstates": 3385 },
    { "args": "-B queue4.hfa -m queue=queueMS code/qtestpar.hny", "issue": "No issues", "nstates": 99816 },
    { "args": "-mqueue=queuebroken code/qtestpar.hny", "issue": "Safety violation", "nstates": 5 },
    { "args": "code/RWtest.hny", "issue": "No issues", "nstates": 135 },
    { "args": "-mRW=RWsbs code/RWtest.hny", "issue": "No issues", "nstates": 1757 },
    { "args": "-mRW=RWcv code/RWtest.hny", "issue": "No issues", "nstates": 1691 },
    { "args": "-mRW=RWcv -msynch=synchS code/RWtest.hny", "issue": "No issues", "nstates": 4301 },
    { "args": "-mRW=RWfair code/RWtest.hny", "issue": "No issues", "nstates": 1248 },
    { "args": "-mRW=RWfair -msynch=synchS code/RWtest.hny", "issue": "No issues", "nstates": 3137 },
    { "args": "-o rw.hfa -cNOPS=2 code/RWbtest.hny", "issue": "No issues", "nstates": 273 },
    { "args": "-B rw.hfa -cNOPS=2 -m RW=RWsbs code/RWbtest.hny", "issue": "No issues", "nstates": 1393 },
    { "args": "-o rw.hfa -cNOPS=2 code/RWbtest.hny", "issue": "No issues", "nstates": 273 },
    { "args": "-B rw.hfa -cNOPS=2 -m RW=RWcv code/RWbtest.hny", "issue": "No issues", "nstates": 923 },
    { "args": "-B rw.hfa -cNOPS=2 -m RW=RWfair code/RWbtest.hny", "issue": "No issues", "nstates": 1019 },
    { "args": "-B rw.hfa -cNOPS=2 -m RW=RWcheat code/RWbtest.hny", "issue": "No issues", "nstates": 257 },
    { "args": "-mboundedbuffer=BBhoare code/BBtest.hny", "issue": "No issues", "nstates": 1017 },
    { "args": "-mboundedbuffer=BBhoare -msynch=synchS code/BBtest.hny", "issue": "No issues", "nstates": 4019 },
    { "args": "code/qsorttest.hny", "issue": "No issues", "nstates": 1190 },
    { "args": "code/Diners.hny", "issue": "Non-terminating state", "nstates": 9095 },
#    { "args": "-msynch=synchS code/Diners.hny", "issue": "Non-terminating state", "nstates": 32476 },
    { "args": "code/DinersCV.hny", "issue": "No issues", "nstates": 101549 },
    { "args": "-msynch=synchS code/DinersCV.hny", "issue": "No issues", "nstates": 2293519 },
    { "args": "code/DinersAvoid.hny", "issue": "No issues", "nstates": 39884 },
    { "args": "-msynch=synchS code/DinersAvoid.hny", "issue": "No issues", "nstates": 152874 },
    { "args": "code/bank.hny", "issue": "Non-terminating state", "nstates": 2827 },
    { "args": "code/counter.hny", "issue": "No issues", "nstates": 508 },
    { "args": "code/qbarrier.hny", "issue": "No issues", "nstates": 1664 },
    { "args": "-msynch=synchS code/qbarrier.hny", "issue": "No issues", "nstates": 4927 },
    { "args": "code/barriertest.hny", "issue": "No issues", "nstates": 2529 },
    { "args": "-msynch=synchS code/barriertest.hny", "issue": "No issues", "nstates": 7425 },
    { "args": "code/barriertest2.hny", "issue": "No issues", "nstates": 5711 },
    { "args": "-msynch=synchS code/barriertest2.hny", "issue": "No issues", "nstates": 16511 },
    { "args": "code/trap.hny", "issue": "No issues", "nstates": 8 },
    { "args": "code/trap2.hny", "issue": "Finally predicate violation", "nstates": 21 },
    { "args": "code/trap3.hny", "issue": "Non-terminating state", "nstates": 26 },
    { "args": "code/trap4.hny", "issue": "No issues", "nstates": 16 },
    { "args": "code/trap5.hny", "issue": "No issues", "nstates": 16 },
    { "args": "code/trap6.hny", "issue": "No issues", "nstates": 386 },
    { "args": "-msynch=synchS code/trap6.hny", "issue": "No issues", "nstates": 554 },
    { "args": "code/hw.hny", "issue": "No issues", "nstates": 23864 },
    { "args": "code/abptest.hny", "issue": "No issues", "nstates": 2778 },
    { "args": "code/leader.hny", "issue": "No issues", "nstates": 33005 },
    { "args": "-mstack=stack1 code/stacktest.hny", "issue": "No issues", "nstates": 2 },
    { "args": "-mstack=stack2 code/stacktest.hny", "issue": "No issues", "nstates": 2 },
    { "args": "-mstack=stack3 code/stacktest.hny", "issue": "No issues", "nstates": 2 },
    { "args": "-mstack=stack4 code/stacktest.hny", "issue": "No issues", "nstates": 2 }
]

for t in tests:
    print()
    print("Running harmony %s"%t["args"], flush=True)
    start = time.time()
    args = t["args"].split(" ")
    cp = subprocess.run(["./harmony", "--noweb"] + args, capture_output=True)
    end = time.time()
    if cp.returncode == 0:
        (base, ext) = os.path.splitext(args[-1])
        with open(base + ".hco") as f:
            hco = json.load(f)
            print("time=%.2f, #states=%d, issue=%s" % (end - start, hco["nstates"], hco["issue"]))
            if t["issue"] != hco["issue"]:
                print("Different issue (was %s)???  Aborting further tests" % t["issue"])
                break
            if t["issue"] != "Safety violation" and min(t["nstates"], hco["nstates"]) / max(t["nstates"], hco["nstates"]) < .9:
                print("#states very different (was %d)???  Aborting further tests" % t["nstates"])
                break
    else:
        print("Error code %d, aborting further tests" % cp.returncode)
        print("Output: ", cp.stdout)
        print("Error: ", cp.stderr)
        break
