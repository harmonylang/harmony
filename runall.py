import subprocess
import time
import json
import os.path

tests = [
    { "args": "code/triangle.hny", "issue": "No issues", "nstates": 13 },
    { "args": "code/prog1.hny", "issue": "No issues", "nstates": 2 },
    { "args": "code/prog2.hny", "issue": "Safety violation", "nstates": 11 },
    { "args": "code/Up.hny", "issue": "Safety violation", "nstates": 44 },
    { "args": "code/Upf.hny", "issue": "Safety violation", "nstates": 13 },
    { "args": "code/UpEnter.hny", "issue": "Non-terminating state", "nstates": 39 },
    { "args": "code/csbarebones.hny", "issue": "Non-terminating state", "nstates": 3 },
    { "args": "code/cs.hny", "issue": "Safety violation", "nstates": 15 },
    { "args": "code/naiveLock.hny", "issue": "Safety violation", "nstates": 43 },
    { "args": "code/naiveFlags.hny", "issue": "Non-terminating state", "nstates": 47 },
    { "args": "code/naiveTurn.hny", "issue": "Non-terminating state", "nstates": 26 },
    { "args": "code/Peterson.hny", "issue": "No issues", "nstates": 118 },
    { "args": "code/PetersonBroken.hny", "issue": "Safety violation", "nstates": 168 },
    { "args": "code/csonebit.hny", "issue": "Active busy waiting", "nstates": 87 },
    { "args": "code/PetersonMethod.hny", "issue": "No issues", "nstates": 118 },
    { "args": "code/hanoi.hny", "issue": "No issues", "nstates": 28 },
    { "args": "-cWIDTH=4 -cHEIGHT=5 code/knight.hny", "issue": "No issues", "nstates": 35662 },
    { "args": "code/clock.hny", "issue": "Safety violation", "nstates": 5462 },
    { "args": "code/lock_test1.hny", "issue": "No issues", "nstates": 112 },
    { "args": "-mlock=lock_tas code/lock_test1.hny", "issue": "No issues", "nstates": 112 },
    { "args": "-mlock=lock_ticket code/lock_test1.hny", "issue": "No issues", "nstates": 2042 },
    { "args": "-mlock=lock_susp code/lock_test1.hny", "issue": "No issues", "nstates": 256 },
    { "args": "-mlock=synch code/lock_test1.hny", "issue": "No issues", "nstates": 112 },
    { "args": "-mlock=synchS code/lock_test1.hny", "issue": "No issues", "nstates": 256 },
    { "args": "code/UpLock.hny", "issue": "No issues", "nstates": 48 },
    { "args": "-msynch=synchS code/UpLock.hny", "issue": "No issues", "nstates": 58 },
    { "args": "code/spinlock.hny", "issue": "No issues", "nstates": 12545 },
    { "args": "code/xy.hny", "issue": "Safety violation", "nstates": 19 },
    { "args": "code/atm.hny", "issue": "Safety violation", "nstates": 1837 },
    { "args": "code/queue_test1.hny", "issue": "No issues", "nstates": 80 },
    { "args": "code/setobj_test1.hny", "issue": "No issues", "nstates": 217 },
    { "args": "-msetobj=setobj_linkedlist code/setobj_test1.hny", "issue": "No issues", "nstates": 8791 },
    { "args": "-mqueueconc=queue_lock code/queue_test_seq.hny", "issue": "No issues", "nstates": 600 },
    { "args": "-mqueueconc=queue_MS code/queue_test_seq.hny", "issue": "No issues", "nstates": 702 },
    { "args": "-o queue4.hfa code/queue_btest1.hny", "issue": "No issues", "nstates": 3385 },
    { "args": "-B queue4.hfa -m queue=queue_lock code/queue_btest1.hny", "issue": "No issues", "nstates": 66530 },
    { "args": "-B queue4.hfa -m queue=queue_MS code/queue_btest1.hny", "issue": "No issues", "nstates": 99816 },
    { "args": "-mqueue=queue_broken2 code/queue_btest1.hny", "issue": "Safety violation", "nstates": 23875 },
    { "args": "code/rwlock_test1.hny", "issue": "No issues", "nstates": 499 },
    { "args": "-mrwlock=rwlock_sbs code/rwlock_test1.hny", "issue": "No issues", "nstates": 8089 },
    { "args": "-mrwlock=rwlock_cv code/rwlock_test1.hny", "issue": "No issues", "nstates": 13138 },
    { "args": "-mrwlock=rwlock_cv -msynch=synchS code/rwlock_test1.hny", "issue": "No issues", "nstates": 35537 },
    { "args": "-mrwlock=rwlock_cv_fair code/rwlock_test1.hny", "issue": "No issues", "nstates": 26508 },
    { "args": "-mrwlock=rwlock_cv_fair -msynch=synchS code/rwlock_test1.hny", "issue": "No issues", "nstates": 65501 },
    { "args": "-mrwlock=rwlock_sbs_fair code/rwlock_test1.hny", "issue": "No issues", "nstates": 5831 },
    { "args": "-mrwlock=rwlock_sbs_fair -msynch=synchS code/rwlock_test1.hny", "issue": "No issues", "nstates": 21060 },
    { "args": "-o rw.hfa -cNOPS=3 code/rwlock_btest.hny", "issue": "No issues", "nstates": 2922 },
    { "args": "-B rw.hfa -cNOPS=3 -m rwlock=rwlock_sbs code/rwlock_btest.hny", "issue": "No issues", "nstates": 51686 },
    { "args": "-B rw.hfa -cNOPS=3 -m rwlock=rwlock_cv code/rwlock_btest.hny", "issue": "No issues", "nstates": 34463 },
    { "args": "-B rw.hfa -cNOPS=3 -m rwlock=rwlock_cv_fair code/rwlock_btest.hny", "issue": "No issues", "nstates": 51221 },
    { "args": "-B rw.hfa -cNOPS=3 -m rwlock=rwlock_sbs_fair code/rwlock_btest.hny", "issue": "No issues", "nstates": 37589 },
    { "args": "-B rw.hfa -cNOPS=3 -m rwlock=rwlock_cheat code/rwlock_btest.hny", "issue": "No issues", "nstates": 7937 },
    { "args": "-mboundedbuffer=boundedbuffer_hoare code/boundedbuffer_test1.hny", "issue": "No issues", "nstates": 1017 },
    { "args": "-mboundedbuffer=boundedbuffer_hoare -msynch=synchS code/boundedbuffer_test1.hny", "issue": "No issues", "nstates": 4019 },
    { "args": "code/qsorttest.hny", "issue": "No issues", "nstates": 1190 },
    { "args": "code/Diners.hny", "issue": "Non-terminating state", "nstates": 8670 },
    { "args": "-msynch=synchS code/Diners.hny", "issue": "Non-terminating state", "nstates": 27671 },
    { "args": "code/DinersCV.hny", "issue": "No issues", "nstates": 58119 },
    { "args": "-msynch=synchS code/DinersCV.hny", "issue": "No issues", "nstates": 837019 },
    { "args": "code/DinersAvoid.hny", "issue": "No issues", "nstates": 39884 },
    { "args": "-msynch=synchS code/DinersAvoid.hny", "issue": "No issues", "nstates": 152874 },
    { "args": "code/bank.hny", "issue": "Non-terminating state", "nstates": 2604 },
    { "args": "code/counter.hny", "issue": "No issues", "nstates": 505 },
    { "args": "code/qbarrier.hny", "issue": "No issues", "nstates": 1664 },
    { "args": "-msynch=synchS code/qbarrier.hny", "issue": "No issues", "nstates": 4927 },
    { "args": "code/barrier_test.hny", "issue": "No issues", "nstates": 1215 },
    { "args": "-mbarrier=code/barrier_double code/barrier_test.hny", "issue": "No issues", "nstates": 1319 },
    { "args": "-mbarrier=code/barrier_cv code/barrier_test.hny", "issue": "No issues", "nstates": 5801 },
    { "args": "-mbarrier=code/barrier_cv -msynch=synchS code/barrier_test.hny", "issue": "No issues", "nstates": 13082 },
    # { "args": "-o file.hfa code/file_btest.hny", "issue": "No issues", "nstates": 36887 },
    # { "args": "-B file.hfa -m file=file_inode code/file_btest.hny", "issue": "No issues", "nstates": 43554096 },
    { "args": "code/trap.hny", "issue": "No issues", "nstates": 8 },
    { "args": "code/trap2.hny", "issue": "Safety violation", "nstates": 21 },
    { "args": "code/trap3.hny", "issue": "Non-terminating state", "nstates": 11 },
    { "args": "code/trap4.hny", "issue": "No issues", "nstates": 16 },
    { "args": "code/trap5.hny", "issue": "No issues", "nstates": 16 },
    { "args": "code/trap6.hny", "issue": "No issues", "nstates": 386 },
    { "args": "-msynch=synchS code/trap6.hny", "issue": "No issues", "nstates": 554 },
    { "args": "code/hw.hny", "issue": "No issues", "nstates": 23864 },
    { "args": "code/abptest.hny", "issue": "No issues", "nstates": 673 },
    { "args": "code/leader.hny", "issue": "No issues", "nstates": 33005 },
    { "args": "code/2pc.hny", "issue": "No issues", "nstates": 666316 },
    { "args": "-o reg.hfa code/abdtest.hny", "issue": "No issues", "nstates": 148 },
    { "args": "-B reg.hfa -mregister=abd code/abdtest.hny", "issue": "No issues", "nstates": 7449569 },
    { "args": "-o consensus.hfa code/consensus.hny", "issue": "No issues", "nstates": 2602 },
    { "args": "-B consensus.hfa code/bosco.hny", "issue": "No issues", "nstates": 5288 },
    { "args": "-o consensus.hfa -cN=2 code/consensus.hny", "issue": "No issues", "nstates": 108 },
    { "args": "-B consensus.hfa code/paxos.hny", "issue": "No issues", "nstates": 103824 },
    { "args": "-o rsm.hfa code/rsm.hny", "issue": "No issues", "nstates": 1952 },
    { "args": "-B rsm.hfa code/chain.hny", "issue": "No issues", "nstates": 213285 },
    { "args": "code/needhamschroeder.hny", "issue": "Safety violation", "nstates": 558 },
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
            if hco["nstates"] == t["nstates"]:
                print("time=%.2f, #states=%d, issue=%s" % (end - start, hco["nstates"], hco["issue"]))
            else:
                print("time=%.2f, #states=%d(%d), issue=%s" % (end - start, hco["nstates"], t["nstates"], hco["issue"]))
            if t["issue"] != hco["issue"]:
                print("Different issue (was %s)???  Aborting further tests" % t["issue"])
                break
            if "warning" in hco:
                print("Got warning: %s" % hco["warning"])
            if t["issue"] != "Safety violation" and min(t["nstates"], hco["nstates"]) / max(t["nstates"], hco["nstates"]) < .1:
                print("#states very different (was %d)???" % t["nstates"])
                break
    else:
        print("Error code %d, aborting further tests" % cp.returncode)
        print("Output: ", cp.stdout.decode())
        print("Error: ", cp.stderr.decode())
        break
