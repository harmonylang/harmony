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

Duration: 0.0036166000000000045

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/bag.hco```

Duration: 0.0043199000000000015

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

Duration: 0.0027106000000000074

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synchBusy.hco```

Duration: 0.0036390000000000033

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

Duration: 0.0024229999999999946

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synchImprecise.hco```

Duration: 0.003438400000000008

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

Duration: 0.002331700000000006

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synch.hco```

Duration: 0.002731300000000006

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

Duration: 0.0034131999999999912

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/alloc.hco```

Duration: 0.0028910000000000047

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

Duration: 0.002105699999999988

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/hoare.hco```

Duration: 0.003008699999999989

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

Duration: 0.0036178999999999933

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synchS.hco```

Duration: 0.002971200000000007

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

Duration: 0.0023143000000000052

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/set.hco```

Duration: 0.0034564000000000122

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

Duration: 0.002664799999999995

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/list.hco```

Duration: 0.002150100000000002

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

Duration: 0.003086200000000011

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/prog1.hco```

Duration: 0.0024722999999999967

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

Duration: 0.0024208000000000007

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

Duration: 0.002912800000000007

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

Duration: 0.002874700000000008

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

Duration: 0.0026734999999999953

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

Duration: 0.002539399999999997

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

Duration: 0.0029939000000000215

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

Duration: 0.002538499999999999

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

Duration: 0.0023222999999999994

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

Duration: 0.0032355000000000023

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

Duration: 0.0027348000000000094

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

Duration: 0.0025975000000000026

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

Duration: 0.003740300000000002

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

Duration: 0.002142900000000003

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

Duration: 0.0017247999999999986

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

Duration: 0.0031225000000000003

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

Duration: 0.003121600000000002

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

Duration: 0.0023138000000000047

### Current Output

```
nworkers = 16
#states (104)
37 components
No issues
Loading code/Peterson.hco```

Duration: 0.003493999999999997

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

Duration: 0.0025915000000000243

### Current Output

```
nworkers = 16
#states (104)
37 components
No issues
Loading code/PetersonInductive.hco```

Duration: 0.0022474000000000105

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

Duration: 0.0032314999999999983

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

Duration: 0.003307399999999988

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

Duration: 0.003141199999999983

### Current Output

```
nworkers = 16
#states (104)
37 components
No issues
Loading code/PetersonMethod.hco```

Duration: 0.0036539000000000155

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

Duration: 0.003372099999999989

### Current Output

```
nworkers = 16
#states (5462)
Safety Violation
Loading code/clock.hco
T0: __init__() [0,1,132-139,2-21,140-144,2-21,145-172,179-195,23-45,81-131,196-205,23-45,81-131,206-226,161-172,179-195,23-45,81-131,196-205,23-45,81-131,206-226,161-172,179-195,23-45,81-131,196-205,23-45,81-131,206-226,161-172,179-195,23-80,31-80,31-80,31-45,81-131,196-205,23-45,81-131,206-226,161-168,173-178(choose 2),179-195,23-30,115-131,196-205,23-30,115-131,206-226,161-168,173-178(choose 1),179-195,23-80,31-45,81-131,196-205,23-30,115-131,206-226,161-168,173-178(choose 2),179-195,23-30,115-131,196-205,23-30,115-131,206-226,161-168,173-178(choose 5),179-195,23-80,31-80,31-80,31-45,81-131,196-205,23-80,31-80,31-80,31-80,31-45,81-131,206-226,161-168,173-178(choose 1),179-195,23-30,115-131,196-205,23-45,81-131,206-226,161-168,173-178(choose 2),179-195,23-30,115-131,196-205,23-45,81-131,206-218] { clock3: { "entries": [ 5, 2, 1 ], "hand": 1, "misses": 6, "recent": { 1, 2, 5 } }, clock4: { "entries": [ 5, 1, 2, 4 ], "hand": 3, "misses": 7, "recent": { 1, 2, 5 } }, refs: [ 1, 2, 3, 4, 2, 1, 2, 5, 1, 2 ] }
Harmony assertion failed```

Duration: 0.002895599999999998

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

Duration: 0.002536499999999997

### Current Output

```
nworkers = 16
#states (473)
148 components
No issues
Loading code/spinlock.hco```

Duration: 0.002324799999999988

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

Duration: 0.0029426999999999925

### Current Output

```
nworkers = 16
#states (57)
57 components
No issues
Loading code/UpLock.hco```

Duration: 0.0027288000000000034

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

Duration: 0.0024766999999999983

### Current Output

```
nworkers = 16
#states (59)
59 components
No issues
Loading code/UpLock.hco```

Duration: 0.002929199999999993

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

Duration: 0.002544700000000011

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

Duration: 0.003455999999999987

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
T0: __init__() [0-5,369-371,1039-1054,766-770,759-764,771,772,1055-1058(choose 1),1059-1062,1044-1054,766-770,759-764,771,772,1055-1058(choose 0),1059-1062,1044-1046,1063-1066,1094,1183-1197(choose 0),1198-1201(choose 1),1202-1205,1185-1197(choose 0),1198-1201(choose 1),1202-1205,1185-1187,1206,1207] { accounts: [ { "balance": 1, "lock": False }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }
T2: customer(2, 0, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-785] { accounts: [ { "balance": 1, "lock": False }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }
T1: customer(1, 0, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-789,793-799,1132-1153,801-815,1154,1155,1179-1182] { accounts: [ { "balance": 0, "lock": False }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }
T2: customer(2, 0, 1) [786-789,793-799,1132-1153,801-804] { accounts: [ { "balance": -1, "lock": True }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }```

Duration: 0.00267199999999998

### Current Output

```
nworkers = 16
#states (4110)
Invariant Violation
Loading code/atm.hco
T0: __init__() [0-5,369-371,1039-1054,766-770,759-764,771,772,1055-1058(choose 1),1059-1062,1044-1054,766-770,759-764,771,772,1055-1058(choose 0),1059-1062,1044-1046,1063-1066,1094,1183-1197(choose 0),1198-1201(choose 1),1202-1205,1185-1197(choose 0),1198-1201(choose 1),1202-1205,1185-1187,1206,1207] { accounts: [ { "balance": 1, "lock": False }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }
T1: customer(1, 0, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-785] { accounts: [ { "balance": 1, "lock": False }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }
T2: customer(2, 0, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-789,793-799,1132-1153,801-815,1154,1155,1179-1182] { accounts: [ { "balance": 0, "lock": False }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }
T1: customer(1, 0, 1) [786-789,793-799,1132-1153,801-804] { accounts: [ { "balance": -1, "lock": True }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }```

Duration: 0.0020619000000000054

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

Duration: 0.002543899999999988

### Current Output

```
nworkers = 16
#states (80)
80 components
No issues
Loading code/queuedemo.hco```

Duration: 0.0029983000000000093

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

Duration: 0.0036260999999999932

### Current Output

```
nworkers = 16
#states (80)
80 components
No issues
Loading code/queuedemo.hco```

Duration: 0.0030010000000000037

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

Duration: 0.0024454999999999893

### Current Output

```
nworkers = 16
#states (600)
600 components
No issues
Loading code/qtestseq.hco```

Duration: 0.00311740000000002

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

Duration: 0.003506199999999987

### Current Output

```
nworkers = 16
#states (274)
274 components
No issues
Loading code/qtest1.hco```

Duration: 0.0033823000000000047

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

Duration: 0.0029716000000000187

### Current Output

```
nworkers = 16
#states (274)
274 components
No issues
Loading code/qtest1.hco```

Duration: 0.003725299999999987

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

Duration: 0.0024411000000000294

### Current Output

```
nworkers = 16
#states (55)
55 components
No issues
Loading code/qtest2.hco```

Duration: 0.0033394999999999953

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

Duration: 0.0022706000000000115

### Current Output

```
nworkers = 16
#states (55)
55 components
No issues
Loading code/qtest2.hco```

Duration: 0.002902799999999983

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

Duration: 0.0030212000000000017

### Current Output

```
nworkers = 16
#states (3225)
3225 components
No issues
Loading code/qtest3.hco```

Duration: 0.002656000000000047

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

Duration: 0.002031800000000028

### Current Output

```
nworkers = 16
#states (3225)
3225 components
No issues
Loading code/qtest3.hco```

Duration: 0.0029681999999999764

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

Duration: 0.0027562999999999893

### Current Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/qtest4.hco```

Duration: 0.002536399999999994

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

Duration: 0.0024269000000000096

### Current Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/qtest4.hco```

Duration: 0.002241499999999952

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

Duration: 0.005218900000000026

### Current Output

```
nworkers = 16
#states (2127239)
2127239 components
No issues
Loading code/qtestconc.hco```

Duration: 0.006919200000000014

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

Duration: 0.0040636000000000005

### Current Output

```
nworkers = 16
#states (3430951)
3430951 components
No issues
Loading code/qtestconc.hco```

Duration: 0.006051899999999999

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

Duration: 0.001339800000000002

### Current Output

```
nworkers = 16
#states (3125)
3125 components
No issues
Loading code/queuedemo.hco```

Duration: 0.0017612999999999657

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

Duration: 0.0016925999999999886

### Current Output

```
nworkers = 16
#states (3287)
3287 components
No issues
Loading code/queuedemo.hco```

Duration: 0.0015580000000000038

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

Duration: 0.0012765000000000137

### Current Output

```
nworkers = 16
#states (12368)
12368 components
No issues
Loading code/intsettest.hco```

Duration: 0.001956499999999972

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

Duration: 0.0015592999999999857

### Current Output

```
nworkers = 16
#states (18377)
18377 components
No issues
Loading code/intsettest.hco```

Duration: 0.0014207999999999998

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

Duration: 0.001248199999999977

### Current Output

```
nworkers = 16
#states (135)
27 components
No issues
Loading code/RWtest.hco```

Duration: 0.001605499999999982

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

Duration: 0.0011956999999999662

### Current Output

```
nworkers = 16
#states (135)
27 components
No issues
Loading code/RWtest.hco```

Duration: 0.0010676000000000019

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

Duration: 0.0012907999999999809

### Current Output

```
nworkers = 16
#states (1943)
619 components
No issues
Loading code/RWtest.hco```

Duration: 0.0013521000000000227

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

Duration: 0.001418699999999995

### Current Output

```
nworkers = 16
#states (4212)
897 components
No issues
Loading code/RWtest.hco```

Duration: 0.0014838999999999825

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

Duration: 0.001408699999999985

### Current Output

```
nworkers = 16
#states (1438)
449 components
No issues
Loading code/RWtest.hco```

Duration: 0.00155540000000004

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

Duration: 0.001370299999999991

### Current Output

```
nworkers = 16
#states (3137)
635 components
No issues
Loading code/RWtest.hco```

Duration: 0.0015233000000000052

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

Duration: 0.0016805999999999766

### Current Output

```
nworkers = 16
#states (1175)
1175 components
No issues
Loading code/BBtest.hco```

Duration: 0.0013468999999999842

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

Duration: 0.0013139999999999818

### Current Output

```
nworkers = 16
#states (4127)
4127 components
No issues
Loading code/BBtest.hco```

Duration: 0.001505100000000037

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

Duration: 0.0014024999999999732

### Current Output

```
nworkers = 16
#states (1902)
406 components
No issues
Loading code/RWtest.hco```

Duration: 0.001387900000000053

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

Duration: 0.0016999999999999793

### Current Output

```
nworkers = 16
#states (4301)
666 components
No issues
Loading code/RWtest.hco```

Duration: 0.0015516999999999892

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

Duration: 0.0015514999999999834

### Current Output

```
nworkers = 16
#states (454)
454 components
No issues
Loading code/qsorttest.hco```

Duration: 0.0013809999999999656

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

Duration: 0.0014688000000000478

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

Duration: 0.0014230000000000076

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

Duration: 0.0013629000000000002

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

Duration: 0.0016227999999999798

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

Duration: 0.0015311000000000075

### Current Output

```
nworkers = 16
#states (111679)
39194 components
No issues
Loading code/DinersCV.hco```

Duration: 0.0014461000000000057

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

Duration: 0.0041180000000000105

### Current Output

```
nworkers = 16
#states (2293519)
441764 components
No issues
Loading code/DinersCV.hco```

Duration: 0.003330999999999973

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

Duration: 0.00153979999999998

### Current Output

```
nworkers = 16
#states (86214)
5589 components
No issues
Loading code/DinersAvoid.hco```

Duration: 0.0016571000000000224

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

Duration: 0.0014559999999999573

### Current Output

```
nworkers = 16
#states (152874)
10504 components
No issues
Loading code/DinersAvoid.hco```

Duration: 0.001923800000000031

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

Duration: 0.0011969000000000007

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

Duration: 0.0013712000000000168

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

Duration: 0.0011847000000000385

### Current Output

```
nworkers = 16
#states (601)
601 components
No issues
Loading code/counter.hco```

Duration: 0.0013161999999999896

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

Duration: 0.001220999999999972

### Current Output

```
nworkers = 16
#states (1664)
1664 components
No issues
Loading code/qbarrier.hco```

Duration: 0.0013352000000000364

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

Duration: 0.0013800999999999952

### Current Output

```
nworkers = 16
#states (4927)
4927 components
No issues
Loading code/qbarrier.hco```

Duration: 0.0014253000000000182

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

Duration: 0.0012064999999999992

### Current Output

```
nworkers = 16
#states (2802)
2802 components
No issues
Loading code/barriertest.hco```

Duration: 0.0014010999999999885

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

Duration: 0.0012878000000000056

### Current Output

```
nworkers = 16
#states (7425)
7425 components
No issues
Loading code/barriertest.hco```

Duration: 0.0013928999999999747

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

Duration: 0.0014107999999999898

### Current Output

```
nworkers = 16
#states (3)
3 components
Non-terminating state
Loading code/trap.hco
T0: __init__() [0-7,34-38] { count: 0, done: False }
T1: main() [17-20] { count: 0, done: False }```

Duration: 0.0014371000000000245

---
##  code/trap2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
constant cannot be an lvalue: ('ok', 'code/trap2.hny', 4, 19) ErrorToken(line=1, message="constant cannot be an lvalue: ('ok', 'code/trap2.hny', 4, 19)", column=5, lexeme='LABEL(0, ok)', filename='code/trap2.hny', is_eof_error=False)```

Duration: 0.0010709999999999886

### Current Output

```
Line 1:5 at code/trap2.hny, constant cannot be an lvalue: ('ok', 'code/trap2.hny', 4, 19)```

Duration: 0.0008906000000000192

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

Duration: 0.0012976000000000099

### Current Output

```
nworkers = 16
#states (4)
Safety Violation
Loading code/trap3.hco
T0: __init__() [0-5,369-371,1039-1043,766-770,759-764,771,772,1044-1049,1096-1100] { bag: (), count: 0, countlock: False, done: False, list: (), synch: () }
T1: main() [1067-1073,782-789,793-799,1074] { bag: (), count: 0, countlock: True, done: False, list: (), synch: () }```

Duration: 0.00150469999999997

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

Duration: 0.0013240000000000474

### Current Output

```
nworkers = 16
#states (5)
5 components
Non-terminating state
Loading code/trap4.hco
T0: __init__() [0-7,44-48] { count: 0, done: False }
T1: main() [17-30] { count: 1, done: False }```

Duration: 0.0014413999999999816

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

Duration: 0.0011881999999999726

### Current Output

```
nworkers = 16
#states (5)
5 components
Non-terminating state
Loading code/trap5.hco
T0: __init__() [0-7,52-56] { count: 0, done: False }
T1: main() [31-37,8-20,38] { count: 1, done: False }```

Duration: 0.001435799999999987

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

Duration: 0.0011281999999999681

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

Duration: 0.0015391000000000155

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

Duration: 0.0012524999999999897

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

Duration: 0.0012498999999999705

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

Duration: 0.0013218000000000396

### Current Output

```
nworkers = 16
#states (23864)
18524 components
No issues
Loading code/hw.hco```

Duration: 0.0015171999999999963

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

Duration: 0.0016864999999999797

### Current Output

```
nworkers = 16
#states (1536)
608 components
No issues
Loading code/abptest.hco```

Duration: 0.001615000000000033

---
##  code/byzbosco.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot assign to constant ('proposal', 'code/byzbosco.hny', 23, 17) ErrorToken(line=23, message="Cannot assign to constant ('proposal', 'code/byzbosco.hny', 23, 17)", column=26, lexeme='=', filename='code/byzbosco.hny', is_eof_error=False)```

Duration: 0.0010338000000000291

### Current Output

```
Line 23:17 at code/byzbosco.hny, Cannot assign to constant ('proposal', 'code/byzbosco.hny', 23, 17)```

Duration: 0.0010650999999999855

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

Duration: 0.001416200000000034

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/BBsematest.hco
T0: __init__() [0-7,371-373,1111-1122,1114-1122,1114-1116,1123-1132] { BBsema: { "b_in": 1, "b_out": 1, "buf": { 1: (), 2: () } }, bag: (), list: (), synch: () }
Load: unknown address ?BBsema["Semaphore"][1]```

Duration: 0.0016287999999999858

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

Duration: 0.0011472000000000149

### Current Output

```
nworkers = 16
#states (14)
12 components
No issues
Loading code/ky.hco```

Duration: 0.0017753999999999825

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

Duration: 0.0013645999999999936

### Current Output

```
nworkers = 16
#states (7404)
7404 components
No issues
Loading code/bosco.hco```

Duration: 0.0013169000000000097

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

Duration: 0.0013608999999999982

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWsbs.hco```

Duration: 0.0014593999999999996

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

Duration: 0.0013272000000000284

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuebroken.hco```

Duration: 0.0014644999999999797

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

Duration: 0.0012765000000000137

### Current Output

```
nworkers = 16
#states (17)
17 components
No issues
Loading code/hello7.hco```

Duration: 0.0011412000000000089

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

Duration: 0.0013132000000000144

### Current Output

```
nworkers = 16
#states (3)
3 components
No issues
Loading code/multitest.hco```

Duration: 0.0013325000000000142

---
##  code/BBsemadata.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('atomic', 'code/BBsemadata.hny', 13, 9), but expected expression ErrorToken(line=13, message="Parse error in statement. Got ('atomic', 'code/BBsemadata.hny', 13, 9), but expected expression", column=9, lexeme='atomic', filename='code/BBsemadata.hny', is_eof_error=False)```

Duration: 0.0009935999999999834

### Current Output

```
```

Duration: 0.0009897999999999851

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

Duration: 0.0011461999999999861

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/dinersfix2.hco
T0: __init__() [0-7] { }
Load: unknown variable left```

Duration: 0.0015767999999999893

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

Duration: 0.0014475999999999933

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/qsort.hco```

Duration: 0.0015892000000000128

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

Duration: 0.0012588000000000044

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/setobj.hco```

Duration: 0.0013384000000000174

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

Duration: 0.0012781000000000042

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/baddblwait.hco
T0: __init__() [0-2] { }
Load: unknown variable left```

Duration: 0.0013355999999999923

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

Duration: 0.001443899999999998

### Current Output

```
nworkers = 16
#states (1393)
1393 components
No issues
Loading code/nbqueuetest.hco```

Duration: 0.0013915999999999928

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

Duration: 0.0013603000000000365

### Current Output

```
nworkers = 16
#states (22)
10 components
No issues
Loading code/cssynch.hco```

Duration: 0.0012529000000000012

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

Duration: 0.0013429000000000357

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack3.hco```

Duration: 0.0011365000000000403

---
##  code/RWqueue.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWqueue.hco
T0: __init__() [0-5,369-371,1251-1254] { bag: (), list: (), synch: () }
Load: unknown address ?Semaphore[1]```

Duration: 0.0015874000000000166

### Current Output

```
```

Duration: 0.0011971000000000065

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

Duration: 0.0012647999999999548

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/DinersSema.hco
T0: __init__() [0-5,369-371,1057-1060] { bag: (), list: (), synch: () }
Load: unknown address ?Semaphore[3]```

Duration: 0.00152540000000001

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

Duration: 0.0013859999999999983

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWcv.hco```

Duration: 0.0014533999999999936

---
##  code/RWmulti.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWmulti.hco
T0: __init__() [0-7,371-373,1109-1112] { RWlock: (), bag: (), list: (), synch: () }
Load: unknown address ?RWlock["Lock"][()]```

Duration: 0.001360199999999978

### Current Output

```
Line 19:8 at code/RWmulti.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}```

Duration: 0.0010787999999999909

---
##  code/2pc.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot operate on constant ('balance', 'code/2pc.hny', 20, 21) ErrorToken(line=20, message="Cannot operate on constant ('balance', 'code/2pc.hny', 20, 21)", column=29, lexeme='-=', filename='code/2pc.hny', is_eof_error=False)```

Duration: 0.0010125000000000273

### Current Output

```
Line 20:29 at code/2pc.hny, Cannot operate on constant ('balance', 'code/2pc.hny', 20, 21)```

Duration: 0.001071500000000003

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

Duration: 0.0015000000000000013

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queueconc.hco```

Duration: 0.002025700000000019

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

Duration: 0.0013757000000000352

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuelin.hco```

Duration: 0.0013385999999999676

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

Duration: 0.0012841999999999576

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/lockspec.hco```

Duration: 0.0013062000000000351

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

Duration: 0.0011180999999999552

### Current Output

```
nworkers = 16
#states (14)
12 components
No issues
Loading code/ky2.hco```

Duration: 0.0013739999999999863

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

Duration: 0.0012559999999999794

### Current Output

```
nworkers = 16
#states (97)
97 components
No issues
Loading code/cslock.hco```

Duration: 0.0015228999999999937

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

Duration: 0.0012265000000000192

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/abp.hco```

Duration: 0.0013482000000000216

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

Duration: 0.001235499999999945

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hello2.hco```

Duration: 0.0012972999999999457

---
##  code/actortest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9) ErrorToken(line=26, message="Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9)", column=19, lexeme='-=', filename='code/actor.hny', is_eof_error=False)```

Duration: 0.0010352000000000139

### Current Output

```
Line 26:19 at code/actor.hny, Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9)```

Duration: 0.0010931999999999054

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

Duration: 0.0010867999999999434

### Current Output

```
nworkers = 16
#states (3)
3 components
No issues
Loading code/hello4.hco```

Duration: 0.0016192999999999902

---
##  code/actor.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9) ErrorToken(line=26, message="Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9)", column=19, lexeme='-=', filename='code/actor.hny', is_eof_error=False)```

Duration: 0.001410699999999987

### Current Output

```
Line 26:19 at code/actor.hny, Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9)```

Duration: 0.0011207000000000855

---
##  code/chain.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
nworkers = 16
#states (69601)
45835 components
No issues
Loading code/chain.hco```

Duration: 0.0018129000000000062

### Current Output

```
Line 24:51 at code/chain.hny, extraneous input 'indent' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 25:77 at code/chain.hny, mismatched input 'newLine' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING, INDENT}

Line 32:0 at code/chain.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}```

Duration: 0.0014849999999999586

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

Duration: 0.0014359999999999928

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/boundedbuffer.hco```

Duration: 0.0013130000000000086

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

Duration: 0.0013780999999999377

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/lockintf.hco```

Duration: 0.0013404000000000194

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

Duration: 0.001202700000000001

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/taslock.hco```

Duration: 0.0012331999999999343

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

Duration: 0.00125390000000003

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RW.hco```

Duration: 0.001237900000000014

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

Duration: 0.0011493999999999671

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/DinersCV2.hco
T0: __init__() [0-5,369-371,1039-1041,766-770,759-764,771,772,1042-1049,825] { bag: (), forks: [ False, False, False, False, False ], list: (), mutex: False, synch: () }
match: expected ()```

Duration: 0.0013027999999999373

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

Duration: 0.0012410000000000476

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/2pc2.hco
T0: __init__() [0-3,735-737] { list: () }
Load: unknown variable NBANKS```

Duration: 0.0012956999999998997

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

Duration: 0.001297399999999893

### Current Output

```
nworkers = 16
#states (5048)
5048 components
No issues
Loading code/rsmspec.hco```

Duration: 0.0012408000000000419

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

Duration: 0.001339800000000002

### Current Output

```
nworkers = 16
#states (8)
Safety Violation
Loading code/paxos1.hco
T0: __init__() [0-3,356-358,4-8,359-372(choose 0),373-375,365-372(choose 0),373-375,365-367,376-379,454,455(print [ 0, 0 ]),456-462] { bag: (), network: (), proposals: [ 0, 0 ] }
Load: unknown variable leader```

Duration: 0.00124829999999998

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

Duration: 0.0012510000000000021

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuespec.hco```

Duration: 0.0013369000000000852

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

Duration: 0.001994700000000016

### Current Output

```
nworkers = 16
#states (3745)
28 components
No issues
Loading code/RWbtest.hco```

Duration: 0.00141710000000006

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

Duration: 0.0017812000000000383

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWhoare.hco```

Duration: 0.0013471000000000455

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

Duration: 0.0017806999999999684

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWbusy.hco```

Duration: 0.00147150000000007

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

Duration: 0.0019871999999999668

### Current Output

```
nworkers = 16
#states (16332)
16332 components
No issues
Loading code/qtestpar.hco```

Duration: 0.0016095999999999888

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

Duration: 0.0014351000000000225

### Current Output

```
nworkers = 16
#states (22279)
15056 components
No issues
Loading code/leader.hco```

Duration: 0.0014025999999999206

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

Duration: 0.001417399999999902

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hoare.hco```

Duration: 0.001605099999999915

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

Duration: 0.0013371999999999273

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWfair.hco```

Duration: 0.0012786000000000186

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

Duration: 0.0014813000000000187

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/register.hco```

Duration: 0.0017527999999999988

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

Duration: 0.001590999999999898

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/lltest.hco
T0: __init__() [0-7,371-373,1041-1047,1331-1334] { alloc: { "next": 0, "pool": () }, bag: (), linkedlist: (), list: (), synch: () }
Load: unknown address ?LinkedList[()]```

Duration: 0.0017319000000000084

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

Duration: 0.0015162000000000786

### Current Output

```
nworkers = 16
#states (50808)
50808 components
No issues
Loading code/paxos.hco```

Duration: 0.0015735000000000054

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

Duration: 0.0016846999999999834

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWlock.hco
T0: __init__() [0-5,369-371,1107-1110] { bag: (), list: (), synch: () }
Load: unknown address ?Lock[()]```

Duration: 0.0013897000000000492

---
##  code/mesa.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Parse error in var statement. Got ('0', 'code/mesa.hny', 5, 13), but expected '=' ErrorToken(line=5, message="Parse error in var statement. Got ('0', 'code/mesa.hny', 5, 13), but expected '='", column=13, lexeme='0', filename='code/mesa.hny', is_eof_error=False)```

Duration: 0.0010044000000000164

### Current Output

```
Line 5:12 at code/mesa.hny, missing '=' at '0'```

Duration: 0.0010369999999999546

---
##  code/RWqtest.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWqtest.hco
T0: __init__() [0-7,371-373,1253-1256] { RWqueue: (), bag: (), list: (), synch: () }
Load: unknown address ?RWqueue["Semaphore"][1]```

Duration: 0.0013885000000000147

### Current Output

```
```

Duration: 0.0011449000000000042

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

Duration: 0.0014144999999999852

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/BBsema.hco
T0: __init__() [0-5,369-371,1109-1120,1112-1120,1112-1114,1121-1130] { b_in: 1, b_out: 1, bag: (), buf: { 1: (), 2: () }, list: (), synch: () }
Load: unknown address ?Semaphore[1]```

Duration: 0.0013913999999999316

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

Duration: 0.0012982000000000271

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queue.hco```

Duration: 0.0015956000000000303

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

Duration: 0.0015340000000000353

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/barrier.hco```

Duration: 0.0015070999999999835

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

Duration: 0.0016884999999999817

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/ticket.hco```

Duration: 0.001428600000000002

---
##  code/PetersonPrint.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
```

Duration: 0.00115070000000006

### Current Output

```
```

Duration: 0.0011497000000000313

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

Duration: 0.0017966999999999844

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/atomicinc.hco```

Duration: 0.001376299999999997

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

Duration: 0.0012179999999999414

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/nbqueue.hco```

Duration: 0.0013792999999999722

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

Duration: 0.0012836000000000514

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/dinersfix.hco
T0: __init__() [0,1] { }
Load: unknown variable left```

Duration: 0.0014775999999999678

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

Duration: 0.0012609999999999566

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack2.hco```

Duration: 0.001264299999999996

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

Duration: 0.0013659999999999783

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/gpu.hco```

Duration: 0.0012311999999999879

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

Duration: 0.0013085000000000457

### Current Output

```
nworkers = 16
#states (13)
13 components
No issues
Loading code/triangle.hco```

Duration: 0.001572299999999971

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

Duration: 0.0017165000000000097

### Current Output

```
nworkers = 16
#states (3614)
3614 components
No issues
Loading code/barrier1.hco```

Duration: 0.0014324000000000003

---
##  code/spinlockInv.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
nworkers = 16
#states (473)
148 components
No issues
Loading code/spinlockInv.hco```

Duration: 0.0014657999999999616

### Current Output

```
```

Duration: 0.0010564000000000684

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

Duration: 0.0016535999999999218

### Current Output

```
nworkers = 16
#states (633)
633 components
No issues
Loading code/bosco2.hco```

Duration: 0.0022363999999999162

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

Duration: 0.001607500000000095

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/paxos2.hco```

Duration: 0.0018209000000000142

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

Duration: 0.0016359999999999708

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/bqueue.hco```

Duration: 0.0015665000000000262

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

Duration: 0.0016943000000000374

### Current Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/hello6.hco```

Duration: 0.001429899999999984

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

Duration: 0.0012254000000000431

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack1.hco```

Duration: 0.0014664999999999262

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

Duration: 0.0013497000000000092

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hello5.hco```

Duration: 0.001270700000000069

---
##  code/abd.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/abd.hco```

Duration: 0.001389100000000032

### Current Output

```
Line 8:13 at code/abd.hny, extraneous input 'atomically' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING, INDENT}```

Duration: 0.0011006000000000071

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

Duration: 0.0013425000000000242

### Current Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/hello8.hco```

Duration: 0.001902699999999924

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

Duration: 0.0013398999999999495

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack4.hco```

Duration: 0.0018169999999999575

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

Duration: 0.0011945999999999346

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/BBhoare.hco```

Duration: 0.0012364999999999737

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

Duration: 0.00119950000000002

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWcheat.hco```

Duration: 0.0012501000000000317

---
##  code/stacktest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Can't import module stack from ['code/stacktest.hny'] ErrorToken(line=1, message="Can't import module stack from ['code/stacktest.hny']", column=6, lexeme='stack', filename='code/stacktest.hny', is_eof_error=False)```

Duration: 0.0009599999999999609

### Current Output

```
Line 1:6 at code/stacktest.hny, Can't import module stack from ['code/stacktest.hny']```

Duration: 0.0015337999999999186

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

Duration: 0.0011672000000000349

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queueMS.hco```

Duration: 0.0012919000000000125

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

Duration: 0.0011513999999999136

### Current Output

```
nworkers = 16
#states (148)
148 components
No issues
Loading code/abdtest.hco```

Duration: 0.001482699999999948

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

Duration: 0.001073099999999938

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/locksusp.hco```

Duration: 0.0012497000000000202

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

Duration: 0.0012691999999999704

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWbusychk.hco
T0: __init__() [0-3,145-156,147-156,147-156,147-149,157-169,160-169,160-169,160-162,170-174] { RW: () }
Load: unknown address ?acquire_wlock[()]```

Duration: 0.001270199999999999

---
##  code/2pc1.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot operate on constant ('balance', 'code/2pc1.hny', 16, 21) ErrorToken(line=16, message="Cannot operate on constant ('balance', 'code/2pc1.hny', 16, 21)", column=29, lexeme='-=', filename='code/2pc1.hny', is_eof_error=False)```

Duration: 0.0009727000000000485

### Current Output

```
Line 16:29 at code/2pc1.hny, Cannot operate on constant ('balance', 'code/2pc1.hny', 16, 21)```

Duration: 0.0010099999999999554

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

Duration: 0.0013306000000000706

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

Duration: 0.0013347999999999693

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

Duration: 0.0014100000000000223

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/linkedlist.hco```

Duration: 0.0014446999999999655

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

Duration: 0.0013153000000000192

### Current Output

```
nworkers = 16
#states (6272)
6272 components
No issues
Loading code/barriertest2.hco```

Duration: 0.001384300000000005

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

Duration: 0.0014720999999999762

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/oo.hco```

Duration: 0.0012828999999999757

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

Duration: 0.0014655000000000085

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuefix.hco```

Duration: 0.0017215000000000424

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

Duration: 0.0017513999999999585

### Current Output

```
nworkers = 16
#states (3)
3 components
No issues
Loading code/hello3.hco```

Duration: 0.001419500000000018

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

Duration: 0.0013998999999998984

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queueseq.hco```

Duration: 0.0013507999999999853

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

Duration: 0.0014305000000000012

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hello1.hco```

Duration: 0.0017445000000000377

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

Duration: 0.001494200000000001

### Current Output

```
nworkers = 16
#states (4540)
4540 components
No issues
Loading code/consensus.hco```

Duration: 0.0016720000000000068

---
##  test/pascal.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
constant cannot be an lvalue: ('k', 'test/pascal.hny', 13, 13) ErrorToken(line=9, message="constant cannot be an lvalue: ('k', 'test/pascal.hny', 13, 13)", column=18, lexeme='k', filename='test/pascal.hny', is_eof_error=False)```

Duration: 0.0011039000000000465

### Current Output

```
Line 9:18 at test/pascal.hny, constant cannot be an lvalue: ('k', 'test/pascal.hny', 13, 13)```

Duration: 0.0011244999999999727

---
##  test/byzbosco.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('atomic', 'test/byzbosco.hny', 11, 5), but expected expression ErrorToken(line=11, message="Parse error in statement. Got ('atomic', 'test/byzbosco.hny', 11, 5), but expected expression", column=5, lexeme='atomic', filename='test/byzbosco.hny', is_eof_error=False)```

Duration: 0.0010284000000000404

### Current Output

```
Line 21:46 at test/byzbosco.hny, mismatched input ':' expecting {NL, ';'}

Line 24:25 at test/byzbosco.hny, no viable alternative at input 'count'

Line 25:16 at test/byzbosco.hny, no viable alternative at input ']'

Line 27:20 at test/byzbosco.hny, no viable alternative at input '1'

Line 34:46 at test/byzbosco.hny, mismatched input ':' expecting {NL, ';'}```

Duration: 0.0012372999999999967

---
##  test/PCcv.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in n-ary operation. Got (';', 'test/PCcv.hny', 32, 21), but expected binary operation or 'if' ErrorToken(line=32, message="Parse error in n-ary operation. Got (';', 'test/PCcv.hny', 32, 21), but expected binary operation or 'if'", column=21, lexeme=';', filename='test/PCcv.hny', is_eof_error=False)```

Duration: 0.000988800000000012

### Current Output

```
Line 33:8 at test/PCcv.hny, mismatched input '@' expecting DEDENT

Line 35:8 at test/PCcv.hny, mismatched input '@' expecting DEDENT

Line 35:29 at test/PCcv.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 36:5 at test/PCcv.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 40:8 at test/PCcv.hny, extraneous input '@' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 42:8 at test/PCcv.hny, mismatched input '@' expecting DEDENT

Line 43:5 at test/PCcv.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 45:6 at test/PCcv.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 45:24 at test/PCcv.hny, no viable alternative at input '..'

Line 53:16 at test/PCcv.hny, no viable alternative at input ','

Line 54:16 at test/PCcv.hny, no viable alternative at input ','

Line 55:16 at test/PCcv.hny, no viable alternative at input ','

Line 56:16 at test/PCcv.hny, no viable alternative at input ','```

Duration: 0.0012075999999999754

---
##  test/msort.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in n-ary operation. Got ('=', 'test/msort.hny', 7, 18), but expected binary operation or 'if' ErrorToken(line=7, message="Parse error in n-ary operation. Got ('=', 'test/msort.hny', 7, 18), but expected binary operation or 'if'", column=18, lexeme='=', filename='test/msort.hny', is_eof_error=False)```

Duration: 0.0009847000000000605

### Current Output

```
Line 7:17 at test/msort.hny, no viable alternative at input '='

Line 7:55 at test/msort.hny, no viable alternative at input ':'

Line 33:14 at test/msort.hny, no viable alternative at input '..'

Line 33:28 at test/msort.hny, no viable alternative at input ':'

Line 40:16 at test/msort.hny, no viable alternative at input '..'

Line 41:35 at test/msort.hny, no viable alternative at input '[choose(values)foriin1..'

Line 41:35 at test/msort.hny, no viable alternative at input '..'```

Duration: 0.0011860000000000204

---
##  test/bosco.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('atomic', 'test/bosco.hny', 14, 5), but expected expression ErrorToken(line=14, message="Parse error in statement. Got ('atomic', 'test/bosco.hny', 14, 5), but expected expression", column=5, lexeme='atomic', filename='test/bosco.hny', is_eof_error=False)```

Duration: 0.001007200000000097

### Current Output

```
Line 30:38 at test/bosco.hny, Cannot operate on constant ('received', 'test/bosco.hny', 30, 29)```

Duration: 0.001089099999999954

---
##  test/qsort.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
```

Duration: 0.0011246000000000311

### Current Output

```
Line 8:12 at test/qsort.hny, extraneous input '^' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 9:8 at test/qsort.hny, extraneous input '^' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 9:13 at test/qsort.hny, extraneous input '^' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 10:8 at test/qsort.hny, mismatched input '^' expecting DEDENT

Line 11:5 at test/qsort.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 15:15 at test/qsort.hny, no viable alternative at input '..'

Line 15:25 at test/qsort.hny, no viable alternative at input ':'

Line 17:17 at test/qsort.hny, no viable alternative at input 'swap(&'

Line 17:29 at test/qsort.hny, mismatched input '&' expecting {NL, ';'}

Line 17:34 at test/qsort.hny, no viable alternative at input ')'

Line 21:9 at test/qsort.hny, no viable alternative at input 'swap(&'

Line 21:21 at test/qsort.hny, mismatched input '&' expecting {NL, ';'}

Line 21:27 at test/qsort.hny, no viable alternative at input ')'

Line 24:26 at test/qsort.hny, no viable alternative at input '='

Line 24:63 at test/qsort.hny, no viable alternative at input ':'

Line 44:17 at test/qsort.hny, no viable alternative at input 'lock(&'

Line 47:23 at test/qsort.hny, no viable alternative at input 'unlock(&'

Line 51:27 at test/qsort.hny, no viable alternative at input 'unlock(&'

Line 57:6 at test/qsort.hny, no viable alternative at input 'V(&'

Line 61:14 at test/qsort.hny, no viable alternative at input '..'

Line 61:28 at test/qsort.hny, no viable alternative at input ':'

Line 68:14 at test/qsort.hny, no viable alternative at input '..'

Line 69:10 at test/qsort.hny, no viable alternative at input 'P(&'

Line 75:16 at test/qsort.hny, no viable alternative at input '..'

Line 76:31 at test/qsort.hny, no viable alternative at input '[choose(values)foriin1..'

Line 76:31 at test/qsort.hny, no viable alternative at input '..'

Line 80:10 at test/qsort.hny, no viable alternative at input '..'```

Duration: 0.0015857999999999706

---
##  test/bound.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Cannot assign to constant ('blocked', 'test/bound.hny', 13, 17) ErrorToken(line=13, message="Cannot assign to constant ('blocked', 'test/bound.hny', 13, 17)", column=25, lexeme='=', filename='test/bound.hny', is_eof_error=False)```

Duration: 0.0010590999999999795

### Current Output

```
Line 4:13 at test/bound.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}```

Duration: 0.0017334999999999434

---
##  test/barriertest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot assign to constant ('x', 'test/barriertest.hny', 43, 17) ErrorToken(line=43, message="Cannot assign to constant ('x', 'test/barriertest.hny', 43, 17)", column=19, lexeme='=', filename='test/barriertest.hny', is_eof_error=False)```

Duration: 0.0009870999999999075

### Current Output

```
Line 43:17 at test/barriertest.hny, Cannot assign to constant ('x', 'test/barriertest.hny', 43, 17)```

Duration: 0.001096000000000097

---
##  test/Bakery.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/Bakery.hny', 23, 9), but expected expression ErrorToken(line=23, message="Parse error in statement. Got ('@', 'test/Bakery.hny', 23, 9), but expected expression", column=9, lexeme='@', filename='test/Bakery.hny', is_eof_error=False)```

Duration: 0.0010101000000000138

### Current Output

```
Line 23:8 at test/Bakery.hny, mismatched input '@' expecting DEDENT

Line 25:0 at test/Bakery.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}```

Duration: 0.0012385999999999786

---
##  test/PCbinsem.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading test/PCbinsem.hco
T0: __init__() [0-5,369-371,1177-1188,1181-1188,1181-1183,1189-1191] { bag: (), list: (), synch: () }
Load: unknown address ?dict[{ 0 }]```

Duration: 0.0013099999999999223

### Current Output

```
Line 43:6 at test/PCbinsem.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}```

Duration: 0.0015963999999999423

---
##  test/anonbosco2.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('atomic', 'test/anonbosco2.hny', 11, 5), but expected expression ErrorToken(line=11, message="Parse error in statement. Got ('atomic', 'test/anonbosco2.hny', 11, 5), but expected expression", column=5, lexeme='atomic', filename='test/anonbosco2.hny', is_eof_error=False)```

Duration: 0.000957100000000044

### Current Output

```
Line 21:46 at test/anonbosco2.hny, mismatched input ':' expecting {NL, ';'}

Line 24:25 at test/anonbosco2.hny, no viable alternative at input 'count'

Line 25:16 at test/anonbosco2.hny, no viable alternative at input ']'

Line 27:20 at test/anonbosco2.hny, no viable alternative at input '1'```

Duration: 0.0015013000000000387

---
##  test/anonbosco.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('atomic', 'test/anonbosco.hny', 11, 5), but expected expression ErrorToken(line=11, message="Parse error in statement. Got ('atomic', 'test/anonbosco.hny', 11, 5), but expected expression", column=5, lexeme='atomic', filename='test/anonbosco.hny', is_eof_error=False)```

Duration: 0.0010913000000000173

### Current Output

```
Line 19:17 at test/anonbosco.hny, Cannot assign to constant ('msgs', 'test/anonbosco.hny', 19, 17)```

Duration: 0.0015912999999999622

---
##  test/poolsbs.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading test/poolsbs.hco```

Duration: 0.0012096999999999802

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading test/poolsbs.hco```

Duration: 0.001461399999999946

---
##  test/extqueue.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Cannot assign to constant ('node', 'test/extqueue.hny', 39, 13) ErrorToken(line=39, message="Cannot assign to constant ('node', 'test/extqueue.hny', 39, 13)", column=18, lexeme='=', filename='test/extqueue.hny', is_eof_error=False)```

Duration: 0.0010775000000000645

### Current Output

```
Line 4:13 at test/extqueue.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 7:21 at test/extqueue.hny, no viable alternative at input '('

Line 7:52 at test/extqueue.hny, no viable alternative at input ')'

Line 16:5 at test/extqueue.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}```

Duration: 0.0012166000000000121

---
##  test/busywait.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in n-ary operation. Got ('-', 'test/busywait.hny', 4, 33), but expected one of {':'} ErrorToken(line=4, message="Parse error in n-ary operation. Got ('-', 'test/busywait.hny', 4, 33), but expected one of {':'}", column=33, lexeme='-', filename='test/busywait.hny', is_eof_error=False)```

Duration: 0.0009756999999999127

### Current Output

```
Line 7:20 at test/busywait.hny, no viable alternative at input ':'

Line 8:0 at test/busywait.hny, extraneous input '@' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 9:8 at test/busywait.hny, no viable alternative at input ':'```

Duration: 0.0011693999999999871

---
##  test/bound_chk2.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Can't import module boundsem from ['test/bound_chk2.hny'] ErrorToken(line=1, message="Can't import module boundsem from ['test/bound_chk2.hny']", column=8, lexeme='boundsem', filename='test/bound_chk2.hny', is_eof_error=False)```

Duration: 0.0010941999999999341

### Current Output

```
Line 1:8 at test/bound_chk2.hny, Can't import module boundsem from ['test/bound_chk2.hny']```

Duration: 0.001133099999999998

---
##  test/RWhoare.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/RWhoare.hny', 60, 13), but expected expression ErrorToken(line=60, message="Parse error in statement. Got ('@', 'test/RWhoare.hny', 60, 13), but expected expression", column=13, lexeme='@', filename='test/RWhoare.hny', is_eof_error=False)```

Duration: 0.0009595999999999494

### Current Output

```
Line 60:12 at test/RWhoare.hny, mismatched input '@' expecting DEDENT

Line 60:40 at test/RWhoare.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 62:8 at test/RWhoare.hny, mismatched input 'else' expecting DEDENT

Line 64:12 at test/RWhoare.hny, mismatched input '@' expecting DEDENT

Line 64:41 at test/RWhoare.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 65:41 at test/RWhoare.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 66:19 at test/RWhoare.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 67:33 at test/RWhoare.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 68:9 at test/RWhoare.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 69:5 at test/RWhoare.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 71:10 at test/RWhoare.hny, no viable alternative at input '..'```

Duration: 0.0012173000000000878

---
##  test/Dekker.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/Dekker.hny', 21, 9), but expected expression ErrorToken(line=21, message="Parse error in statement. Got ('@', 'test/Dekker.hny', 21, 9), but expected expression", column=9, lexeme='@', filename='test/Dekker.hny', is_eof_error=False)```

Duration: 0.0009485999999999661

### Current Output

```
Line 21:8 at test/Dekker.hny, mismatched input '@' expecting DEDENT

Line 23:0 at test/Dekker.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}```

Duration: 0.0011372999999998967

---
##  test/PetersonBroken.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/PetersonBroken.hny', 14, 9), but expected expression ErrorToken(line=14, message="Parse error in statement. Got ('@', 'test/PetersonBroken.hny', 14, 9), but expected expression", column=9, lexeme='@', filename='test/PetersonBroken.hny', is_eof_error=False)```

Duration: 0.0010000000000000009

### Current Output

```
Line 14:8 at test/PetersonBroken.hny, mismatched input '@' expecting DEDENT

Line 17:20 at test/PetersonBroken.hny, mismatched input '=' expecting {NL, ';'}

Line 18:0 at test/PetersonBroken.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}```

Duration: 0.0010002000000000066

---
##  test/PetersonBadProof.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/PetersonBadProof.hny', 8, 9), but expected expression ErrorToken(line=8, message="Parse error in statement. Got ('@', 'test/PetersonBadProof.hny', 8, 9), but expected expression", column=9, lexeme='@', filename='test/PetersonBadProof.hny', is_eof_error=False)```

Duration: 0.000977099999999953

### Current Output

```
Line 8:8 at test/PetersonBadProof.hny, mismatched input '@' expecting DEDENT

Line 10:5 at test/PetersonBadProof.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 14:16 at test/PetersonBadProof.hny, no viable alternative at input ','

Line 15:16 at test/PetersonBadProof.hny, no viable alternative at input ','```

Duration: 0.0010285999999999351

---
##  test/PetersonOO.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/PetersonOO.hny', 18, 9), but expected expression ErrorToken(line=18, message="Parse error in statement. Got ('@', 'test/PetersonOO.hny', 18, 9), but expected expression", column=9, lexeme='@', filename='test/PetersonOO.hny', is_eof_error=False)```

Duration: 0.001040299999999994

### Current Output

```
Line 10:13 at test/PetersonOO.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 18:8 at test/PetersonOO.hny, mismatched input '@' expecting DEDENT

Line 18:34 at test/PetersonOO.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 20:5 at test/PetersonOO.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 23:26 at test/PetersonOO.hny, no viable alternative at input ','

Line 24:26 at test/PetersonOO.hny, no viable alternative at input ','```

Duration: 0.0011740999999999557

---
##  test/bound_chk1.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Can't import module boundsem from ['test/bound_chk1.hny'] ErrorToken(line=1, message="Can't import module boundsem from ['test/bound_chk1.hny']", column=8, lexeme='boundsem', filename='test/bound_chk1.hny', is_eof_error=False)```

Duration: 0.0009582000000000201

### Current Output

```
Line 1:8 at test/bound_chk1.hny, Can't import module boundsem from ['test/bound_chk1.hny']```

Duration: 0.0010997000000000368

---
##  test/RWbadlock.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/RWbadlock.hny', 8, 13), but expected expression ErrorToken(line=8, message="Parse error in statement. Got ('@', 'test/RWbadlock.hny', 8, 13), but expected expression", column=13, lexeme='@', filename='test/RWbadlock.hny', is_eof_error=False)```

Duration: 0.0011785000000000823

### Current Output

```
Line 8:12 at test/RWbadlock.hny, mismatched input '@' expecting DEDENT

Line 8:40 at test/RWbadlock.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 12:8 at test/RWbadlock.hny, extraneous input 'else' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 15:12 at test/RWbadlock.hny, mismatched input '@' expecting DEDENT

Line 15:41 at test/RWbadlock.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 16:39 at test/RWbadlock.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 18:0 at test/RWbadlock.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 19:34 at test/RWbadlock.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 20:9 at test/RWbadlock.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 21:5 at test/RWbadlock.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 24:10 at test/RWbadlock.hny, no viable alternative at input '..'```

Duration: 0.0013745000000000562

---
##  test/barber.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading test/barber.hco
T0: __init__() [0-5,369-371,1039-1046] { bag: (), done: {}, list: (), seated: {}, synch: () }
Load: unknown address ?Lock[()]```

Duration: 0.0012851999999999864

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading test/barber.hco
T0: __init__() [0-5,369-371,1039-1046] { bag: (), done: {}, list: (), seated: {}, synch: () }
Load: unknown address ?Lock[()]```

Duration: 0.001521100000000053

---
##  test/paxos.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('atomic', 'test/paxos.hny', 12, 5), but expected expression ErrorToken(line=12, message="Parse error in statement. Got ('atomic', 'test/paxos.hny', 12, 5), but expected expression", column=5, lexeme='atomic', filename='test/paxos.hny', is_eof_error=False)```

Duration: 0.0009796000000000804

### Current Output

```
Line 11:20 at test/paxos.hny, constant cannot be an lvalue: ('proposal', 'test/paxos.hny', 26, 40)```

Duration: 0.0009962000000000026

---
##  test/extqtest.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Cannot assign to constant ('node', 'test/extqueue.hny', 39, 13) ErrorToken(line=39, message="Cannot assign to constant ('node', 'test/extqueue.hny', 39, 13)", column=18, lexeme='=', filename='test/extqueue.hny', is_eof_error=False)```

Duration: 0.000965099999999941

### Current Output

```
Line 4:13 at test/extqueue.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 7:21 at test/extqueue.hny, no viable alternative at input '('

Line 7:52 at test/extqueue.hny, no viable alternative at input ')'

Line 16:5 at test/extqueue.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}```

Duration: 0.0017754000000000936

---
##  test/InfLoop.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/InfLoop.hny', 5, 5), but expected expression ErrorToken(line=5, message="Parse error in statement. Got ('@', 'test/InfLoop.hny', 5, 5), but expected expression", column=5, lexeme='@', filename='test/InfLoop.hny', is_eof_error=False)```

Duration: 0.0007812999999999848

### Current Output

```
Line 5:4 at test/InfLoop.hny, mismatched input '@' expecting DEDENT

Line 6:0 at test/InfLoop.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}```

Duration: 0.001418699999999995

---
##  test/queue.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in n-ary operation. Got ('..', 'test/queue.hny', 30, 54), but expected binary operation or 'if' ErrorToken(line=30, message="Parse error in n-ary operation. Got ('..', 'test/queue.hny', 30, 54), but expected binary operation or 'if'", column=54, lexeme='..', filename='test/queue.hny', is_eof_error=False)```

Duration: 0.0010398999999999825

### Current Output

```
Line 30:11 at test/queue.hny, no viable alternative at input '[dict'

Line 30:53 at test/queue.hny, no viable alternative at input '..'

Line 30:67 at test/queue.hny, no viable alternative at input ']'

Line 32:10 at test/queue.hny, no viable alternative at input '..'

Line 32:23 at test/queue.hny, no viable alternative at input ':'```

Duration: 0.0012735999999999859

---
##  test/pooltest.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Can't import module pool from ['test/pooltest.hny'] ErrorToken(line=1, message="Can't import module pool from ['test/pooltest.hny']", column=8, lexeme='pool', filename='test/pooltest.hny', is_eof_error=False)```

Duration: 0.0009721999999999786

### Current Output

```
Line 1:8 at test/pooltest.hny, Can't import module pool from ['test/pooltest.hny']```

Duration: 0.001085900000000084

---
##  test/Sema.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/Sema.hny', 8, 9), but expected expression ErrorToken(line=8, message="Parse error in statement. Got ('@', 'test/Sema.hny', 8, 9), but expected expression", column=9, lexeme='@', filename='test/Sema.hny', is_eof_error=False)```

Duration: 0.0009972999999999788

### Current Output

```
Line 8:8 at test/Sema.hny, mismatched input '@' expecting DEDENT

Line 8:34 at test/Sema.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 10:5 at test/Sema.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 13:15 at test/Sema.hny, no viable alternative at input ','

Line 14:15 at test/Sema.hny, no viable alternative at input ','

Line 15:15 at test/Sema.hny, no viable alternative at input ','

Line 16:15 at test/Sema.hny, no viable alternative at input ','```

Duration: 0.0011322000000000276

---
##  test/Szymanski.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/Szymanski.hny', 24, 9), but expected expression ErrorToken(line=24, message="Parse error in statement. Got ('@', 'test/Szymanski.hny', 24, 9), but expected expression", column=9, lexeme='@', filename='test/Szymanski.hny', is_eof_error=False)```

Duration: 0.0009968999999999673

### Current Output

```
Line 24:8 at test/Szymanski.hny, mismatched input '@' expecting DEDENT

Line 26:0 at test/Szymanski.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}```

Duration: 0.001857400000000009

---
##  test/lst.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in n-ary operation. Got (')', 'test/lst.hny', 6, 13), but expected binary operation or 'if' ErrorToken(line=6, message="Parse error in n-ary operation. Got (')', 'test/lst.hny', 6, 13), but expected binary operation or 'if'", column=13, lexeme=')', filename='test/lst.hny', is_eof_error=False)```

Duration: 0.0011670999999999765

### Current Output

```
Line 6:5 at test/lst.hny, no viable alternative at input '(^'

Line 6:21 at test/lst.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 7:5 at test/lst.hny, no viable alternative at input '(^'

Line 13:28 at test/lst.hny, no viable alternative at input '='

Line 13:44 at test/lst.hny, no viable alternative at input ':'

Line 14:33 at test/lst.hny, no viable alternative at input ';'

Line 15:13 at test/lst.hny, no viable alternative at input '(&('

Line 15:32 at test/lst.hny, no viable alternative at input ';'

Line 16:15 at test/lst.hny, extraneous input '^' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', ')', STRING}

Line 17:19 at test/lst.hny, no viable alternative at input '(&('

Line 17:39 at test/lst.hny, no viable alternative at input ';'

Line 19:21 at test/lst.hny, no viable alternative at input '^before'

Line 20:17 at test/lst.hny, no viable alternative at input '(&('

Line 20:36 at test/lst.hny, no viable alternative at input ';'

Line 23:5 at test/lst.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 26:37 at test/lst.hny, no viable alternative at input 'x'

Line 26:57 at test/lst.hny, no viable alternative at input 'indent'

Line 27:12 at test/lst.hny, extraneous input '^' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', ')', STRING}

Line 28:13 at test/lst.hny, no viable alternative at input '^before'

Line 30:15 at test/lst.hny, no viable alternative at input '(&('

Line 30:35 at test/lst.hny, no viable alternative at input ';'

Line 31:15 at test/lst.hny, no viable alternative at input '(&('

Line 31:34 at test/lst.hny, no viable alternative at input ';'

Line 35:37 at test/lst.hny, no viable alternative at input 'x'

Line 35:57 at test/lst.hny, no viable alternative at input 'indent'

Line 36:12 at test/lst.hny, extraneous input '^' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', ')', STRING}

Line 37:13 at test/lst.hny, no viable alternative at input '^before'

Line 37:30 at test/lst.hny, no viable alternative at input '^after'

Line 38:19 at test/lst.hny, no viable alternative at input '(&('

Line 38:38 at test/lst.hny, no viable alternative at input ';'

Line 41:19 at test/lst.hny, no viable alternative at input '(&('

Line 41:38 at test/lst.hny, no viable alternative at input ';'

Line 43:15 at test/lst.hny, no viable alternative at input '(&('

Line 43:35 at test/lst.hny, no viable alternative at input ';'

Line 49:15 at test/lst.hny, extraneous input '^' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', ')', STRING}

Line 50:17 at test/lst.hny, no viable alternative at input '^n'

Line 52:18 at test/lst.hny, no viable alternative at input '^n'```

Duration: 0.0015335000000000765

---
##  test/mutex.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in n-ary operation. Got (':', 'test/mutex.hny', 1, 16), but expected binary operation or 'if' ErrorToken(line=1, message="Parse error in n-ary operation. Got (':', 'test/mutex.hny', 1, 16), but expected binary operation or 'if'", column=16, lexeme=':', filename='test/mutex.hny', is_eof_error=False)```

Duration: 0.0010289999999999466

### Current Output

```
Line 1:15 at test/mutex.hny, no viable alternative at input ':'

Line 2:27 at test/mutex.hny, no viable alternative at input 'atLabel'

Line 2:60 at test/mutex.hny, no viable alternative at input 'for'

Line 3:24 at test/mutex.hny, no viable alternative at input '='

Line 4:35 at test/mutex.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 11:31 at test/mutex.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 12:5 at test/mutex.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 14:19 at test/mutex.hny, no viable alternative at input ':'

Line 17:21 at test/mutex.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 18:44 at test/mutex.hny, mismatched input ':' expecting {NL, ';'}

Line 19:35 at test/mutex.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 24:5 at test/mutex.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}```

Duration: 0.001437899999999992

---
##  test/NotSaveSym.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/NotSaveSym.hny', 7, 9), but expected expression ErrorToken(line=7, message="Parse error in statement. Got ('@', 'test/NotSaveSym.hny', 7, 9), but expected expression", column=9, lexeme='@', filename='test/NotSaveSym.hny', is_eof_error=False)```

Duration: 0.0010537999999999936

### Current Output

```
Line 7:8 at test/NotSaveSym.hny, mismatched input '@' expecting DEDENT

Line 7:34 at test/NotSaveSym.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 9:5 at test/NotSaveSym.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 12:16 at test/NotSaveSym.hny, no viable alternative at input ','

Line 13:16 at test/NotSaveSym.hny, no viable alternative at input ','```

Duration: 0.0013733000000000217

---
##  test/teahouse.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (27155)
27155 components
No issues
Loading test/teahouse.hco```

Duration: 0.0011564000000000574

### Current Output

```
nworkers = 16
#states (27155)
27155 components
No issues
Loading test/teahouse.hco```

Duration: 0.0015458000000000416

---
##  test/Turn.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/Turn.hny', 3, 9), but expected expression ErrorToken(line=3, message="Parse error in statement. Got ('@', 'test/Turn.hny', 3, 9), but expected expression", column=9, lexeme='@', filename='test/Turn.hny', is_eof_error=False)```

Duration: 0.00097629999999993

### Current Output

```
Line 3:8 at test/Turn.hny, extraneous input '@' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 9:8 at test/Turn.hny, mismatched input '@' expecting DEDENT

Line 9:34 at test/Turn.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 13:5 at test/Turn.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 16:10 at test/Turn.hny, no viable alternative at input ','

Line 17:10 at test/Turn.hny, no viable alternative at input ','```

Duration: 0.0009743999999999309

---
##  test/test.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading test/test.hco
T0: __init__() [0,1,8-12,2-7,13-15,2-7,16-18,2-7,19-30,2-7,31-33,2-7,34-36,2-7,37-39,2-7,40-51,2-7,52-54,2-7,55-66,2-7,67-78,2-7,79-89,2-7,90-92,2-7,93-95,2-7,96-107,2-7,108-110,2-7,111-113,2-7,114-125,2-7,126-128,2-7,129-131,2-7,132-143,2-7,144-146,2-7,147-158,2-7,159-161,2-7,162-173,2-7,174-176,2-7,177-186,2-7,187-189,2-7,190-200,2-7,201-203,2-7,204-214,2-7,215-225,2-7,226-236,2-7,237-247,2-7,248-258,2-7,259-269,2-7,270-280,2-7,281-283,2-7,284-294,2-7,295-297,2-7,298] { }
**: overflow (model too large)```

Duration: 0.0011537000000000353

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading test/test.hco
T0: __init__() [0,1,8-12,2-7,13-15,2-7,16-18,2-7,19-30,2-7,31-33,2-7,34-36,2-7,37-39,2-7,40-51,2-7,52-54,2-7,55-66,2-7,67-78,2-7,79-89,2-7,90-92,2-7,93-95,2-7,96-107,2-7,108-110,2-7,111-113,2-7,114-125,2-7,126-128,2-7,129-131,2-7,132-143,2-7,144-146,2-7,147-158,2-7,159-161,2-7,162-173,2-7,174-176,2-7,177-186,2-7,187-189,2-7,190-200,2-7,201-203,2-7,204-214,2-7,215-225,2-7,226-236,2-7,237-247,2-7,248-258,2-7,259-269,2-7,270-280,2-7,281-283,2-7,284-294,2-7,295-297,2-7,298] { }
**: overflow (model too large)```

Duration: 0.0018816999999999862

---
##  test/NotLiveSym.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/NotLiveSym.hny', 7, 9), but expected expression ErrorToken(line=7, message="Parse error in statement. Got ('@', 'test/NotLiveSym.hny', 7, 9), but expected expression", column=9, lexeme='@', filename='test/NotLiveSym.hny', is_eof_error=False)```

Duration: 0.0009751999999999539

### Current Output

```
Line 7:8 at test/NotLiveSym.hny, mismatched input '@' expecting DEDENT

Line 7:34 at test/NotLiveSym.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 9:5 at test/NotLiveSym.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 11:8 at test/NotLiveSym.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 12:16 at test/NotLiveSym.hny, no viable alternative at input ','

Line 13:16 at test/NotLiveSym.hny, no viable alternative at input ','```

Duration: 0.0010327999999999449

---
##  test/Lock.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/Lock.hny', 6, 9), but expected expression ErrorToken(line=6, message="Parse error in statement. Got ('@', 'test/Lock.hny', 6, 9), but expected expression", column=9, lexeme='@', filename='test/Lock.hny', is_eof_error=False)```

Duration: 0.0010366000000000541

### Current Output

```
Line 6:8 at test/Lock.hny, mismatched input '@' expecting DEDENT

Line 6:34 at test/Lock.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 8:5 at test/Lock.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 11:10 at test/Lock.hny, no viable alternative at input '..'```

Duration: 0.0012422999999999185

---
##  test/anonbosco3.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('atomic', 'test/anonbosco3.hny', 13, 5), but expected expression ErrorToken(line=13, message="Parse error in statement. Got ('atomic', 'test/anonbosco3.hny', 13, 5), but expected expression", column=5, lexeme='atomic', filename='test/anonbosco3.hny', is_eof_error=False)```

Duration: 0.0011196999999999457

### Current Output

```
Line 20:17 at test/anonbosco3.hny, Cannot assign to constant ('receiving', 'test/anonbosco3.hny', 20, 17)```

Duration: 0.0011200999999999572

---
##  test/ctriangle.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (13)
13 components
No issues
Loading test/ctriangle.hco```

Duration: 0.0012052000000000174

### Current Output

```
nworkers = 16
#states (13)
13 components
No issues
Loading test/ctriangle.hco```

Duration: 0.0011881999999999726

---
##  test/EM.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('@', 'test/EM.hny', 48, 9), but expected expression ErrorToken(line=48, message="Parse error in statement. Got ('@', 'test/EM.hny', 48, 9), but expected expression", column=9, lexeme='@', filename='test/EM.hny', is_eof_error=False)```

Duration: 0.0014135999999999038

### Current Output

```
Line 48:8 at test/EM.hny, mismatched input '@' expecting DEDENT

Line 48:34 at test/EM.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 50:5 at test/EM.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}```

Duration: 0.0011322000000000276

---
##  test/sorttest.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in n-ary operation. Got ('..', 'test/sorttest.hny', 7, 15), but expected binary operation or 'if' ErrorToken(line=7, message="Parse error in n-ary operation. Got ('..', 'test/sorttest.hny', 7, 15), but expected binary operation or 'if'", column=15, lexeme='..', filename='test/sorttest.hny', is_eof_error=False)```

Duration: 0.0010204000000000324

### Current Output

```
Line 7:14 at test/sorttest.hny, no viable alternative at input '..'

Line 7:28 at test/sorttest.hny, no viable alternative at input ':'

Line 13:16 at test/sorttest.hny, no viable alternative at input '..'

Line 14:34 at test/sorttest.hny, no viable alternative at input '[choose(values)foriin1..'

Line 14:34 at test/sorttest.hny, no viable alternative at input '..'```

Duration: 0.0010860999999999787

---
##  test/PClock.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in n-ary operation. Got (';', 'test/PClock.hny', 8, 20), but expected binary operation or 'if' ErrorToken(line=8, message="Parse error in n-ary operation. Got (';', 'test/PClock.hny', 8, 20), but expected binary operation or 'if'", column=20, lexeme=';', filename='test/PClock.hny', is_eof_error=False)```

Duration: 0.0010735000000000605

### Current Output

```
Line 18:4 at test/PClock.hny, mismatched input '@' expecting DEDENT

Line 24:26 at test/PClock.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 37:4 at test/PClock.hny, mismatched input '@' expecting DEDENT

Line 41:26 at test/PClock.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 47:8 at test/PClock.hny, mismatched input '@' expecting DEDENT

Line 48:5 at test/PClock.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 53:8 at test/PClock.hny, mismatched input '@' expecting DEDENT

Line 54:5 at test/PClock.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 56:6 at test/PClock.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 56:24 at test/PClock.hny, no viable alternative at input '..'

Line 62:16 at test/PClock.hny, no viable alternative at input ','

Line 63:16 at test/PClock.hny, no viable alternative at input ','

Line 64:16 at test/PClock.hny, no viable alternative at input ','

Line 65:16 at test/PClock.hny, no viable alternative at input ','```

Duration: 0.0012436000000000114

---
##  test/DinersOrdered.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
nworkers = 16
#states (2)
Safety Violation
Loading test/DinersOrdered.hco
T0: __init__() [0-5,369-371,1104-1116] { bag: (), list: (), synch: () }
Load: unknown address ?Lock[()]```

Duration: 0.0013078000000000811

### Current Output

```
Line 20:8 at test/DinersOrdered.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}```

Duration: 0.001578700000000044

---
##  test/rdwr.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in n-ary operation. Got (':', 'test/rdwr.hny', 1, 16), but expected binary operation or 'if' ErrorToken(line=1, message="Parse error in n-ary operation. Got (':', 'test/rdwr.hny', 1, 16), but expected binary operation or 'if'", column=16, lexeme=':', filename='test/rdwr.hny', is_eof_error=False)```

Duration: 0.0012015000000000775

### Current Output

```
Line 1:15 at test/rdwr.hny, no viable alternative at input ':'

Line 2:39 at test/rdwr.hny, no viable alternative at input 'bagsize'

Line 3:59 at test/rdwr.hny, no viable alternative at input '('

Line 6:33 at test/rdwr.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 7:5 at test/rdwr.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 9:19 at test/rdwr.hny, no viable alternative at input 'assert'

Line 32:5 at test/rdwr.hny, extraneous input 'dedent' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}```

Duration: 0.0017950999999999384

---
##  test/benor.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in statement. Got ('atomic', 'test/benor.hny', 13, 5), but expected expression ErrorToken(line=13, message="Parse error in statement. Got ('atomic', 'test/benor.hny', 13, 5), but expected expression", column=5, lexeme='atomic', filename='test/benor.hny', is_eof_error=False)```

Duration: 0.0010137999999999536

### Current Output

```
Line 21:17 at test/benor.hny, Cannot assign to constant ('msgs', 'test/benor.hny', 21, 17)```

Duration: 0.0014329999999999066

---
##  test/Stop.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in n-ary operation. Got ('..', 'test/Stop.hny', 8, 11), but expected binary operation or 'if' ErrorToken(line=8, message="Parse error in n-ary operation. Got ('..', 'test/Stop.hny', 8, 11), but expected binary operation or 'if'", column=11, lexeme='..', filename='test/Stop.hny', is_eof_error=False)```

Duration: 0.0010423999999999989

### Current Output

```
Line 8:10 at test/Stop.hny, no viable alternative at input '..'```

Duration: 0.0015695000000000014

---
##  test/DinersCVwrong.hny

### Summary

Duration is good: ✅

Output is good: ❌

### Baseline Output

```
Parse error in n-ary operation. Got ('=', 'test/DinersCVwrong.hny', 6, 29), but expected binary operation or 'if' ErrorToken(line=6, message="Parse error in n-ary operation. Got ('=', 'test/DinersCVwrong.hny', 6, 29), but expected binary operation or 'if'", column=29, lexeme='=', filename='test/DinersCVwrong.hny', is_eof_error=False)```

Duration: 0.0009552999999999923

### Current Output

```
Line 6:28 at test/DinersCVwrong.hny, no viable alternative at input '='

Line 6:45 at test/DinersCVwrong.hny, mismatched input ':' expecting {NL, ';'}

Line 35:8 at test/DinersCVwrong.hny, extraneous input 'dict' expecting {'-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', '!', 'print', 'setintlevel', 'stop', 'lambda', '?', 'not', 'None', BOOL, INT, NAME, ATOM, '[', '{', '(', STRING}

Line 35:30 at test/DinersCVwrong.hny, no viable alternative at input '..'

Line 36:8 at test/DinersCVwrong.hny, extraneous input 'dict' expecting {<EOF>, '-', '~', 'abs', 'all', 'any', 'atLabel', 'countLabel', 'choose', 'contexts', 'get_context', 'min', 'max', 'keys', 'hash', 'len', NL, '!', 'import', 'print', 'from', 'setintlevel', 'stop', 'lambda', '?', 'not', 'const', 'await', 'assert', 'var', 'trap', 'possibly', 'pass', 'del', 'spawn', 'invariant', 'go', 'sequential', 'atomic', 'when', 'let', 'if', 'while', 'def', 'for', 'None', 'atomically', BOOL, INT, NAME, ATOM, '[', '{', '(', ';', STRING, INDENT}

Line 36:32 at test/DinersCVwrong.hny, no viable alternative at input ')'

Line 36:44 at test/DinersCVwrong.hny, no viable alternative at input '..'

Line 37:10 at test/DinersCVwrong.hny, no viable alternative at input '..'```

Duration: 0.0013729000000000102

---
##  test/poolmesa.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading test/poolmesa.hco```

Duration: 0.001611000000000029

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading test/poolmesa.hco```

Duration: 0.001847799999999955

---
##  test/DinersVar.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
nworkers = 16
#states (23905)
4285 components
Non-terminating state
Loading test/DinersVar.hco
T0: __init__() [0-5,369-371,1039-1043,766-770,759-764,771,772,1044-1048,1094-1105,1096-1105,1096-1105,1096-1105,1096-1105,1096-1098,1106,1107] { bag: (), forks: [ False, False, False, False, False ], list: (), synch: () }
T3: diner(2) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ False, False, True, False, False ], list: (), synch: () }
T1: diner(0) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, False, False ], list: (), synch: () }
T5: diner(4) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, False, True ], list: (), synch: () }
T4: diner(3) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, True, True ], list: (), synch: () }
T2: diner(1) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, True, True, True, True ], list: (), synch: () }```

Duration: 0.0012651999999999664

### Current Output

```
nworkers = 16
#states (23905)
4285 components
Non-terminating state
Loading test/DinersVar.hco
T0: __init__() [0-5,369-371,1039-1043,766-770,759-764,771,772,1044-1048,1094-1105,1096-1105,1096-1105,1096-1105,1096-1105,1096-1098,1106,1107] { bag: (), forks: [ False, False, False, False, False ], list: (), synch: () }
T3: diner(2) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ False, False, True, False, False ], list: (), synch: () }
T1: diner(0) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, False, False ], list: (), synch: () }
T5: diner(4) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, False, True ], list: (), synch: () }
T4: diner(3) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, True, True ], list: (), synch: () }
T2: diner(1) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, True, True, True, True ], list: (), synch: () }```

Duration: 0.0013694999999999125

---