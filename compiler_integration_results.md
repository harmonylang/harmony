# Compiler Integration Test Results

---
##  harmony_model_checker/modules/bag.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/bag.hco```

Duration: 0.0011459999999999977

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/bag.hco```

Duration: 0.0011697999999999986

---
##  harmony_model_checker/modules/synchBusy.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synchBusy.hco```

Duration: 0.0015348000000000028

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synchBusy.hco```

Duration: 0.0010944000000000023

---
##  harmony_model_checker/modules/synchImprecise.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synchImprecise.hco```

Duration: 0.0011132000000000017

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synchImprecise.hco```

Duration: 0.0015929999999999972

---
##  harmony_model_checker/modules/synch.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synch.hco```

Duration: 0.0013827000000000006

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synch.hco```

Duration: 0.001453999999999997

---
##  harmony_model_checker/modules/alloc.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/alloc.hco```

Duration: 0.001905999999999998

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/alloc.hco```

Duration: 0.0015929000000000013

---
##  harmony_model_checker/modules/hoare.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/hoare.hco```

Duration: 0.0013765999999999987

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/hoare.hco```

Duration: 0.0012493000000000018

---
##  harmony_model_checker/modules/synchS.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synchS.hco```

Duration: 0.0014278999999999958

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synchS.hco```

Duration: 0.0017845000000000014

---
##  harmony_model_checker/modules/set.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/set.hco```

Duration: 0.001256100000000003

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/set.hco```

Duration: 0.001333899999999999

---
##  harmony_model_checker/modules/list.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/list.hco```

Duration: 0.0012505999999999975

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/list.hco```

Duration: 0.0011607999999999966

---
##  code/prog1.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/prog1.hco```

Duration: 0.001274299999999999

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/prog1.hco```

Duration: 0.0014648999999999981

---
##  code/prog2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (11)
Safety Violation
Loading code/prog2.hco
T0: __init__() [0-3,17-25] { shared: True }
T2: g() [13-16] { shared: False }
T1: f() [4-8] { shared: False }
Harmony assertion failed```

Duration: 0.0011265999999999984

### Current Output

```
nworkers = 16
#states (11)
Safety Violation
Loading code/prog2.hco
T0: __init__() [0-3,17-25] { shared: True }
T2: g() [13-16] { shared: False }
T1: f() [4-8] { shared: False }
Harmony assertion failed```

Duration: 0.0010155999999999984

---
##  code/Up.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (44)
Safety Violation
Loading code/Up.hco
T0: __init__() [0-5,35-43] { count: 0, done: [ False, False ] }
T2: incrementer(1) [6-9] { count: 0, done: [ False, False ] }
T1: incrementer(0) [6-20] { count: 1, done: [ True, False ] }
T2: incrementer(1) [10-24,26-31] { count: 1, done: [ True, True ] }
Harmony assertion failed```

Duration: 0.0015287999999999968

### Current Output

```
nworkers = 16
#states (44)
Safety Violation
Loading code/Up.hco
T0: __init__() [0-5,35-43] { count: 0, done: [ False, False ] }
T2: incrementer(1) [6-9] { count: 0, done: [ False, False ] }
T1: incrementer(0) [6-20] { count: 1, done: [ True, False ] }
T2: incrementer(1) [10-24,26-31] { count: 1, done: [ True, True ] }
Harmony assertion failed```

Duration: 0.0012071000000000026

---
##  code/UpEnter.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (60)
60 components
Non-terminating state
Loading code/UpEnter.hco
T0: __init__() [0-7,58-66] { count: 0, done: [ False, False ], entered: [ False, False ] }
T2: incrementer(1) [8-18] { count: 0, done: [ False, False ], entered: [ False, True ] }
T1: incrementer(0) [8-25] { count: 0, done: [ False, False ], entered: [ True, True ] }
T2: incrementer(1) [19-25] { count: 0, done: [ False, False ], entered: [ True, True ] }```

Duration: 0.0015410999999999897

### Current Output

```
nworkers = 16
#states (60)
60 components
Non-terminating state
Loading code/UpEnter.hco
T0: __init__() [0-7,58-66] { count: 0, done: [ False, False ], entered: [ False, False ] }
T2: incrementer(1) [8-18] { count: 0, done: [ False, False ], entered: [ False, True ] }
T1: incrementer(0) [8-25] { count: 0, done: [ False, False ], entered: [ True, True ] }
T2: incrementer(1) [19-25] { count: 0, done: [ False, False ], entered: [ True, True ] }```

Duration: 0.0011938000000000018

---
##  code/csbarebones.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (5)
Safety Violation
Loading code/csbarebones.hco
T0: __init__() [0,1,18-26] { }
T1: thread() [2-4] { }
T2: thread() [2-4] { }
T1: thread() [5-12] { }
Harmony assertion failed```

Duration: 0.0011257999999999962

### Current Output

```
nworkers = 16
#states (5)
Safety Violation
Loading code/csbarebones.hco
T0: __init__() [0,1,18-26] { }
T1: thread() [2-4] { }
T2: thread() [2-4] { }
T1: thread() [5-12] { }
Harmony assertion failed```

Duration: 0.0016591999999999996

---
##  code/cs.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (11)
Safety Violation
Loading code/cs.hco
T0: __init__() [0,1,19-27] { }
T1: thread() [2-4(choose True),5] { }
T2: thread() [2-4(choose True),5] { }
T1: thread() [6-13] { }
Harmony assertion failed```

Duration: 0.0011425999999999936

### Current Output

```
nworkers = 16
#states (11)
Safety Violation
Loading code/cs.hco
T0: __init__() [0,1,19-27] { }
T1: thread() [2-4(choose True),5] { }
T2: thread() [2-4(choose True),5] { }
T1: thread() [6-13] { }
Harmony assertion failed```

Duration: 0.0011486999999999886

---
##  code/naiveLock.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (49)
Safety Violation
Loading code/naiveLock.hco
T0: __init__() [0-3,31-39] { lockTaken: False }
T2: thread(1) [4-7(choose True),8-12,14] { lockTaken: False }
T1: thread(0) [4-7(choose True),8-12,14,15] { lockTaken: True }
T2: thread(1) [15-23] { lockTaken: True }
Harmony assertion failed```

Duration: 0.0010195000000000065

### Current Output

```
nworkers = 16
#states (49)
Safety Violation
Loading code/naiveLock.hco
T0: __init__() [0-3,31-39] { lockTaken: False }
T2: thread(1) [4-7(choose True),8-12,14] { lockTaken: False }
T1: thread(0) [4-7(choose True),8-12,14,15] { lockTaken: True }
T2: thread(1) [15-23] { lockTaken: True }
Harmony assertion failed```

Duration: 0.0010344999999999938

---
##  code/naiveFlags.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (45)
15 components
Non-terminating state
Loading code/naiveFlags.hco
T0: __init__() [0-3,42-50] { flags: [ False, False ] }
T2: thread(1) [4-6(choose True),7-17] { flags: [ False, True ] }
T1: thread(0) [4-6(choose True),7-17] { flags: [ True, True ] }```

Duration: 0.0011338999999999932

### Current Output

```
nworkers = 16
#states (45)
15 components
Non-terminating state
Loading code/naiveFlags.hco
T0: __init__() [0-3,42-50] { flags: [ False, False ] }
T2: thread(1) [4-6(choose True),7-17] { flags: [ False, True ] }
T1: thread(0) [4-6(choose True),7-17] { flags: [ True, True ] }```

Duration: 0.0009819999999999968

---
##  code/naiveTurn.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (28)
21 components
Non-terminating state
Loading code/naiveTurn.hco
T0: __init__() [0-3,32-40] { turn: 0 }
T1: thread(0) [4-6(choose True),7-11] { turn: 1 }
T2: thread(1) [4-6(choose False),7,30,31] { turn: 1 }```

Duration: 0.0011287999999999992

### Current Output

```
nworkers = 16
#states (28)
21 components
Non-terminating state
Loading code/naiveTurn.hco
T0: __init__() [0-3,32-40] { turn: 0 }
T1: thread(0) [4-6(choose True),7-11] { turn: 1 }
T2: thread(1) [4-6(choose False),7,30,31] { turn: 1 }```

Duration: 0.001103899999999991

---
##  code/Peterson.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (104)
37 components
No issues
Loading code/Peterson.hco```

Duration: 0.0010717000000000088

### Current Output

```
nworkers = 16
#states (104)
37 components
No issues
Loading code/Peterson.hco```

Duration: 0.0010234000000000076

---
##  code/PetersonInductive.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (104)
37 components
No issues
Loading code/PetersonInductive.hco```

Duration: 0.0012411999999999979

### Current Output

```
nworkers = 16
#states (104)
37 components
No issues
Loading code/PetersonInductive.hco```

Duration: 0.0010610999999999954

---
##  code/csonebit.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (73)
18 components
Active busy waiting
Loading code/csonebit.hco
T0: __init__() [0-5,52-60] { flags: [ False, False ] }
T2: thread(1) [6-8(choose True),9-19] { flags: [ False, True ] }
T1: thread(0) [6-8(choose True),9-19] { flags: [ True, True ] }```

Duration: 0.001207799999999995

### Current Output

```
nworkers = 16
#states (73)
18 components
Active busy waiting
Loading code/csonebit.hco
T0: __init__() [0-5,52-60] { flags: [ False, False ] }
T2: thread(1) [6-8(choose True),9-19] { flags: [ False, True ] }
T1: thread(0) [6-8(choose True),9-19] { flags: [ True, True ] }```

Duration: 0.0010146000000000044

---
##  code/PetersonMethod.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (104)
37 components
No issues
Loading code/PetersonMethod.hco```

Duration: 0.0011063999999999935

### Current Output

```
nworkers = 16
#states (104)
37 components
No issues
Loading code/PetersonMethod.hco```

Duration: 0.0010423000000000099

---
##  code/clock.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (5462)
Safety Violation
Loading code/clock.hco
T0: __init__() [0,1,132-139,2-21,140-144,2-21,145-172,179-195,23-45,81-131,196-205,23-45,81-131,206-226,161-172,179-195,23-45,81-131,196-205,23-45,81-131,206-226,161-172,179-195,23-45,81-131,196-205,23-45,81-131,206-226,161-172,179-195,23-80,31-80,31-80,31-45,81-131,196-205,23-45,81-131,206-226,161-168,173-178(choose 2),179-195,23-30,115-131,196-205,23-30,115-131,206-226,161-168,173-178(choose 1),179-195,23-80,31-45,81-131,196-205,23-30,115-131,206-226,161-168,173-178(choose 2),179-195,23-30,115-131,196-205,23-30,115-131,206-226,161-168,173-178(choose 5),179-195,23-80,31-80,31-80,31-45,81-131,196-205,23-80,31-80,31-80,31-80,31-45,81-131,206-226,161-168,173-178(choose 1),179-195,23-30,115-131,196-205,23-45,81-131,206-226,161-168,173-178(choose 2),179-195,23-30,115-131,196-205,23-45,81-131,206-218] { clock3: { "entries": [ 5, 2, 1 ], "hand": 1, "misses": 6, "recent": { 1, 2, 5 } }, clock4: { "entries": [ 5, 1, 2, 4 ], "hand": 3, "misses": 7, "recent": { 1, 2, 5 } }, refs: [ 1, 2, 3, 4, 2, 1, 2, 5, 1, 2 ] }
Harmony assertion failed```

Duration: 0.001300499999999996

### Current Output

```
nworkers = 16
#states (5462)
Safety Violation
Loading code/clock.hco
T0: __init__() [0,1,132-139,2-21,140-144,2-21,145-172,179-195,23-45,81-131,196-205,23-45,81-131,206-226,161-172,179-195,23-45,81-131,196-205,23-45,81-131,206-226,161-172,179-195,23-45,81-131,196-205,23-45,81-131,206-226,161-172,179-195,23-80,31-80,31-80,31-45,81-131,196-205,23-45,81-131,206-226,161-168,173-178(choose 2),179-195,23-30,115-131,196-205,23-30,115-131,206-226,161-168,173-178(choose 1),179-195,23-80,31-45,81-131,196-205,23-30,115-131,206-226,161-168,173-178(choose 2),179-195,23-30,115-131,196-205,23-30,115-131,206-226,161-168,173-178(choose 5),179-195,23-80,31-80,31-80,31-45,81-131,196-205,23-80,31-80,31-80,31-80,31-45,81-131,206-226,161-168,173-178(choose 1),179-195,23-30,115-131,196-205,23-45,81-131,206-226,161-168,173-178(choose 2),179-195,23-30,115-131,196-205,23-45,81-131,206-218] { clock3: { "entries": [ 5, 2, 1 ], "hand": 1, "misses": 6, "recent": { 1, 2, 5 } }, clock4: { "entries": [ 5, 1, 2, 4 ], "hand": 3, "misses": 7, "recent": { 1, 2, 5 } }, refs: [ 1, 2, 3, 4, 2, 1, 2, 5, 1, 2 ] }
Harmony assertion failed```

Duration: 0.0013142000000000015

---
##  code/spinlock.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (473)
148 components
No issues
Loading code/spinlock.hco```

Duration: 0.0011918000000000067

### Current Output

```
nworkers = 16
#states (473)
148 components
No issues
Loading code/spinlock.hco```

Duration: 0.0010196999999999984

---
##  code/UpLock.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (57)
57 components
No issues
Loading code/UpLock.hco```

Duration: 0.0013770999999999922

### Current Output

```
nworkers = 16
#states (57)
57 components
No issues
Loading code/UpLock.hco```

Duration: 0.0013264999999999944

---
## -msynch=synchS code/UpLock.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (59)
59 components
No issues
Loading code/UpLock.hco```

Duration: 0.0013296000000000002

### Current Output

```
nworkers = 16
#states (59)
59 components
No issues
Loading code/UpLock.hco```

Duration: 0.0012413000000000007

---
##  code/xy.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (20)
Safety Violation
Loading code/xy.hco
T0: __init__() [0-9,54-62] { x: 0, y: 100 }
T2: setX(50) [10-16] { x: 50, y: 100 }
T1: checker() [32-35,20-30,36-50] { x: 50, y: 100 }
Harmony assertion failed: (50, 100)```

Duration: 0.0011821999999999944

### Current Output

```
nworkers = 16
#states (20)
Safety Violation
Loading code/xy.hco
T0: __init__() [0-9,54-62] { x: 0, y: 100 }
T2: setX(50) [10-16] { x: 50, y: 100 }
T1: checker() [32-35,20-30,36-50] { x: 50, y: 100 }
Harmony assertion failed: (50, 100)```

Duration: 0.0013985999999999998

---
##  code/atm.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (4110)
Invariant Violation
Loading code/atm.hco
T0: __init__() [0-5,369-371,1039-1054,766-770,759-764,771,772,1055-1058(choose 1),1059-1062,1044-1054,766-770,759-764,771,772,1055-1058(choose 1),1059-1062,1044-1046,1063-1066,1094,1183-1197(choose 0),1198-1201(choose 1),1202-1205,1185-1197(choose 0),1198-1201(choose 1),1202-1205,1185-1187,1206,1207] { accounts: [ { "balance": 1, "lock": False }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }
T2: customer(2, 0, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-785] { accounts: [ { "balance": 1, "lock": False }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }
T1: customer(1, 0, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-789,793-799,1132-1153,801-815,1154,1155,1179-1182] { accounts: [ { "balance": 0, "lock": False }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }
T2: customer(2, 0, 1) [786-789,793-799,1132-1153,801-804] { accounts: [ { "balance": -1, "lock": True }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }```

Duration: 0.0013558000000000042

### Current Output

```
nworkers = 16
#states (4110)
Invariant Violation
Loading code/atm.hco
T0: __init__() [0-5,369-371,1039-1054,766-770,759-764,771,772,1055-1058(choose 1),1059-1062,1044-1054,766-770,759-764,771,772,1055-1058(choose 1),1059-1062,1044-1046,1063-1066,1094,1183-1197(choose 1),1198-1201(choose 1),1202-1205,1185-1197(choose 1),1198-1201(choose 1),1202-1205,1185-1187,1206,1207] { accounts: [ { "balance": 1, "lock": False }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }
T1: customer(1, 1, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-785] { accounts: [ { "balance": 1, "lock": False }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }
T2: customer(2, 1, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-789,793-799,1132-1153,801-815,1154,1155,1179-1182] { accounts: [ { "balance": 1, "lock": False }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }
T1: customer(1, 1, 1) [786-789,793-799,1132-1153,801-804] { accounts: [ { "balance": 1, "lock": False }, { "balance": -1, "lock": True } ], bag: (), list: (), synch: () }```

Duration: 0.0016202999999999912

---
##  code/queuedemo.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (80)
80 components
No issues
Loading code/queuedemo.hco```

Duration: 0.0012093000000000104

### Current Output

```
nworkers = 16
#states (80)
80 components
No issues
Loading code/queuedemo.hco```

Duration: 0.0013312000000000046

---
## -msynch=synchS code/queuedemo.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (80)
80 components
No issues
Loading code/queuedemo.hco```

Duration: 0.0013081999999999955

### Current Output

```
nworkers = 16
#states (80)
80 components
No issues
Loading code/queuedemo.hco```

Duration: 0.0010854000000000003

---
##  code/qtestseq.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (600)
600 components
No issues
Loading code/qtestseq.hco```

Duration: 0.0013538000000000022

### Current Output

```
nworkers = 16
#states (600)
600 components
No issues
Loading code/qtestseq.hco```

Duration: 0.0013977000000000017

---
##  code/qtest1.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (274)
274 components
No issues
Loading code/qtest1.hco```

Duration: 0.001483100000000001

### Current Output

```
nworkers = 16
#states (274)
274 components
No issues
Loading code/qtest1.hco```

Duration: 0.0012225000000000014

---
## -msynch=synchS code/qtest1.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (274)
274 components
No issues
Loading code/qtest1.hco```

Duration: 0.001602199999999998

### Current Output

```
nworkers = 16
#states (274)
274 components
No issues
Loading code/qtest1.hco```

Duration: 0.0012992000000000004

---
##  code/qtest2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (55)
55 components
No issues
Loading code/qtest2.hco```

Duration: 0.0014310000000000017

### Current Output

```
nworkers = 16
#states (55)
55 components
No issues
Loading code/qtest2.hco```

Duration: 0.0013391000000000097

---
## -msynch=synchS code/qtest2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (55)
55 components
No issues
Loading code/qtest2.hco```

Duration: 0.0012680999999999942

### Current Output

```
nworkers = 16
#states (55)
55 components
No issues
Loading code/qtest2.hco```

Duration: 0.0014099999999999946

---
##  code/qtest3.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3225)
3225 components
No issues
Loading code/qtest3.hco```

Duration: 0.0012302999999999897

### Current Output

```
nworkers = 16
#states (3225)
3225 components
No issues
Loading code/qtest3.hco```

Duration: 0.0012044999999999972

---
## -msynch=synchS code/qtest3.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3225)
3225 components
No issues
Loading code/qtest3.hco```

Duration: 0.0013168000000000069

### Current Output

```
nworkers = 16
#states (3225)
3225 components
No issues
Loading code/qtest3.hco```

Duration: 0.00114510000000001

---
##  code/qtest4.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/qtest4.hco```

Duration: 0.0013708000000000053

### Current Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/qtest4.hco```

Duration: 0.0011287999999999854

---
## -msynch=synchS code/qtest4.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/qtest4.hco```

Duration: 0.00112509999999999

### Current Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/qtest4.hco```

Duration: 0.0012222000000000066

---
##  code/qtestconc.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2127239)
2127239 components
No issues
Loading code/qtestconc.hco```

Duration: 0.005788199999999993

### Current Output

```
nworkers = 16
#states (2127239)
2127239 components
No issues
Loading code/qtestconc.hco```

Duration: 0.002636699999999992

---
## -msynch=synchS code/qtestconc.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3430951)
3430951 components
No issues
Loading code/qtestconc.hco```

Duration: 0.00408989999999998

### Current Output

```
nworkers = 16
#states (3430951)
3430951 components
No issues
Loading code/qtestconc.hco```

Duration: 0.003318600000000005

---
## -mqueue=queueMS code/queuedemo.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3125)
3125 components
No issues
Loading code/queuedemo.hco```

Duration: 0.0014875000000000027

### Current Output

```
nworkers = 16
#states (3125)
3125 components
No issues
Loading code/queuedemo.hco```

Duration: 0.0012786999999999937

---
## -mqueue=queueMS -msynch=synchS code/queuedemo.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3287)
3287 components
No issues
Loading code/queuedemo.hco```

Duration: 0.0013794000000000028

### Current Output

```
nworkers = 16
#states (3287)
3287 components
No issues
Loading code/queuedemo.hco```

Duration: 0.0011933999999999834

---
## -msetobj=linkedlist code/intsettest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (12368)
12368 components
No issues
Loading code/intsettest.hco```

Duration: 0.001308599999999993

### Current Output

```
nworkers = 16
#states (12368)
12368 components
No issues
Loading code/intsettest.hco```

Duration: 0.001765700000000009

---
## -msynch=synchS -msetobj=linkedlist code/intsettest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (18377)
18377 components
No issues
Loading code/intsettest.hco```

Duration: 0.0013451999999999908

### Current Output

```
nworkers = 16
#states (18377)
18377 components
No issues
Loading code/intsettest.hco```

Duration: 0.0014292000000000193

---
##  code/RWtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (135)
27 components
No issues
Loading code/RWtest.hco```

Duration: 0.0012231999999999799

### Current Output

```
nworkers = 16
#states (135)
27 components
No issues
Loading code/RWtest.hco```

Duration: 0.0012767000000000195

---
## -msynch=synchS code/RWtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (135)
27 components
No issues
Loading code/RWtest.hco```

Duration: 0.0015186000000000088

### Current Output

```
nworkers = 16
#states (135)
27 components
No issues
Loading code/RWtest.hco```

Duration: 0.001234099999999988

---
## -mRW=RWsbs code/RWtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (1943)
619 components
No issues
Loading code/RWtest.hco```

Duration: 0.0012781000000000042

### Current Output

```
nworkers = 16
#states (1943)
619 components
No issues
Loading code/RWtest.hco```

Duration: 0.0011060999999999988

---
## -mRW=RWsbs -msynch=synchS code/RWtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (4212)
897 components
No issues
Loading code/RWtest.hco```

Duration: 0.0012082999999999955

### Current Output

```
nworkers = 16
#states (4212)
897 components
No issues
Loading code/RWtest.hco```

Duration: 0.0013009000000000215

---
## -mRW=RWfair code/RWtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (1438)
449 components
No issues
Loading code/RWtest.hco```

Duration: 0.0014732000000000078

### Current Output

```
nworkers = 16
#states (1438)
449 components
No issues
Loading code/RWtest.hco```

Duration: 0.00147029999999998

---
## -mRW=RWfair -msynch=synchS code/RWtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3137)
635 components
No issues
Loading code/RWtest.hco```

Duration: 0.0015569

### Current Output

```
nworkers = 16
#states (3137)
635 components
No issues
Loading code/RWtest.hco```

Duration: 0.0014102000000000003

---
## -mboundedbuffer=BBhoare code/BBtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (1175)
1175 components
No issues
Loading code/BBtest.hco```

Duration: 0.0013054999999999872

### Current Output

```
nworkers = 16
#states (1175)
1175 components
No issues
Loading code/BBtest.hco```

Duration: 0.001631400000000005

---
## -mboundedbuffer=BBhoare -msynch=synchS code/BBtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (4127)
4127 components
No issues
Loading code/BBtest.hco```

Duration: 0.0015776000000000123

### Current Output

```
nworkers = 16
#states (4127)
4127 components
No issues
Loading code/BBtest.hco```

Duration: 0.0014128999999999947

---
## -mRW=RWcv code/RWtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (1902)
406 components
No issues
Loading code/RWtest.hco```

Duration: 0.0013180999999999887

### Current Output

```
nworkers = 16
#states (1902)
406 components
No issues
Loading code/RWtest.hco```

Duration: 0.0011631000000000002

---
## -mRW=RWcv -msynch=synchS code/RWtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (4301)
666 components
No issues
Loading code/RWtest.hco```

Duration: 0.0017305999999999988

### Current Output

```
nworkers = 16
#states (4301)
666 components
No issues
Loading code/RWtest.hco```

Duration: 0.0013928999999999747

---
##  code/qsorttest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (454)
454 components
No issues
Loading code/qsorttest.hco```

Duration: 0.0012871999999999884

### Current Output

```
nworkers = 16
#states (454)
454 components
No issues
Loading code/qsorttest.hco```

Duration: 0.0012796999999999947

---
##  code/Diners.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (23905)
4285 components
Non-terminating state
Loading code/Diners.hco
T0: __init__() [0-5,369-371,1039-1043,766-770,759-764,771,772,1044-1048,1094-1105,1096-1105,1096-1105,1096-1105,1096-1105,1096-1098,1106,1107] { bag: (), forks: [ False, False, False, False, False ], list: (), synch: () }
T3: diner(2) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ False, False, True, False, False ], list: (), synch: () }
T1: diner(0) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, False, False ], list: (), synch: () }
T5: diner(4) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, False, True ], list: (), synch: () }
T4: diner(3) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, True, True ], list: (), synch: () }
T2: diner(1) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, True, True, True, True ], list: (), synch: () }```

Duration: 0.001591100000000012

### Current Output

```
nworkers = 16
#states (23905)
4285 components
Non-terminating state
Loading code/Diners.hco
T0: __init__() [0-5,369-371,1039-1043,766-770,759-764,771,772,1044-1048,1094-1105,1096-1105,1096-1105,1096-1105,1096-1105,1096-1098,1106,1107] { bag: (), forks: [ False, False, False, False, False ], list: (), synch: () }
T3: diner(2) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ False, False, True, False, False ], list: (), synch: () }
T1: diner(0) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, False, False ], list: (), synch: () }
T5: diner(4) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, False, True ], list: (), synch: () }
T4: diner(3) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, True, True ], list: (), synch: () }
T2: diner(1) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, True, True, True, True ], list: (), synch: () }```

Duration: 0.0013052999999999815

---
## -msynch=synchS code/Diners.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (32476)
6416 components
Non-terminating state
Loading code/Diners.hco
T0: __init__() [0-5,799-803,417-421,404-415,422,423,804-808,854-865,856-865,856-865,856-865,856-865,856-858,866,867] { forks: [ { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () } ], list: (), synch: () }
T2: diner(1) [809-824(choose True),825-830,425-431,455-462,831-836,425-429] { forks: [ { "acquired": False, "suspended": () }, { "acquired": True, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () } ], list: (), synch: () }
T1: diner(0) [809-824(choose True),825-830,425-431,455-462,831-836,425-441] { forks: [ { "acquired": True, "suspended": () }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () } ], list: (), synch: () }
T5: diner(4) [809-824(choose True),825-830,425-431,455-462,831-836,425-441] { forks: [ { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": True, "suspended": () } ], list: (), synch: () }
T4: diner(3) [809-824(choose True),825-830,425-431,455-462,831-836,425-441] { forks: [ { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": False, "suspended": () }, { "acquired": True, "suspended": () }, { "acquired": True, "suspended": [ CONTEXT("diner") ] } ], list: (), synch: () }
T3: diner(2) [809-824(choose True),825-830,425-431,455-462,831-836,425-441] { forks: [ { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": () }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] } ], list: (), synch: () }
T2: diner(1) [430-441] { forks: [ { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] } ], list: (), synch: () }```

Duration: 0.0016457

### Current Output

```
nworkers = 16
#states (32476)
6416 components
Non-terminating state
Loading code/Diners.hco
T0: __init__() [0-5,799-803,417-421,404-415,422,423,804-808,854-865,856-865,856-865,856-865,856-865,856-858,866,867] { forks: [ { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () } ], list: (), synch: () }
T2: diner(1) [809-824(choose True),825-830,425-431,455-462,831-836,425-429] { forks: [ { "acquired": False, "suspended": () }, { "acquired": True, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () } ], list: (), synch: () }
T1: diner(0) [809-824(choose True),825-830,425-431,455-462,831-836,425-441] { forks: [ { "acquired": True, "suspended": () }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () } ], list: (), synch: () }
T5: diner(4) [809-824(choose True),825-830,425-431,455-462,831-836,425-441] { forks: [ { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": False, "suspended": () }, { "acquired": False, "suspended": () }, { "acquired": True, "suspended": () } ], list: (), synch: () }
T4: diner(3) [809-824(choose True),825-830,425-431,455-462,831-836,425-441] { forks: [ { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": False, "suspended": () }, { "acquired": True, "suspended": () }, { "acquired": True, "suspended": [ CONTEXT("diner") ] } ], list: (), synch: () }
T3: diner(2) [809-824(choose True),825-830,425-431,455-462,831-836,425-441] { forks: [ { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": () }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] } ], list: (), synch: () }
T2: diner(1) [430-441] { forks: [ { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] } ], list: (), synch: () }```

Duration: 0.001437799999999989

---
##  code/DinersCV.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (111679)
39194 components
No issues
Loading code/DinersCV.hco```

Duration: 0.0013679000000000052

### Current Output

```
nworkers = 16
#states (111679)
39194 components
No issues
Loading code/DinersCV.hco```

Duration: 0.0014413000000000065

---
## -msynch=synchS code/DinersCV.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2293519)
441764 components
No issues
Loading code/DinersCV.hco```

Duration: 0.003512100000000018

### Current Output

```
nworkers = 16
#states (2293519)
441764 components
No issues
Loading code/DinersCV.hco```

Duration: 0.00312380000000001

---
##  code/DinersAvoid.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (86214)
5589 components
No issues
Loading code/DinersAvoid.hco```

Duration: 0.0018589999999999995

### Current Output

```
nworkers = 16
#states (86214)
5589 components
No issues
Loading code/DinersAvoid.hco```

Duration: 0.0014706000000000163

---
## -msynch=synchS code/DinersAvoid.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (152874)
10504 components
No issues
Loading code/DinersAvoid.hco```

Duration: 0.0017391000000000212

### Current Output

```
nworkers = 16
#states (152874)
10504 components
No issues
Loading code/DinersAvoid.hco```

Duration: 0.0014098999999999917

---
##  code/bank.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3359)
3359 components
Non-terminating state
Loading code/bank.hco
T0: __init__() [0-5,369-371,1039-1054,766-770,759-764,771,772,1055-1058(choose 2),1059-1062,1044-1054,766-770,759-764,771,772,1055-1058(choose 2),1059-1062,1044-1046,1063-1066,1170-1181,1172-1181,1172-1174,1182,1183] { accounts: [ { "balance": 2, "lock": False }, { "balance": 2, "lock": False } ], bag: (), list: (), synch: () }
T1: thread() [1142-1144(choose 0),1145-1151(choose 1),1152-1165(choose 1),1166,1167,1067-1075,782-789,793-799,1076-1102,782-785] { accounts: [ { "balance": 1, "lock": True }, { "balance": 2, "lock": False } ], bag: (), list: (), synch: () }
T2: thread() [1142-1144(choose 1),1145-1151(choose 0),1152-1165(choose 2),1166,1167,1067-1075,782-789,793-799,1076-1102,782-785] { accounts: [ { "balance": 1, "lock": True }, { "balance": 0, "lock": True } ], bag: (), list: (), synch: () }```

Duration: 0.00152469999999999

### Current Output

```
nworkers = 16
#states (3359)
3359 components
Non-terminating state
Loading code/bank.hco
T0: __init__() [0-5,369-371,1039-1054,766-770,759-764,771,772,1055-1058(choose 2),1059-1062,1044-1054,766-770,759-764,771,772,1055-1058(choose 2),1059-1062,1044-1046,1063-1066,1170-1181,1172-1181,1172-1174,1182,1183] { accounts: [ { "balance": 2, "lock": False }, { "balance": 2, "lock": False } ], bag: (), list: (), synch: () }
T1: thread() [1142-1144(choose 0),1145-1151(choose 1),1152-1165(choose 1),1166,1167,1067-1075,782-789,793-799,1076-1102,782-785] { accounts: [ { "balance": 1, "lock": True }, { "balance": 2, "lock": False } ], bag: (), list: (), synch: () }
T2: thread() [1142-1144(choose 1),1145-1151(choose 0),1152-1165(choose 2),1166,1167,1067-1075,782-789,793-799,1076-1102,782-785] { accounts: [ { "balance": 1, "lock": True }, { "balance": 0, "lock": True } ], bag: (), list: (), synch: () }```

Duration: 0.00128049999999999

---
##  code/counter.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (601)
601 components
No issues
Loading code/counter.hco```

Duration: 0.0013728999999999825

### Current Output

```
nworkers = 16
#states (601)
601 components
No issues
Loading code/counter.hco```

Duration: 0.0015085999999999988

---
##  code/qbarrier.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (1664)
1664 components
No issues
Loading code/qbarrier.hco```

Duration: 0.001167499999999988

### Current Output

```
nworkers = 16
#states (1664)
1664 components
No issues
Loading code/qbarrier.hco```

Duration: 0.0013679000000000052

---
## -msynch=synchS code/qbarrier.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (4927)
4927 components
No issues
Loading code/qbarrier.hco```

Duration: 0.0014231999999999856

### Current Output

```
nworkers = 16
#states (4927)
4927 components
No issues
Loading code/qbarrier.hco```

Duration: 0.001322799999999985

---
##  code/barriertest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2802)
2802 components
No issues
Loading code/barriertest.hco```

Duration: 0.0013422000000000156

### Current Output

```
nworkers = 16
#states (2802)
2802 components
No issues
Loading code/barriertest.hco```

Duration: 0.0012768000000000224

---
## -msynch=synchS code/barriertest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (7425)
7425 components
No issues
Loading code/barriertest.hco```

Duration: 0.0018267999999999895

### Current Output

```
nworkers = 16
#states (7425)
7425 components
No issues
Loading code/barriertest.hco```

Duration: 0.0012101999999999946

---
##  code/trap.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3)
3 components
Non-terminating state
Loading code/trap.hco
T0: __init__() [0-7,34-38] { count: 0, done: False }
T1: main() [17-20] { count: 0, done: False }```

Duration: 0.0015272999999999815

### Current Output

```
nworkers = 16
#states (3)
3 components
Non-terminating state
Loading code/trap.hco
T0: __init__() [0-7,34-38] { count: 0, done: False }
T1: main() [17-20] { count: 0, done: False }```

Duration: 0.0016347999999999918

---
##  code/trap2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
constant cannot be an lvalue: ('ok', 'code/trap2.hny', 4, 19) ErrorToken(line=1, message="constant cannot be an lvalue: ('ok', 'code/trap2.hny', 4, 19)", column=5, lexeme='LABEL(0, ok)', filename='code/trap2.hny', is_eof_error=False)```

Duration: 0.0012959999999999916

### Current Output

```
Line 1:5 at code/trap2.hny, constant cannot be an lvalue: ('ok', 'code/trap2.hny', 4, 19)```

Duration: 0.001023099999999999

---
##  code/trap3.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (4)
Safety Violation
Loading code/trap3.hco
T0: __init__() [0-5,369-371,1039-1043,766-770,759-764,771,772,1044-1049,1096-1100] { bag: (), count: 0, countlock: False, done: False, list: (), synch: () }
T1: main() [1067-1073,782-789,793-799,1074] { bag: (), count: 0, countlock: True, done: False, list: (), synch: () }```

Duration: 0.0012630999999999892

### Current Output

```
nworkers = 16
#states (4)
Safety Violation
Loading code/trap3.hco
T0: __init__() [0-5,369-371,1039-1043,766-770,759-764,771,772,1044-1049,1096-1100] { bag: (), count: 0, countlock: False, done: False, list: (), synch: () }
T1: main() [1067-1073,782-789,793-799,1074] { bag: (), count: 0, countlock: True, done: False, list: (), synch: () }```

Duration: 0.0016850000000000198

---
##  code/trap4.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (5)
5 components
Non-terminating state
Loading code/trap4.hco
T0: __init__() [0-7,44-48] { count: 0, done: False }
T1: main() [17-30] { count: 1, done: False }```

Duration: 0.0014830999999999872

### Current Output

```
nworkers = 16
#states (5)
5 components
Non-terminating state
Loading code/trap4.hco
T0: __init__() [0-7,44-48] { count: 0, done: False }
T1: main() [17-30] { count: 1, done: False }```

Duration: 0.0011936000000000169

---
##  code/trap5.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (5)
5 components
Non-terminating state
Loading code/trap5.hco
T0: __init__() [0-7,52-56] { count: 0, done: False }
T1: main() [31-37,8-20,38] { count: 1, done: False }```

Duration: 0.001273300000000005

### Current Output

```
nworkers = 16
#states (5)
5 components
Non-terminating state
Loading code/trap5.hco
T0: __init__() [0-7,52-56] { count: 0, done: False }
T1: main() [31-37,8-20,38] { count: 1, done: False }```

Duration: 0.0012699999999999934

---
##  code/trap6.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (34)
34 components
Non-terminating state
Loading code/trap6.hco
T0: __init__() [0-5,369-371,1039-1045,766-770,759-764,771,772,1046-1049,1109-1117] { bag: (), count: 0, countlock: False, done: [ False, False ], list: (), synch: () }
T1: thread(0) [1085-1092,1050-1056,782-789,793-799,1057-1064,801-815,1065-1070,1093] { bag: (), count: 1, countlock: False, done: [ False, False ], list: (), synch: () }
T2: thread(1) [1085-1092,1050-1056,782-789,793-799,1057-1064,801-815,1065-1070,1093] { bag: (), count: 2, countlock: False, done: [ False, False ], list: (), synch: () }```

Duration: 0.0014067999999999858

### Current Output

```
nworkers = 16
#states (34)
34 components
Non-terminating state
Loading code/trap6.hco
T0: __init__() [0-5,369-371,1039-1045,766-770,759-764,771,772,1046-1049,1109-1117] { bag: (), count: 0, countlock: False, done: [ False, False ], list: (), synch: () }
T1: thread(0) [1085-1092,1050-1056,782-789,793-799,1057-1064,801-815,1065-1070,1093] { bag: (), count: 1, countlock: False, done: [ False, False ], list: (), synch: () }
T2: thread(1) [1085-1092,1050-1056,782-789,793-799,1057-1064,801-815,1065-1070,1093] { bag: (), count: 2, countlock: False, done: [ False, False ], list: (), synch: () }```

Duration: 0.0013082000000000094

---
## -msynch=synchS code/trap6.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (36)
36 components
Non-terminating state
Loading code/trap6.hco
T0: __init__() [0-5,799-805,417-421,404-415,422,423,806-809,869-877] { count: 0, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }
T1: thread(0) [845-852,810-816,425-431,455-462,817-824,464-488,508,509,825-830,853] { count: 1, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }
T2: thread(1) [845-852,810-816,425-431,455-462,817-824,464-488,508,509,825-830,853] { count: 2, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }```

Duration: 0.0011654000000000386

### Current Output

```
nworkers = 16
#states (36)
36 components
Non-terminating state
Loading code/trap6.hco
T0: __init__() [0-5,799-805,417-421,404-415,422,423,806-809,869-877] { count: 0, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }
T1: thread(0) [845-852,810-816,425-431,455-462,817-824,464-488,508,509,825-830,853] { count: 1, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }
T2: thread(1) [845-852,810-816,425-431,455-462,817-824,464-488,508,509,825-830,853] { count: 2, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }```

Duration: 0.0011902000000000301

---
##  code/hw.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (23864)
18524 components
No issues
Loading code/hw.hco```

Duration: 0.0013788000000000133

### Current Output

```
nworkers = 16
#states (23864)
18524 components
No issues
Loading code/hw.hco```

Duration: 0.001389499999999988

---
##  code/abptest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (1536)
608 components
No issues
Loading code/abptest.hco```

Duration: 0.0012828999999999757

### Current Output

```
nworkers = 16
#states (1536)
608 components
No issues
Loading code/abptest.hco```

Duration: 0.001253100000000007

---
##  code/byzbosco.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot assign to constant ('proposal', 'code/byzbosco.hny', 23, 17) ErrorToken(line=23, message="Cannot assign to constant ('proposal', 'code/byzbosco.hny', 23, 17)", column=26, lexeme='=', filename='code/byzbosco.hny', is_eof_error=False)```

Duration: 0.0010022000000000086

### Current Output

```
Line 23:17 at code/byzbosco.hny, Cannot assign to constant ('proposal', 'code/byzbosco.hny', 23, 17)```

Duration: 0.0008751999999999649

---
##  code/BBsematest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/BBsematest.hco
T0: __init__() [0-7,371-373,1111-1122,1114-1122,1114-1116,1123-1132] { BBsema: { "b_in": 1, "b_out": 1, "buf": { 1: (), 2: () } }, bag: (), list: (), synch: () }
Load: unknown address ?BBsema["Semaphore"][1]```

Duration: 0.0015312999999999577

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/BBsematest.hco
T0: __init__() [0-7,371-373,1111-1122,1114-1122,1114-1116,1123-1132] { BBsema: { "b_in": 1, "b_out": 1, "buf": { 1: (), 2: () } }, bag: (), list: (), synch: () }
Load: unknown address ?BBsema["Semaphore"][1]```

Duration: 0.0016528000000000098

---
##  code/ky.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (14)
12 components
No issues
Loading code/ky.hco```

Duration: 0.0011901000000000272

### Current Output

```
nworkers = 16
#states (14)
12 components
No issues
Loading code/ky.hco```

Duration: 0.001181500000000002

---
##  code/bosco.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (7404)
7404 components
No issues
Loading code/bosco.hco```

Duration: 0.0013128000000000029

### Current Output

```
nworkers = 16
#states (7404)
7404 components
No issues
Loading code/bosco.hco```

Duration: 0.001239099999999993

---
##  code/RWsbs.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWsbs.hco```

Duration: 0.001705399999999968

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWsbs.hco```

Duration: 0.001301400000000008

---
##  code/queuebroken.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuebroken.hco```

Duration: 0.0012898000000000076

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuebroken.hco```

Duration: 0.0015634999999999954

---
##  code/hello7.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (17)
17 components
No issues
Loading code/hello7.hco```

Duration: 0.0012458000000000191

### Current Output

```
nworkers = 16
#states (17)
17 components
No issues
Loading code/hello7.hco```

Duration: 0.0016464999999999952

---
##  code/multitest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3)
3 components
No issues
Loading code/multitest.hco```

Duration: 0.0012059000000000375

### Current Output

```
nworkers = 16
#states (3)
3 components
No issues
Loading code/multitest.hco```

Duration: 0.0014419999999999988

---
##  code/BBsemadata.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/BBsemadata.hco
T0: __init__() [0-7,371-373,1111-1122,1114-1122,1114-1116,1123-1132] { BBsema: { "b_in": 1, "b_out": 1, "buf": { 1: (), 2: () } }, bag: (), list: (), synch: () }
Load: unknown address ?BBsema["Semaphore"][1]```

Duration: 0.001423899999999978

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/BBsemadata.hco
T0: __init__() [0-7,371-373,1111-1122,1114-1122,1114-1116,1123-1132] { BBsema: { "b_in": 1, "b_out": 1, "buf": { 1: (), 2: () } }, bag: (), list: (), synch: () }
Load: unknown address ?BBsema["Semaphore"][1]```

Duration: 0.0013515000000000055

---
##  code/dinersfix2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/dinersfix2.hco
T0: __init__() [0-7] { }
Load: unknown variable left```

Duration: 0.0014967000000000175

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/dinersfix2.hco
T0: __init__() [0-7] { }
Load: unknown variable left```

Duration: 0.0018149000000000082

---
##  code/qsort.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/qsort.hco```

Duration: 0.0013385999999999676

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/qsort.hco```

Duration: 0.0011361000000000288

---
##  code/setobj.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/setobj.hco```

Duration: 0.0013345999999999636

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/setobj.hco```

Duration: 0.0018106999999999984

---
##  code/baddblwait.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/baddblwait.hco
T0: __init__() [0-2] { }
Load: unknown variable left```

Duration: 0.0012197999999999931

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/baddblwait.hco
T0: __init__() [0-2] { }
Load: unknown variable left```

Duration: 0.0012293999999999916

---
##  code/nbqueuetest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (1393)
1393 components
No issues
Loading code/nbqueuetest.hco```

Duration: 0.00185059999999998

### Current Output

```
nworkers = 16
#states (1393)
1393 components
No issues
Loading code/nbqueuetest.hco```

Duration: 0.001207899999999984

---
##  code/cssynch.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (22)
10 components
No issues
Loading code/cssynch.hco```

Duration: 0.0011913999999999536

### Current Output

```
nworkers = 16
#states (22)
10 components
No issues
Loading code/cssynch.hco```

Duration: 0.001385499999999984

---
##  code/stack3.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack3.hco```

Duration: 0.0013675999999999688

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack3.hco```

Duration: 0.0011690000000000311

---
##  code/RWqueue.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWqueue.hco
T0: __init__() [0-5,369-371,1251-1254] { bag: (), list: (), synch: () }
Load: unknown address ?Semaphore[1]```

Duration: 0.0018024999999999847

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWqueue.hco
T0: __init__() [0-5,369-371,1251-1254] { bag: (), list: (), synch: () }
Load: unknown address ?Semaphore[1]```

Duration: 0.0012314999999999965

---
##  code/DinersSema.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/DinersSema.hco
T0: __init__() [0-5,369-371,1057-1060] { bag: (), list: (), synch: () }
Load: unknown address ?Semaphore[3]```

Duration: 0.0014282999999999935

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/DinersSema.hco
T0: __init__() [0-5,369-371,1057-1060] { bag: (), list: (), synch: () }
Load: unknown address ?Semaphore[3]```

Duration: 0.001190300000000033

---
##  code/RWcv.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWcv.hco```

Duration: 0.001809900000000031

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWcv.hco```

Duration: 0.001323899999999989

---
##  code/RWmulti.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWmulti.hco
T0: __init__() [0-7,371-373,1109-1112] { RWlock: (), bag: (), list: (), synch: () }
Load: unknown address ?RWlock["Lock"][()]```

Duration: 0.0013978000000000046

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWmulti.hco
T0: __init__() [0-7,371-373,1109-1112] { RWlock: (), bag: (), list: (), synch: () }
Load: unknown address ?RWlock["Lock"][()]```

Duration: 0.0012334999999999985

---
##  code/2pc.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot operate on constant ('balance', 'code/2pc.hny', 20, 21) ErrorToken(line=20, message="Cannot operate on constant ('balance', 'code/2pc.hny', 20, 21)", column=29, lexeme='-=', filename='code/2pc.hny', is_eof_error=False)```

Duration: 0.0010475999999999819

### Current Output

```
Line 20:29 at code/2pc.hny, Cannot operate on constant ('balance', 'code/2pc.hny', 20, 21)```

Duration: 0.0008982000000000157

---
##  code/queueconc.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queueconc.hco```

Duration: 0.001354299999999975

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queueconc.hco```

Duration: 0.001648700000000003

---
##  code/queuelin.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuelin.hco```

Duration: 0.0018043999999999838

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuelin.hco```

Duration: 0.0014673000000000047

---
##  code/lockspec.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/lockspec.hco```

Duration: 0.0011580000000000479

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/lockspec.hco```

Duration: 0.0012315999999999994

---
##  code/ky2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (14)
12 components
No issues
Loading code/ky2.hco```

Duration: 0.0011261000000000188

### Current Output

```
nworkers = 16
#states (14)
12 components
No issues
Loading code/ky2.hco```

Duration: 0.0014576000000000033

---
##  code/cslock.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (97)
97 components
No issues
Loading code/cslock.hco```

Duration: 0.0013354000000000421

### Current Output

```
nworkers = 16
#states (97)
97 components
No issues
Loading code/cslock.hco```

Duration: 0.0012198000000000486

---
##  code/abp.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/abp.hco```

Duration: 0.001296599999999981

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/abp.hco```

Duration: 0.0011878000000000166

---
##  code/hello2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hello2.hco```

Duration: 0.0011036999999999852

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hello2.hco```

Duration: 0.0016147000000000244

---
##  code/actortest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9) ErrorToken(line=26, message="Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9)", column=19, lexeme='-=', filename='code/actor.hny', is_eof_error=False)```

Duration: 0.0010336000000000234

### Current Output

```
Line 26:19 at code/actor.hny, Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9)```

Duration: 0.0009274000000000227

---
##  code/hello4.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3)
3 components
No issues
Loading code/hello4.hco```

Duration: 0.0013393000000000432

### Current Output

```
nworkers = 16
#states (3)
3 components
No issues
Loading code/hello4.hco```

Duration: 0.0014325999999999506

---
##  code/actor.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9) ErrorToken(line=26, message="Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9)", column=19, lexeme='-=', filename='code/actor.hny', is_eof_error=False)```

Duration: 0.0011468000000000034

### Current Output

```
Line 26:19 at code/actor.hny, Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9)```

Duration: 0.0009350999999999665

---
##  code/chain.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (69601)
45835 components
No issues
Loading code/chain.hco```

Duration: 0.0014764999999999917

### Current Output

```
nworkers = 16
#states (69601)
45835 components
No issues
Loading code/chain.hco```

Duration: 0.0015672999999999937

---
##  code/boundedbuffer.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/boundedbuffer.hco```

Duration: 0.0012658999999999865

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/boundedbuffer.hco```

Duration: 0.0010907

---
##  code/lockintf.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/lockintf.hco```

Duration: 0.001201500000000022

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/lockintf.hco```

Duration: 0.0013969999999999816

---
##  code/taslock.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/taslock.hco```

Duration: 0.0012538000000000271

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/taslock.hco```

Duration: 0.0013422000000000156

---
##  code/RW.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RW.hco```

Duration: 0.0014762000000000386

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RW.hco```

Duration: 0.0011938000000000226

---
##  code/DinersCV2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/DinersCV2.hco
T0: __init__() [0-5,369-371,1039-1041,766-770,759-764,771,772,1042-1049,825] { bag: (), forks: [ False, False, False, False, False ], list: (), mutex: False, synch: () }
match: expected ()```

Duration: 0.0015963999999999978

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/DinersCV2.hco
T0: __init__() [0-5,369-371,1039-1041,766-770,759-764,771,772,1042-1049,825] { bag: (), forks: [ False, False, False, False, False ], list: (), mutex: False, synch: () }
match: expected ()```

Duration: 0.0013645999999999936

---
##  code/2pc2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/2pc2.hco
T0: __init__() [0-3,735-737] { list: () }
Load: unknown variable NBANKS```

Duration: 0.0014824999999999977

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/2pc2.hco
T0: __init__() [0-3,735-737] { list: () }
Load: unknown variable NBANKS```

Duration: 0.0014152000000000053

---
##  code/rsmspec.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (5048)
5048 components
No issues
Loading code/rsmspec.hco```

Duration: 0.0012291999999999859

### Current Output

```
nworkers = 16
#states (5048)
5048 components
No issues
Loading code/rsmspec.hco```

Duration: 0.0014039000000000135

---
##  code/paxos1.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (8)
Safety Violation
Loading code/paxos1.hco
T0: __init__() [0-3,356-358,4-8,359-372(choose 0),373-375,365-372(choose 0),373-375,365-367,376-379,454,455(print [ 0, 0 ]),456-462] { bag: (), network: (), proposals: [ 0, 0 ] }
Load: unknown variable leader```

Duration: 0.0012805000000000177

### Current Output

```
nworkers = 16
#states (8)
Safety Violation
Loading code/paxos1.hco
T0: __init__() [0-3,356-358,4-8,359-372(choose 0),373-375,365-372(choose 0),373-375,365-367,376-379,454,455(print [ 0, 0 ]),456-462] { bag: (), network: (), proposals: [ 0, 0 ] }
Load: unknown variable leader```

Duration: 0.0011773999999999951

---
##  code/queuespec.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuespec.hco```

Duration: 0.001303500000000013

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuespec.hco```

Duration: 0.0013116999999999712

---
##  code/RWbtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3745)
28 components
No issues
Loading code/RWbtest.hco```

Duration: 0.0014178000000000246

### Current Output

```
nworkers = 16
#states (3745)
28 components
No issues
Loading code/RWbtest.hco```

Duration: 0.0012941999999999676

---
##  code/RWhoare.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWhoare.hco```

Duration: 0.0012180999999999997

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWhoare.hco```

Duration: 0.001434600000000008

---
##  code/RWbusy.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWbusy.hco```

Duration: 0.001839000000000035

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWbusy.hco```

Duration: 0.0013931999999999833

---
##  code/qtestpar.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (16332)
16332 components
No issues
Loading code/qtestpar.hco```

Duration: 0.0013329000000000257

### Current Output

```
nworkers = 16
#states (16332)
16332 components
No issues
Loading code/qtestpar.hco```

Duration: 0.0013524999999999787

---
##  code/leader.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (22279)
15056 components
No issues
Loading code/leader.hco```

Duration: 0.0014865000000000017

### Current Output

```
nworkers = 16
#states (22279)
15056 components
No issues
Loading code/leader.hco```

Duration: 0.0015132999999999952

---
##  code/hoare.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hoare.hco```

Duration: 0.0015152999999999972

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hoare.hco```

Duration: 0.0016777999999999516

---
##  code/RWfair.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWfair.hco```

Duration: 0.0016672999999999827

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWfair.hco```

Duration: 0.0012484999999999857

---
##  code/register.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/register.hco```

Duration: 0.0013375999999999943

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/register.hco```

Duration: 0.0010567000000000215

---
##  code/lltest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/lltest.hco
T0: __init__() [0-7,371-373,1041-1047,1331-1334] { alloc: { "next": 0, "pool": () }, bag: (), linkedlist: (), list: (), synch: () }
Load: unknown address ?LinkedList[()]```

Duration: 0.0013004999999999822

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/lltest.hco
T0: __init__() [0-7,371-373,1041-1047,1331-1334] { alloc: { "next": 0, "pool": () }, bag: (), linkedlist: (), list: (), synch: () }
Load: unknown address ?LinkedList[()]```

Duration: 0.0012530000000000041

---
##  code/paxos.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (50808)
50808 components
No issues
Loading code/paxos.hco```

Duration: 0.0014144999999999852

### Current Output

```
nworkers = 16
#states (50808)
50808 components
No issues
Loading code/paxos.hco```

Duration: 0.0012853000000000447

---
##  code/RWlock.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWlock.hco
T0: __init__() [0-5,369-371,1107-1110] { bag: (), list: (), synch: () }
Load: unknown address ?Lock[()]```

Duration: 0.0017719999999999958

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWlock.hco
T0: __init__() [0-5,369-371,1107-1110] { bag: (), list: (), synch: () }
Load: unknown address ?Lock[()]```

Duration: 0.0013869000000000242

---
##  code/mesa.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/mesa.hco```

Duration: 0.0009909999999999641

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/mesa.hco```

Duration: 0.0009078999999999615

---
##  code/RWqtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWqtest.hco
T0: __init__() [0-7,371-373,1253-1256] { RWqueue: (), bag: (), list: (), synch: () }
Load: unknown address ?RWqueue["Semaphore"][1]```

Duration: 0.0013916999999999957

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWqtest.hco
T0: __init__() [0-7,371-373,1253-1256] { RWqueue: (), bag: (), list: (), synch: () }
Load: unknown address ?RWqueue["Semaphore"][1]```

Duration: 0.001419400000000015

---
##  code/BBsema.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/BBsema.hco
T0: __init__() [0-5,369-371,1109-1120,1112-1120,1112-1114,1121-1130] { b_in: 1, b_out: 1, bag: (), buf: { 1: (), 2: () }, list: (), synch: () }
Load: unknown address ?Semaphore[1]```

Duration: 0.0013635000000000175

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/BBsema.hco
T0: __init__() [0-5,369-371,1109-1120,1112-1120,1112-1114,1121-1130] { b_in: 1, b_out: 1, bag: (), buf: { 1: (), 2: () }, list: (), synch: () }
Load: unknown address ?Semaphore[1]```

Duration: 0.0011617999999999906

---
##  code/queue.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queue.hco```

Duration: 0.0013617000000000212

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queue.hco```

Duration: 0.001196999999999948

---
##  code/barrier.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/barrier.hco```

Duration: 0.001801499999999956

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/barrier.hco```

Duration: 0.0012930000000000441

---
##  code/ticket.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/ticket.hco```

Duration: 0.0013007999999999909

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/ticket.hco```

Duration: 0.00174669999999999

---
##  code/PetersonPrint.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
```

Duration: 0.0009849000000000108

### Current Output

```
```

Duration: 0.0009268000000000054

---
##  code/atomicinc.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/atomicinc.hco```

Duration: 0.0015044999999999642

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/atomicinc.hco```

Duration: 0.0015056999999999987

---
##  code/nbqueue.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/nbqueue.hco```

Duration: 0.0016664000000000123

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/nbqueue.hco```

Duration: 0.0017267999999999728

---
##  code/dinersfix.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/dinersfix.hco
T0: __init__() [0,1] { }
Load: unknown variable left```

Duration: 0.0013944000000000178

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/dinersfix.hco
T0: __init__() [0,1] { }
Load: unknown variable left```

Duration: 0.001361399999999957

---
##  code/stack2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack2.hco```

Duration: 0.0016183999999999643

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack2.hco```

Duration: 0.0014368000000000158

---
##  code/gpu.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/gpu.hco```

Duration: 0.0016541999999999946

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/gpu.hco```

Duration: 0.001354600000000039

---
##  code/triangle.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (13)
13 components
No issues
Loading code/triangle.hco```

Duration: 0.0013818999999999915

### Current Output

```
nworkers = 16
#states (13)
13 components
No issues
Loading code/triangle.hco```

Duration: 0.0012908999999999837

---
##  code/barrier1.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3614)
3614 components
No issues
Loading code/barrier1.hco```

Duration: 0.00126390000000004

### Current Output

```
nworkers = 16
#states (3614)
3614 components
No issues
Loading code/barrier1.hco```

Duration: 0.0013568000000000469

---
##  code/spinlockInv.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (473)
148 components
No issues
Loading code/spinlockInv.hco```

Duration: 0.0012120999999999937

### Current Output

```
nworkers = 16
#states (473)
148 components
No issues
Loading code/spinlockInv.hco```

Duration: 0.0011271999999999949

---
##  code/bosco2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (633)
633 components
No issues
Loading code/bosco2.hco```

Duration: 0.0011992000000000114

### Current Output

```
nworkers = 16
#states (633)
633 components
No issues
Loading code/bosco2.hco```

Duration: 0.001165499999999986

---
##  code/paxos2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/paxos2.hco```

Duration: 0.0013704000000000494

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/paxos2.hco```

Duration: 0.0013616999999999657

---
##  code/bqueue.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/bqueue.hco```

Duration: 0.0012819000000000025

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/bqueue.hco```

Duration: 0.0011189000000000338

---
##  code/hello6.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/hello6.hco```

Duration: 0.0012990999999999975

### Current Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/hello6.hco```

Duration: 0.0012106000000000061

---
##  code/stack1.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack1.hco```

Duration: 0.0012514000000000136

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack1.hco```

Duration: 0.0014667999999999903

---
##  code/hello5.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hello5.hco```

Duration: 0.0013713000000000197

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hello5.hco```

Duration: 0.0014121999999999746

---
##  code/abd.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/abd.hco```

Duration: 0.0016139000000000014

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/abd.hco```

Duration: 0.0015685999999999756

---
##  code/hello8.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/hello8.hco```

Duration: 0.0012795000000000445

### Current Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/hello8.hco```

Duration: 0.0012013999999999636

---
##  code/stack4.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack4.hco```

Duration: 0.0015197000000000127

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack4.hco```

Duration: 0.0016206000000000276

---
##  code/BBhoare.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/BBhoare.hco```

Duration: 0.0014441000000000037

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/BBhoare.hco```

Duration: 0.0014353000000000282

---
##  code/RWcheat.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWcheat.hco```

Duration: 0.0011508999999999547

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWcheat.hco```

Duration: 0.0015029000000000292

---
##  code/stacktest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Can't import module stack from ['code/stacktest.hny'] ErrorToken(line=1, message="Can't import module stack from ['code/stacktest.hny']", column=6, lexeme='stack', filename='code/stacktest.hny', is_eof_error=False)```

Duration: 0.0009004000000000234

### Current Output

```
Line 1:6 at code/stacktest.hny, Can't import module stack from ['code/stacktest.hny']```

Duration: 0.0007330000000000392

---
##  code/queueMS.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queueMS.hco```

Duration: 0.0012693000000000287

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queueMS.hco```

Duration: 0.0014079000000000175

---
##  code/abdtest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (148)
148 components
No issues
Loading code/abdtest.hco```

Duration: 0.001195899999999972

### Current Output

```
nworkers = 16
#states (148)
148 components
No issues
Loading code/abdtest.hco```

Duration: 0.0011114000000000401

---
##  code/locksusp.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/locksusp.hco```

Duration: 0.0011484999999999967

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/locksusp.hco```

Duration: 0.0011620999999999992

---
##  code/RWbusychk.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWbusychk.hco
T0: __init__() [0-3,145-156,147-156,147-156,147-149,157-169,160-169,160-169,160-162,170-174] { RW: () }
Load: unknown address ?acquire_wlock[()]```

Duration: 0.0013050000000000006

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWbusychk.hco
T0: __init__() [0-3,145-156,147-156,147-156,147-149,157-169,160-169,160-169,160-162,170-174] { RW: () }
Load: unknown address ?acquire_wlock[()]```

Duration: 0.00110509999999997

---
##  code/2pc1.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot operate on constant ('balance', 'code/2pc1.hny', 16, 21) ErrorToken(line=16, message="Cannot operate on constant ('balance', 'code/2pc1.hny', 16, 21)", column=29, lexeme='-=', filename='code/2pc1.hny', is_eof_error=False)```

Duration: 0.0008441999999999616

### Current Output

```
Line 16:29 at code/2pc1.hny, Cannot operate on constant ('balance', 'code/2pc1.hny', 16, 21)```

Duration: 0.0008993999999999946

---
##  code/needhamschroeder.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (502)
Safety Violation
Loading code/needhamschroeder.hco
T0: __init__() [0-4(choose "Corey"),5,6,408-420] { dest: "Corey", network: {} }
T1: alice() [19-32,7-17,33-35] { dest: "Corey", network: { { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" } } }
T3: corey() [225-243(choose { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" }),244-251,256-282,295-335,313-335,313-315,336-366,344-366,344-346,367-390,304-335,313-335,313-315,336-366,344-366,344-346,367-390,304-306,391-393,298-335,313-335,313-315,336-366,344-366,344-346,367-390,304-335,313-335,313-315,336-366,344-366,344-346,367-390,304-306,391-393,298-300,394-399(choose { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }),400,7-17,401-403,228-231] { dest: "Corey", network: { { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }, { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" } } }
T2: bob() [101-113(choose { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }),114-136,138,139,144-167,7-17,168-171] { dest: "Corey", network: { { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }, { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" }, { "contents": { "nonce": "nonceA", "nonce2": "nonceB", "type": 2 }, "dst": "Alice" } } }
T1: alice() [36-45(choose { "contents": { "nonce": "nonceA", "nonce2": "nonceB", "type": 2 }, "dst": "Alice" }),46-68,70,71,76-96,7-17,97-99] { dest: "Corey", network: { { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }, { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" }, { "contents": { "nonce": "nonceA", "nonce2": "nonceB", "type": 2 }, "dst": "Alice" }, { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Corey" } } }
T3: corey() [232-243(choose { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Corey" }),244-251,256-282,295-335,313-335,313-315,336-366,344-366,344-366,344-346,367-390,304-335,313-335,313-315,336-366,344-366,344-366,344-346,367-390,304-335,313-335,313-315,336-366,344-366,344-366,344-346,367-390,304-306,391-393,298-335,313-335,313-315,336-366,344-366,344-366,344-346,367-390,304-335,313-335,313-315,336-366,344-366,344-366,344-346,367-390,304-335,313-335,313-315,336-366,344-366,344-366,344-346,367-390,304-306,391-393,298-300,394-399(choose { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Bob" }),400,7-17,401-403,228-231] { dest: "Corey", network: { { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }, { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" }, { "contents": { "nonce": "nonceA", "nonce2": "nonceB", "type": 2 }, "dst": "Alice" }, { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Bob" }, { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Corey" } } }
T2: bob() [172-181(choose { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Bob" }),182-205,208,209,213-219] { dest: "Corey", network: { { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }, { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" }, { "contents": { "nonce": "nonceA", "nonce2": "nonceB", "type": 2 }, "dst": "Alice" }, { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Bob" }, { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Corey" } } }
Harmony assertion failed```

Duration: 0.0014185000000000447

### Current Output

```
nworkers = 16
#states (502)
Safety Violation
Loading code/needhamschroeder.hco
T0: __init__() [0-4(choose "Corey"),5,6,408-420] { dest: "Corey", network: {} }
T1: alice() [19-32,7-17,33-35] { dest: "Corey", network: { { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" } } }
T3: corey() [225-243(choose { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" }),244-251,256-282,295-335,313-335,313-315,336-366,344-366,344-346,367-390,304-335,313-335,313-315,336-366,344-366,344-346,367-390,304-306,391-393,298-335,313-335,313-315,336-366,344-366,344-346,367-390,304-335,313-335,313-315,336-366,344-366,344-346,367-390,304-306,391-393,298-300,394-399(choose { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }),400,7-17,401-403,228-231] { dest: "Corey", network: { { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }, { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" } } }
T2: bob() [101-113(choose { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }),114-136,138,139,144-167,7-17,168-171] { dest: "Corey", network: { { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }, { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" }, { "contents": { "nonce": "nonceA", "nonce2": "nonceB", "type": 2 }, "dst": "Alice" } } }
T1: alice() [36-45(choose { "contents": { "nonce": "nonceA", "nonce2": "nonceB", "type": 2 }, "dst": "Alice" }),46-68,70,71,76-96,7-17,97-99] { dest: "Corey", network: { { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }, { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" }, { "contents": { "nonce": "nonceA", "nonce2": "nonceB", "type": 2 }, "dst": "Alice" }, { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Corey" } } }
T3: corey() [232-243(choose { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Corey" }),244-251,256-282,295-335,313-335,313-315,336-366,344-366,344-366,344-346,367-390,304-335,313-335,313-315,336-366,344-366,344-366,344-346,367-390,304-335,313-335,313-315,336-366,344-366,344-366,344-346,367-390,304-306,391-393,298-335,313-335,313-315,336-366,344-366,344-366,344-346,367-390,304-335,313-335,313-315,336-366,344-366,344-366,344-346,367-390,304-335,313-335,313-315,336-366,344-366,344-366,344-346,367-390,304-306,391-393,298-300,394-399(choose { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Bob" }),400,7-17,401-403,228-231] { dest: "Corey", network: { { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }, { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" }, { "contents": { "nonce": "nonceA", "nonce2": "nonceB", "type": 2 }, "dst": "Alice" }, { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Bob" }, { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Corey" } } }
T2: bob() [172-181(choose { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Bob" }),182-205,208,209,213-219] { dest: "Corey", network: { { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Bob" }, { "contents": { "initiator": "Alice", "nonce": "nonceA", "type": 1 }, "dst": "Corey" }, { "contents": { "nonce": "nonceA", "nonce2": "nonceB", "type": 2 }, "dst": "Alice" }, { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Bob" }, { "contents": { "nonce": "nonceB", "type": 3 }, "dst": "Corey" } } }
Harmony assertion failed```

Duration: 0.0016826999999999814

---
##  code/linkedlist.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/linkedlist.hco```

Duration: 0.0013526999999999845

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/linkedlist.hco```

Duration: 0.0012410000000000476

---
##  code/barriertest2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (6272)
6272 components
No issues
Loading code/barriertest2.hco```

Duration: 0.0012490000000000556

### Current Output

```
nworkers = 16
#states (6272)
6272 components
No issues
Loading code/barriertest2.hco```

Duration: 0.0012720000000000509

---
##  code/oo.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/oo.hco```

Duration: 0.0011607000000000145

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/oo.hco```

Duration: 0.0010748000000000424

---
##  code/queuefix.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuefix.hco```

Duration: 0.0017584999999999962

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuefix.hco```

Duration: 0.0012092999999999687

---
##  code/hello3.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (3)
3 components
No issues
Loading code/hello3.hco```

Duration: 0.0013016999999999612

### Current Output

```
nworkers = 16
#states (3)
3 components
No issues
Loading code/hello3.hco```

Duration: 0.0012864000000000209

---
##  code/queueseq.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queueseq.hco```

Duration: 0.0012468999999999397

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queueseq.hco```

Duration: 0.0012503999999999849

---
##  code/hello1.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hello1.hco```

Duration: 0.0013222999999999985

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hello1.hco```

Duration: 0.0012689999999999646

---
##  code/consensus.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (4540)
4540 components
No issues
Loading code/consensus.hco```

Duration: 0.001624599999999976

### Current Output

```
nworkers = 16
#states (4540)
4540 components
No issues
Loading code/consensus.hco```

Duration: 0.001178699999999977

---