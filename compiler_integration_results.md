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
Loading harmony_model_checker/modules/bag.hco
```

Duration: 0.0015591000000000008

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/bag.hco
```

Duration: 0.0017630000000000007

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
Loading harmony_model_checker/modules/synchBusy.hco
```

Duration: 0.001424599999999998

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synchBusy.hco
```

Duration: 0.0013767000000000015

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
Loading harmony_model_checker/modules/synchImprecise.hco
```

Duration: 0.0014416999999999972

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synchImprecise.hco
```

Duration: 0.0012042000000000025

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
Loading harmony_model_checker/modules/synch.hco
```

Duration: 0.0014131999999999964

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synch.hco
```

Duration: 0.0016366999999999979

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
Loading harmony_model_checker/modules/alloc.hco
```

Duration: 0.0011938999999999977

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/alloc.hco
```

Duration: 0.0012177000000000021

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
Loading harmony_model_checker/modules/hoare.hco
```

Duration: 0.0017345999999999959

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/hoare.hco
```

Duration: 0.0011765999999999999

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
Loading harmony_model_checker/modules/synchS.hco
```

Duration: 0.0012980000000000005

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/synchS.hco
```

Duration: 0.0011530000000000012

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
Loading harmony_model_checker/modules/set.hco
```

Duration: 0.0013244000000000034

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/set.hco
```

Duration: 0.0012030999999999986

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
Loading harmony_model_checker/modules/list.hco
```

Duration: 0.0011928000000000008

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading harmony_model_checker/modules/list.hco
```

Duration: 0.0013734999999999997

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
Loading code/prog1.hco
```

Duration: 0.0012899000000000035

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/prog1.hco
```

Duration: 0.001127000000000003

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
Harmony assertion failed
```

Duration: 0.0010559999999999944

### Current Output

```
nworkers = 16
#states (11)
Safety Violation
Loading code/prog2.hco
T0: __init__() [0-3,17-25] { shared: True }
T2: g() [13-16] { shared: False }
T1: f() [4-8] { shared: False }
Harmony assertion failed
```

Duration: 0.0011359999999999981

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
Harmony assertion failed
```

Duration: 0.0011398999999999992

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
Harmony assertion failed
```

Duration: 0.0011767999999999987

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
T2: incrementer(1) [19-25] { count: 0, done: [ False, False ], entered: [ True, True ] }
```

Duration: 0.001706299999999994

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
T2: incrementer(1) [19-25] { count: 0, done: [ False, False ], entered: [ True, True ] }
```

Duration: 0.0012427999999999953

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
Harmony assertion failed
```

Duration: 0.0012187000000000031

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
Harmony assertion failed
```

Duration: 0.001082699999999992

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
Harmony assertion failed
```

Duration: 0.0012585999999999986

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
Harmony assertion failed
```

Duration: 0.0011298999999999892

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
Harmony assertion failed
```

Duration: 0.0011180999999999969

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
Harmony assertion failed
```

Duration: 0.0011268000000000111

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
T1: thread(0) [4-6(choose True),7-17] { flags: [ True, True ] }
```

Duration: 0.0011369999999999991

### Current Output

```
nworkers = 16
#states (45)
15 components
Non-terminating state
Loading code/naiveFlags.hco
T0: __init__() [0-3,42-50] { flags: [ False, False ] }
T2: thread(1) [4-6(choose True),7-17] { flags: [ False, True ] }
T1: thread(0) [4-6(choose True),7-17] { flags: [ True, True ] }
```

Duration: 0.0011436999999999975

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
T2: thread(1) [4-6(choose False),7,30,31] { turn: 1 }
```

Duration: 0.001646700000000001

### Current Output

```
nworkers = 16
#states (28)
21 components
Non-terminating state
Loading code/naiveTurn.hco
T0: __init__() [0-3,32-40] { turn: 0 }
T1: thread(0) [4-6(choose True),7-11] { turn: 1 }
T2: thread(1) [4-6(choose False),7,30,31] { turn: 1 }
```

Duration: 0.0011516000000000026

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
Loading code/Peterson.hco
```

Duration: 0.001292599999999991

### Current Output

```
nworkers = 16
#states (104)
37 components
No issues
Loading code/Peterson.hco
```

Duration: 0.0011850000000000055

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
Loading code/PetersonInductive.hco
```

Duration: 0.0012658000000000114

### Current Output

```
nworkers = 16
#states (104)
37 components
No issues
Loading code/PetersonInductive.hco
```

Duration: 0.0011748000000000036

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
T1: thread(0) [6-8(choose True),9-19] { flags: [ True, True ] }
```

Duration: 0.0016533999999999993

### Current Output

```
nworkers = 16
#states (73)
18 components
Active busy waiting
Loading code/csonebit.hco
T0: __init__() [0-5,52-60] { flags: [ False, False ] }
T2: thread(1) [6-8(choose True),9-19] { flags: [ False, True ] }
T1: thread(0) [6-8(choose True),9-19] { flags: [ True, True ] }
```

Duration: 0.001329700000000003

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
Loading code/PetersonMethod.hco
```

Duration: 0.00152759999999999

### Current Output

```
nworkers = 16
#states (104)
37 components
No issues
Loading code/PetersonMethod.hco
```

Duration: 0.0012619999999999992

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
Harmony assertion failed
```

Duration: 0.0015866999999999964

### Current Output

```
nworkers = 16
#states (5462)
Safety Violation
Loading code/clock.hco
T0: __init__() [0,1,132-139,2-21,140-144,2-21,145-172,179-195,23-45,81-131,196-205,23-45,81-131,206-226,161-172,179-195,23-45,81-131,196-205,23-45,81-131,206-226,161-172,179-195,23-45,81-131,196-205,23-45,81-131,206-226,161-172,179-195,23-80,31-80,31-80,31-45,81-131,196-205,23-45,81-131,206-226,161-168,173-178(choose 2),179-195,23-30,115-131,196-205,23-30,115-131,206-226,161-168,173-178(choose 1),179-195,23-80,31-45,81-131,196-205,23-30,115-131,206-226,161-168,173-178(choose 2),179-195,23-30,115-131,196-205,23-30,115-131,206-226,161-168,173-178(choose 5),179-195,23-80,31-80,31-80,31-45,81-131,196-205,23-80,31-80,31-80,31-80,31-45,81-131,206-226,161-168,173-178(choose 1),179-195,23-30,115-131,196-205,23-45,81-131,206-226,161-168,173-178(choose 2),179-195,23-30,115-131,196-205,23-45,81-131,206-218] { clock3: { "entries": [ 5, 2, 1 ], "hand": 1, "misses": 6, "recent": { 1, 2, 5 } }, clock4: { "entries": [ 5, 1, 2, 4 ], "hand": 3, "misses": 7, "recent": { 1, 2, 5 } }, refs: [ 1, 2, 3, 4, 2, 1, 2, 5, 1, 2 ] }
Harmony assertion failed
```

Duration: 0.0015458

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
Loading code/spinlock.hco
```

Duration: 0.0017493000000000092

### Current Output

```
nworkers = 16
#states (473)
148 components
No issues
Loading code/spinlock.hco
```

Duration: 0.0012376999999999944

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
Loading code/UpLock.hco
```

Duration: 0.0015714000000000006

### Current Output

```
nworkers = 16
#states (57)
57 components
No issues
Loading code/UpLock.hco
```

Duration: 0.0015575000000000033

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
Loading code/UpLock.hco
```

Duration: 0.0013340000000000019

### Current Output

```
nworkers = 16
#states (59)
59 components
No issues
Loading code/UpLock.hco
```

Duration: 0.00120279999999999

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
Harmony assertion failed: (50, 100)
```

Duration: 0.001099799999999998

### Current Output

```
nworkers = 16
#states (20)
Safety Violation
Loading code/xy.hco
T0: __init__() [0-9,54-62] { x: 0, y: 100 }
T2: setX(50) [10-16] { x: 50, y: 100 }
T1: checker() [32-35,20-30,36-50] { x: 50, y: 100 }
Harmony assertion failed: (50, 100)
```

Duration: 0.0010962000000000055

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
T1: customer(1, 0, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-785] { accounts: [ { "balance": 1, "lock": False }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }
T2: customer(2, 0, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-789,793-799,1132-1153,801-815,1154,1155,1179-1182] { accounts: [ { "balance": 0, "lock": False }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }
T1: customer(1, 0, 1) [786-789,793-799,1132-1153,801-804] { accounts: [ { "balance": -1, "lock": True }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }
```

Duration: 0.001398499999999997

### Current Output

```
nworkers = 16
#states (4110)
Invariant Violation
Loading code/atm.hco
T0: __init__() [0-5,369-371,1039-1054,766-770,759-764,771,772,1055-1058(choose 1),1059-1062,1044-1054,766-770,759-764,771,772,1055-1058(choose 1),1059-1062,1044-1046,1063-1066,1094,1183-1197(choose 0),1198-1201(choose 1),1202-1205,1185-1197(choose 0),1198-1201(choose 1),1202-1205,1185-1187,1206,1207] { accounts: [ { "balance": 1, "lock": False }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }
T2: customer(2, 0, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-785] { accounts: [ { "balance": 1, "lock": False }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }
T1: customer(1, 0, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-789,793-799,1132-1153,801-815,1154,1155,1179-1182] { accounts: [ { "balance": 0, "lock": False }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }
T2: customer(2, 0, 1) [786-789,793-799,1132-1153,801-804] { accounts: [ { "balance": -1, "lock": True }, { "balance": 1, "lock": False } ], bag: (), list: (), synch: () }
```

Duration: 0.001130099999999995

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
Loading code/queuedemo.hco
```

Duration: 0.001266299999999998

### Current Output

```
nworkers = 16
#states (80)
80 components
No issues
Loading code/queuedemo.hco
```

Duration: 0.0014692000000000038

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
Loading code/queuedemo.hco
```

Duration: 0.0016508999999999968

### Current Output

```
nworkers = 16
#states (80)
80 components
No issues
Loading code/queuedemo.hco
```

Duration: 0.0012780000000000014

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
Loading code/qtestseq.hco
```

Duration: 0.0015555000000000013

### Current Output

```
nworkers = 16
#states (600)
600 components
No issues
Loading code/qtestseq.hco
```

Duration: 0.001575000000000007

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
Loading code/qtest1.hco
```

Duration: 0.0016088999999999964

### Current Output

```
nworkers = 16
#states (274)
274 components
No issues
Loading code/qtest1.hco
```

Duration: 0.0012550000000000061

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
Loading code/qtest1.hco
```

Duration: 0.001270199999999999

### Current Output

```
nworkers = 16
#states (274)
274 components
No issues
Loading code/qtest1.hco
```

Duration: 0.0015231999999999885

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
Loading code/qtest2.hco
```

Duration: 0.0015832000000000068

### Current Output

```
nworkers = 16
#states (55)
55 components
No issues
Loading code/qtest2.hco
```

Duration: 0.0013808000000000015

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
Loading code/qtest2.hco
```

Duration: 0.0012106999999999812

### Current Output

```
nworkers = 16
#states (55)
55 components
No issues
Loading code/qtest2.hco
```

Duration: 0.0015408999999999978

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
Loading code/qtest3.hco
```

Duration: 0.001308599999999993

### Current Output

```
nworkers = 16
#states (3225)
3225 components
No issues
Loading code/qtest3.hco
```

Duration: 0.0015415000000000012

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
Loading code/qtest3.hco
```

Duration: 0.0013587999999999933

### Current Output

```
nworkers = 16
#states (3225)
3225 components
No issues
Loading code/qtest3.hco
```

Duration: 0.0014346999999999832

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
Loading code/qtest4.hco
```

Duration: 0.0011928999999999967

### Current Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/qtest4.hco
```

Duration: 0.0011160000000000059

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
Loading code/qtest4.hco
```

Duration: 0.0017073999999999978

### Current Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/qtest4.hco
```

Duration: 0.0014686000000000143

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
Loading code/qtestconc.hco
```

Duration: 0.003019999999999995

### Current Output

```
nworkers = 16
#states (2127239)
2127239 components
No issues
Loading code/qtestconc.hco
```

Duration: 0.002994500000000011

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
Loading code/qtestconc.hco
```

Duration: 0.004718

### Current Output

```
nworkers = 16
#states (3430951)
3430951 components
No issues
Loading code/qtestconc.hco
```

Duration: 0.005551499999999987

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
Loading code/queuedemo.hco
```

Duration: 0.0016076000000000146

### Current Output

```
nworkers = 16
#states (3125)
3125 components
No issues
Loading code/queuedemo.hco
```

Duration: 0.0013605999999999896

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
Loading code/queuedemo.hco
```

Duration: 0.0014637000000000122

### Current Output

```
nworkers = 16
#states (3287)
3287 components
No issues
Loading code/queuedemo.hco
```

Duration: 0.0013685999999999976

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
Loading code/intsettest.hco
```

Duration: 0.0013192999999999955

### Current Output

```
nworkers = 16
#states (12368)
12368 components
No issues
Loading code/intsettest.hco
```

Duration: 0.0014060000000000183

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
Loading code/intsettest.hco
```

Duration: 0.0013111000000000095

### Current Output

```
nworkers = 16
#states (18377)
18377 components
No issues
Loading code/intsettest.hco
```

Duration: 0.001723499999999989

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
Loading code/RWtest.hco
```

Duration: 0.0013498999999999872

### Current Output

```
nworkers = 16
#states (135)
27 components
No issues
Loading code/RWtest.hco
```

Duration: 0.0013330000000000009

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
Loading code/RWtest.hco
```

Duration: 0.001459999999999989

### Current Output

```
nworkers = 16
#states (135)
27 components
No issues
Loading code/RWtest.hco
```

Duration: 0.0013757000000000075

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
Loading code/RWtest.hco
```

Duration: 0.0012727999999999906

### Current Output

```
nworkers = 16
#states (1943)
619 components
No issues
Loading code/RWtest.hco
```

Duration: 0.0013168000000000069

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
Loading code/RWtest.hco
```

Duration: 0.001392499999999991

### Current Output

```
nworkers = 16
#states (4212)
897 components
No issues
Loading code/RWtest.hco
```

Duration: 0.0011271999999999949

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
Loading code/RWtest.hco
```

Duration: 0.0012496999999999925

### Current Output

```
nworkers = 16
#states (1438)
449 components
No issues
Loading code/RWtest.hco
```

Duration: 0.001159100000000024

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
Loading code/RWtest.hco
```

Duration: 0.0013431999999999888

### Current Output

```
nworkers = 16
#states (3137)
635 components
No issues
Loading code/RWtest.hco
```

Duration: 0.0013205000000000022

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
Loading code/BBtest.hco
```

Duration: 0.001193699999999992

### Current Output

```
nworkers = 16
#states (1175)
1175 components
No issues
Loading code/BBtest.hco
```

Duration: 0.0013294000000000084

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
Loading code/BBtest.hco
```

Duration: 0.0016912000000000038

### Current Output

```
nworkers = 16
#states (4127)
4127 components
No issues
Loading code/BBtest.hco
```

Duration: 0.001204700000000003

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
Loading code/RWtest.hco
```

Duration: 0.0012745000000000117

### Current Output

```
nworkers = 16
#states (1902)
406 components
No issues
Loading code/RWtest.hco
```

Duration: 0.0012196000000000151

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
Loading code/RWtest.hco
```

Duration: 0.0012613999999999959

### Current Output

```
nworkers = 16
#states (4301)
666 components
No issues
Loading code/RWtest.hco
```

Duration: 0.0012482000000000049

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
Loading code/qsorttest.hco
```

Duration: 0.0011635999999999869

### Current Output

```
nworkers = 16
#states (454)
454 components
No issues
Loading code/qsorttest.hco
```

Duration: 0.0011496000000000006

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
T2: diner(1) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, True, True, True, True ], list: (), synch: () }
```

Duration: 0.001543899999999987

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
T2: diner(1) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, True, True, True, True ], list: (), synch: () }
```

Duration: 0.0013057000000000207

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
T2: diner(1) [430-441] { forks: [ { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] } ], list: (), synch: () }
```

Duration: 0.0012889999999999846

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
T2: diner(1) [430-441] { forks: [ { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] }, { "acquired": True, "suspended": [ CONTEXT("diner") ] } ], list: (), synch: () }
```

Duration: 0.0014309999999999878

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
Loading code/DinersCV.hco
```

Duration: 0.0014756999999999965

### Current Output

```
nworkers = 16
#states (111679)
39194 components
No issues
Loading code/DinersCV.hco
```

Duration: 0.0013920000000000043

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
Loading code/DinersCV.hco
```

Duration: 0.0029032999999999975

### Current Output

```
nworkers = 16
#states (2293519)
441764 components
No issues
Loading code/DinersCV.hco
```

Duration: 0.0029364000000000057

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
Loading code/DinersAvoid.hco
```

Duration: 0.0015220999999999985

### Current Output

```
nworkers = 16
#states (86214)
5589 components
No issues
Loading code/DinersAvoid.hco
```

Duration: 0.00143879999999999

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
Loading code/DinersAvoid.hco
```

Duration: 0.0014905999999999808

### Current Output

```
nworkers = 16
#states (152874)
10504 components
No issues
Loading code/DinersAvoid.hco
```

Duration: 0.001398200000000016

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
T2: thread() [1142-1144(choose 1),1145-1151(choose 0),1152-1165(choose 2),1166,1167,1067-1075,782-789,793-799,1076-1102,782-785] { accounts: [ { "balance": 1, "lock": True }, { "balance": 0, "lock": True } ], bag: (), list: (), synch: () }
```

Duration: 0.0015583000000000125

### Current Output

```
nworkers = 16
#states (3359)
3359 components
Non-terminating state
Loading code/bank.hco
T0: __init__() [0-5,369-371,1039-1054,766-770,759-764,771,772,1055-1058(choose 2),1059-1062,1044-1054,766-770,759-764,771,772,1055-1058(choose 2),1059-1062,1044-1046,1063-1066,1170-1181,1172-1181,1172-1174,1182,1183] { accounts: [ { "balance": 2, "lock": False }, { "balance": 2, "lock": False } ], bag: (), list: (), synch: () }
T1: thread() [1142-1144(choose 0),1145-1151(choose 1),1152-1165(choose 1),1166,1167,1067-1075,782-789,793-799,1076-1102,782-785] { accounts: [ { "balance": 1, "lock": True }, { "balance": 2, "lock": False } ], bag: (), list: (), synch: () }
T2: thread() [1142-1144(choose 1),1145-1151(choose 0),1152-1165(choose 2),1166,1167,1067-1075,782-789,793-799,1076-1102,782-785] { accounts: [ { "balance": 1, "lock": True }, { "balance": 0, "lock": True } ], bag: (), list: (), synch: () }
```

Duration: 0.0014631999999999978

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
Loading code/counter.hco
```

Duration: 0.001245099999999999

### Current Output

```
nworkers = 16
#states (601)
601 components
No issues
Loading code/counter.hco
```

Duration: 0.001536799999999977

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
Loading code/qbarrier.hco
```

Duration: 0.0012875999999999999

### Current Output

```
nworkers = 16
#states (1664)
1664 components
No issues
Loading code/qbarrier.hco
```

Duration: 0.0016684999999999894

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
Loading code/qbarrier.hco
```

Duration: 0.001283499999999993

### Current Output

```
nworkers = 16
#states (4927)
4927 components
No issues
Loading code/qbarrier.hco
```

Duration: 0.001040299999999994

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
Loading code/barriertest.hco
```

Duration: 0.0013384000000000174

### Current Output

```
nworkers = 16
#states (2802)
2802 components
No issues
Loading code/barriertest.hco
```

Duration: 0.0012001999999999846

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
Loading code/barriertest.hco
```

Duration: 0.0013514000000000026

### Current Output

```
nworkers = 16
#states (7425)
7425 components
No issues
Loading code/barriertest.hco
```

Duration: 0.0015431999999999946

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
T1: main() [17-20] { count: 0, done: False }
```

Duration: 0.0014662000000000008

### Current Output

```
nworkers = 16
#states (3)
3 components
Non-terminating state
Loading code/trap.hco
T0: __init__() [0-7,34-38] { count: 0, done: False }
T1: main() [17-20] { count: 0, done: False }
```

Duration: 0.0010378999999999805

---
##  code/trap2.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
constant cannot be an lvalue: ('ok', 'code/trap2.hny', 4, 19) ErrorToken(line=1, message="constant cannot be an lvalue: ('ok', 'code/trap2.hny', 4, 19)", column=5, lexeme='LABEL(0, ok)', filename='code/trap2.hny', is_eof_error=False)
```

Duration: 0.000992700000000013

### Current Output

```
Line 1:5 at code/trap2.hny, constant cannot be an lvalue: ('ok', 'code/trap2.hny', 4, 19)
```

Duration: 0.0009274999999999978

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
T1: main() [1067-1073,782-789,793-799,1074] { bag: (), count: 0, countlock: True, done: False, list: (), synch: () }
```

Duration: 0.001620399999999994

### Current Output

```
nworkers = 16
#states (4)
Safety Violation
Loading code/trap3.hco
T0: __init__() [0-5,369-371,1039-1043,766-770,759-764,771,772,1044-1049,1096-1100] { bag: (), count: 0, countlock: False, done: False, list: (), synch: () }
T1: main() [1067-1073,782-789,793-799,1074] { bag: (), count: 0, countlock: True, done: False, list: (), synch: () }
```

Duration: 0.0014388000000000178

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
T1: main() [17-30] { count: 1, done: False }
```

Duration: 0.0011699000000000015

### Current Output

```
nworkers = 16
#states (5)
5 components
Non-terminating state
Loading code/trap4.hco
T0: __init__() [0-7,44-48] { count: 0, done: False }
T1: main() [17-30] { count: 1, done: False }
```

Duration: 0.0010397999999999796

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
T1: main() [31-37,8-20,38] { count: 1, done: False }
```

Duration: 0.0013193999999999984

### Current Output

```
nworkers = 16
#states (5)
5 components
Non-terminating state
Loading code/trap5.hco
T0: __init__() [0-7,52-56] { count: 0, done: False }
T1: main() [31-37,8-20,38] { count: 1, done: False }
```

Duration: 0.0011275999999999786

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
T2: thread(1) [1085-1092,1050-1056,782-789,793-799,1057-1064,801-815,1065-1070,1093] { bag: (), count: 2, countlock: False, done: [ False, False ], list: (), synch: () }
```

Duration: 0.001168300000000011

### Current Output

```
nworkers = 16
#states (34)
34 components
Non-terminating state
Loading code/trap6.hco
T0: __init__() [0-5,369-371,1039-1045,766-770,759-764,771,772,1046-1049,1109-1117] { bag: (), count: 0, countlock: False, done: [ False, False ], list: (), synch: () }
T1: thread(0) [1085-1092,1050-1056,782-789,793-799,1057-1064,801-815,1065-1070,1093] { bag: (), count: 1, countlock: False, done: [ False, False ], list: (), synch: () }
T2: thread(1) [1085-1092,1050-1056,782-789,793-799,1057-1064,801-815,1065-1070,1093] { bag: (), count: 2, countlock: False, done: [ False, False ], list: (), synch: () }
```

Duration: 0.0012514000000000136

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
T2: thread(1) [845-852,810-816,425-431,455-462,817-824,464-488,508,509,825-830,853] { count: 2, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }
```

Duration: 0.0012530999999999515

### Current Output

```
nworkers = 16
#states (36)
36 components
Non-terminating state
Loading code/trap6.hco
T0: __init__() [0-5,799-805,417-421,404-415,422,423,806-809,869-877] { count: 0, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }
T1: thread(0) [845-852,810-816,425-431,455-462,817-824,464-488,508,509,825-830,853] { count: 1, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }
T2: thread(1) [845-852,810-816,425-431,455-462,817-824,464-488,508,509,825-830,853] { count: 2, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }
```

Duration: 0.0011816000000000049

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
Loading code/hw.hco
```

Duration: 0.001257100000000011

### Current Output

```
nworkers = 16
#states (23864)
18524 components
No issues
Loading code/hw.hco
```

Duration: 0.0013818999999999915

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
Loading code/abptest.hco
```

Duration: 0.001272300000000004

### Current Output

```
nworkers = 16
#states (1536)
608 components
No issues
Loading code/abptest.hco
```

Duration: 0.0013524999999999787

---
##  code/byzbosco.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot assign to constant ('proposal', 'code/byzbosco.hny', 23, 17) ErrorToken(line=23, message="Cannot assign to constant ('proposal', 'code/byzbosco.hny', 23, 17)", column=26, lexeme='=', filename='code/byzbosco.hny', is_eof_error=False)
```

Duration: 0.0009989999999999721

### Current Output

```
Line 23:17 at code/byzbosco.hny, Cannot assign to constant ('proposal', 'code/byzbosco.hny', 23, 17)
```

Duration: 0.00088870000000002

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
Load: unknown address ?BBsema["Semaphore"][1]
```

Duration: 0.0014895000000000325

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/BBsematest.hco
T0: __init__() [0-7,371-373,1111-1122,1114-1122,1114-1116,1123-1132] { BBsema: { "b_in": 1, "b_out": 1, "buf": { 1: (), 2: () } }, bag: (), list: (), synch: () }
Load: unknown address ?BBsema["Semaphore"][1]
```

Duration: 0.001482199999999989

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
Loading code/ky.hco
```

Duration: 0.0016242999999999674

### Current Output

```
nworkers = 16
#states (14)
12 components
No issues
Loading code/ky.hco
```

Duration: 0.0012032000000000154

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
Loading code/bosco.hco
```

Duration: 0.0013533000000000017

### Current Output

```
nworkers = 16
#states (7404)
7404 components
No issues
Loading code/bosco.hco
```

Duration: 0.0013232000000000244

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
Loading code/RWsbs.hco
```

Duration: 0.001346600000000031

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWsbs.hco
```

Duration: 0.0012323000000000195

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
Loading code/queuebroken.hco
```

Duration: 0.0013214999999999755

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuebroken.hco
```

Duration: 0.0014625999999999806

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
Loading code/hello7.hco
```

Duration: 0.0011671999999999794

### Current Output

```
nworkers = 16
#states (17)
17 components
No issues
Loading code/hello7.hco
```

Duration: 0.001154299999999997

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
Loading code/multitest.hco
```

Duration: 0.0011981999999999826

### Current Output

```
nworkers = 16
#states (3)
3 components
No issues
Loading code/multitest.hco
```

Duration: 0.0012099999999999889

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
Load: unknown address ?BBsema["Semaphore"][1]
```

Duration: 0.0012797999999999976

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/BBsemadata.hco
T0: __init__() [0-7,371-373,1111-1122,1114-1122,1114-1116,1123-1132] { BBsema: { "b_in": 1, "b_out": 1, "buf": { 1: (), 2: () } }, bag: (), list: (), synch: () }
Load: unknown address ?BBsema["Semaphore"][1]
```

Duration: 0.0011682999999999555

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
Load: unknown variable left
```

Duration: 0.0011509000000000102

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/dinersfix2.hco
T0: __init__() [0-7] { }
Load: unknown variable left
```

Duration: 0.0012274000000000451

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
Loading code/qsort.hco
```

Duration: 0.0013688000000000033

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/qsort.hco
```

Duration: 0.0013523999999999758

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
Loading code/setobj.hco
```

Duration: 0.0013620999999999772

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/setobj.hco
```

Duration: 0.0011576999999999837

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
Load: unknown variable left
```

Duration: 0.0012967999999999869

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/baddblwait.hco
T0: __init__() [0-2] { }
Load: unknown variable left
```

Duration: 0.001052300000000006

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
Loading code/nbqueuetest.hco
```

Duration: 0.0011545000000000027

### Current Output

```
nworkers = 16
#states (1393)
1393 components
No issues
Loading code/nbqueuetest.hco
```

Duration: 0.0010950000000000126

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
Loading code/cssynch.hco
```

Duration: 0.0011475000000000235

### Current Output

```
nworkers = 16
#states (22)
10 components
No issues
Loading code/cssynch.hco
```

Duration: 0.0012618999999999825

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
Loading code/stack3.hco
```

Duration: 0.0012215999999999894

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack3.hco
```

Duration: 0.0010142000000000206

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
Load: unknown address ?Semaphore[1]
```

Duration: 0.001253100000000007

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWqueue.hco
T0: __init__() [0-5,369-371,1251-1254] { bag: (), list: (), synch: () }
Load: unknown address ?Semaphore[1]
```

Duration: 0.001270599999999955

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
Load: unknown address ?Semaphore[3]
```

Duration: 0.0013505999999999796

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/DinersSema.hco
T0: __init__() [0-5,369-371,1057-1060] { bag: (), list: (), synch: () }
Load: unknown address ?Semaphore[3]
```

Duration: 0.0012125000000000052

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
Loading code/RWcv.hco
```

Duration: 0.0014030999999999905

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWcv.hco
```

Duration: 0.0012950999999999935

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
Load: unknown address ?RWlock["Lock"][()]
```

Duration: 0.0014353000000000282

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWmulti.hco
T0: __init__() [0-7,371-373,1109-1112] { RWlock: (), bag: (), list: (), synch: () }
Load: unknown address ?RWlock["Lock"][()]
```

Duration: 0.0017231999999999803

---
##  code/2pc.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot operate on constant ('balance', 'code/2pc.hny', 20, 21) ErrorToken(line=20, message="Cannot operate on constant ('balance', 'code/2pc.hny', 20, 21)", column=29, lexeme='-=', filename='code/2pc.hny', is_eof_error=False)
```

Duration: 0.001140299999999983

### Current Output

```
Line 20:29 at code/2pc.hny, Cannot operate on constant ('balance', 'code/2pc.hny', 20, 21)
```

Duration: 0.0008547999999999889

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
Loading code/queueconc.hco
```

Duration: 0.0013248000000000149

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queueconc.hco
```

Duration: 0.001424599999999998

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
Loading code/queuelin.hco
```

Duration: 0.0011991000000000085

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuelin.hco
```

Duration: 0.0012263000000000135

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
Loading code/lockspec.hco
```

Duration: 0.0012294999999999945

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/lockspec.hco
```

Duration: 0.0014039999999999608

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
Loading code/ky2.hco
```

Duration: 0.0015700999999999632

### Current Output

```
nworkers = 16
#states (14)
12 components
No issues
Loading code/ky2.hco
```

Duration: 0.0011109000000000258

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
Loading code/cslock.hco
```

Duration: 0.001448700000000025

### Current Output

```
nworkers = 16
#states (97)
97 components
No issues
Loading code/cslock.hco
```

Duration: 0.001224999999999976

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
Loading code/abp.hco
```

Duration: 0.0015695000000000014

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/abp.hco
```

Duration: 0.0011412999999999562

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
Loading code/hello2.hco
```

Duration: 0.0016206000000000276

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hello2.hco
```

Duration: 0.0011392000000000069

---
##  code/actortest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9) ErrorToken(line=26, message="Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9)", column=19, lexeme='-=', filename='code/actor.hny', is_eof_error=False)
```

Duration: 0.0010229999999999961

### Current Output

```
Line 26:19 at code/actor.hny, Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9)
```

Duration: 0.0010585000000000178

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
Loading code/hello4.hco
```

Duration: 0.0022148000000000168

### Current Output

```
nworkers = 16
#states (3)
3 components
No issues
Loading code/hello4.hco
```

Duration: 0.0012352999999999947

---
##  code/actor.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9) ErrorToken(line=26, message="Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9)", column=19, lexeme='-=', filename='code/actor.hny', is_eof_error=False)
```

Duration: 0.0009993000000000363

### Current Output

```
Line 26:19 at code/actor.hny, Cannot operate on constant ('nrequests', 'code/actor.hny', 26, 9)
```

Duration: 0.0009380999999999973

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
Loading code/chain.hco
```

Duration: 0.0013825000000000087

### Current Output

```
nworkers = 16
#states (69601)
45835 components
No issues
Loading code/chain.hco
```

Duration: 0.0016953000000000107

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
Loading code/boundedbuffer.hco
```

Duration: 0.0013754000000000266

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/boundedbuffer.hco
```

Duration: 0.0012300000000000089

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
Loading code/lockintf.hco
```

Duration: 0.0012042000000000441

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/lockintf.hco
```

Duration: 0.0014954000000000356

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
Loading code/taslock.hco
```

Duration: 0.001554600000000017

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/taslock.hco
```

Duration: 0.001154299999999997

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
Loading code/RW.hco
```

Duration: 0.0012992000000000004

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RW.hco
```

Duration: 0.0011797999999999531

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
match: expected ()
```

Duration: 0.0013494000000000006

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/DinersCV2.hco
T0: __init__() [0-5,369-371,1039-1041,766-770,759-764,771,772,1042-1049,825] { bag: (), forks: [ False, False, False, False, False ], list: (), mutex: False, synch: () }
match: expected ()
```

Duration: 0.0011314000000000046

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
Load: unknown variable NBANKS
```

Duration: 0.0012884999999999702

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/2pc2.hco
T0: __init__() [0-3,735-737] { list: () }
Load: unknown variable NBANKS
```

Duration: 0.001154299999999997

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
Loading code/rsmspec.hco
```

Duration: 0.001409400000000005

### Current Output

```
nworkers = 16
#states (5048)
5048 components
No issues
Loading code/rsmspec.hco
```

Duration: 0.001228199999999957

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
Load: unknown variable leader
```

Duration: 0.0012590000000000101

### Current Output

```
nworkers = 16
#states (8)
Safety Violation
Loading code/paxos1.hco
T0: __init__() [0-3,356-358,4-8,359-372(choose 0),373-375,365-372(choose 0),373-375,365-367,376-379,454,455(print [ 0, 0 ]),456-462] { bag: (), network: (), proposals: [ 0, 0 ] }
Load: unknown variable leader
```

Duration: 0.0014461000000000057

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
Loading code/queuespec.hco
```

Duration: 0.0015178000000000136

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuespec.hco
```

Duration: 0.0012705000000000077

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
Loading code/RWbtest.hco
```

Duration: 0.0014627999999999863

### Current Output

```
nworkers = 16
#states (3745)
28 components
No issues
Loading code/RWbtest.hco
```

Duration: 0.00123829999999997

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
Loading code/RWhoare.hco
```

Duration: 0.0016720000000000068

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWhoare.hco
```

Duration: 0.0012796999999999947

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
Loading code/RWbusy.hco
```

Duration: 0.0016206000000000276

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWbusy.hco
```

Duration: 0.0016686999999999674

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
Loading code/qtestpar.hco
```

Duration: 0.0012213999999999836

### Current Output

```
nworkers = 16
#states (16332)
16332 components
No issues
Loading code/qtestpar.hco
```

Duration: 0.0011699000000000015

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
Loading code/leader.hco
```

Duration: 0.00162859999999998

### Current Output

```
nworkers = 16
#states (22279)
15056 components
No issues
Loading code/leader.hco
```

Duration: 0.0016439999999999788

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
Loading code/hoare.hco
```

Duration: 0.0012795999999999919

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hoare.hco
```

Duration: 0.0014118000000000186

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
Loading code/RWfair.hco
```

Duration: 0.0013910999999999785

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWfair.hco
```

Duration: 0.0016978999999999744

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
Loading code/register.hco
```

Duration: 0.001374299999999995

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/register.hco
```

Duration: 0.0015210999999999975

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
Load: unknown address ?LinkedList[()]
```

Duration: 0.0013646999999999965

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/lltest.hco
T0: __init__() [0-7,371-373,1041-1047,1331-1334] { alloc: { "next": 0, "pool": () }, bag: (), linkedlist: (), list: (), synch: () }
Load: unknown address ?LinkedList[()]
```

Duration: 0.0014177000000000217

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
Loading code/paxos.hco
```

Duration: 0.001381800000000044

### Current Output

```
nworkers = 16
#states (50808)
50808 components
No issues
Loading code/paxos.hco
```

Duration: 0.0012435999999999559

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
Load: unknown address ?Lock[()]
```

Duration: 0.0011957999999999691

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWlock.hco
T0: __init__() [0-5,369-371,1107-1110] { bag: (), list: (), synch: () }
Load: unknown address ?Lock[()]
```

Duration: 0.0011969000000000007

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
Loading code/mesa.hco
```

Duration: 0.0012028000000000039

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/mesa.hco
```

Duration: 0.0013124999999999942

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
Load: unknown address ?RWqueue["Semaphore"][1]
```

Duration: 0.0013462000000000196

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWqtest.hco
T0: __init__() [0-7,371-373,1253-1256] { RWqueue: (), bag: (), list: (), synch: () }
Load: unknown address ?RWqueue["Semaphore"][1]
```

Duration: 0.0012836999999999987

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
Load: unknown address ?Semaphore[1]
```

Duration: 0.0012495000000000145

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/BBsema.hco
T0: __init__() [0-5,369-371,1109-1120,1112-1120,1112-1114,1121-1130] { b_in: 1, b_out: 1, bag: (), buf: { 1: (), 2: () }, list: (), synch: () }
Load: unknown address ?Semaphore[1]
```

Duration: 0.0014213000000000142

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
Loading code/queue.hco
```

Duration: 0.0014284999999999992

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queue.hco
```

Duration: 0.0011697999999999986

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
Loading code/barrier.hco
```

Duration: 0.0011592000000000269

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/barrier.hco
```

Duration: 0.0010718000000000116

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
Loading code/ticket.hco
```

Duration: 0.001366299999999987

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/ticket.hco
```

Duration: 0.0012309000000000347

---
##  code/PetersonPrint.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```

```

Duration: 0.000953499999999996

### Current Output

```

```

Duration: 0.0008098999999999745

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
Loading code/atomicinc.hco
```

Duration: 0.0011438000000000281

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/atomicinc.hco
```

Duration: 0.001242199999999971

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
Loading code/nbqueue.hco
```

Duration: 0.0011546000000000056

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/nbqueue.hco
```

Duration: 0.0015107000000000315

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
Load: unknown variable left
```

Duration: 0.0012015999999999694

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/dinersfix.hco
T0: __init__() [0,1] { }
Load: unknown variable left
```

Duration: 0.0010379999999999834

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
Loading code/stack2.hco
```

Duration: 0.001268199999999997

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack2.hco
```

Duration: 0.0012841000000000102

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
Loading code/gpu.hco
```

Duration: 0.001251900000000028

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/gpu.hco
```

Duration: 0.0011608000000000174

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
Loading code/triangle.hco
```

Duration: 0.001184699999999983

### Current Output

```
nworkers = 16
#states (13)
13 components
No issues
Loading code/triangle.hco
```

Duration: 0.0012996000000000119

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
Loading code/barrier1.hco
```

Duration: 0.0013504000000000294

### Current Output

```
nworkers = 16
#states (3614)
3614 components
No issues
Loading code/barrier1.hco
```

Duration: 0.0011854000000000031

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
Loading code/spinlockInv.hco
```

Duration: 0.0012578999999999785

### Current Output

```
nworkers = 16
#states (473)
148 components
No issues
Loading code/spinlockInv.hco
```

Duration: 0.001213500000000034

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
Loading code/bosco2.hco
```

Duration: 0.0012820999999999527

### Current Output

```
nworkers = 16
#states (633)
633 components
No issues
Loading code/bosco2.hco
```

Duration: 0.0011867000000000405

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
Loading code/paxos2.hco
```

Duration: 0.0011924000000000379

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/paxos2.hco
```

Duration: 0.0016866999999999854

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
Loading code/bqueue.hco
```

Duration: 0.0012836999999999987

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/bqueue.hco
```

Duration: 0.0012165000000000092

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
Loading code/hello6.hco
```

Duration: 0.0013195999999999763

### Current Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/hello6.hco
```

Duration: 0.0014331999999999678

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
Loading code/stack1.hco
```

Duration: 0.0011365999999999876

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack1.hco
```

Duration: 0.0012215999999999894

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
Loading code/hello5.hco
```

Duration: 0.0012371999999999939

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hello5.hco
```

Duration: 0.0016147999999999718

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
Loading code/abd.hco
```

Duration: 0.0013388999999999762

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/abd.hco
```

Duration: 0.001346999999999987

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
Loading code/hello8.hco
```

Duration: 0.001141100000000006

### Current Output

```
nworkers = 16
#states (10)
10 components
No issues
Loading code/hello8.hco
```

Duration: 0.001189899999999966

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
Loading code/stack4.hco
```

Duration: 0.001227900000000004

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/stack4.hco
```

Duration: 0.0011767999999999779

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
Loading code/BBhoare.hco
```

Duration: 0.0012051999999999619

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/BBhoare.hco
```

Duration: 0.0012490999999999475

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
Loading code/RWcheat.hco
```

Duration: 0.0011874000000000051

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/RWcheat.hco
```

Duration: 0.0012464999999999837

---
##  code/stacktest.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Can't import module stack from ['code/stacktest.hny'] ErrorToken(line=1, message="Can't import module stack from ['code/stacktest.hny']", column=6, lexeme='stack', filename='code/stacktest.hny', is_eof_error=False)
```

Duration: 0.001020299999999974

### Current Output

```
Line 1:6 at code/stacktest.hny, Can't import module stack from ['code/stacktest.hny']
```

Duration: 0.0009290000000000131

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
Loading code/queueMS.hco
```

Duration: 0.0015491000000000255

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queueMS.hco
```

Duration: 0.0016639999999999988

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
Loading code/abdtest.hco
```

Duration: 0.0012151000000000245

### Current Output

```
nworkers = 16
#states (148)
148 components
No issues
Loading code/abdtest.hco
```

Duration: 0.0012029000000000067

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
Loading code/locksusp.hco
```

Duration: 0.0012105000000000032

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/locksusp.hco
```

Duration: 0.001368299999999989

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
Load: unknown address ?acquire_wlock[()]
```

Duration: 0.0012660999999999922

### Current Output

```
nworkers = 16
#states (2)
Safety Violation
Loading code/RWbusychk.hco
T0: __init__() [0-3,145-156,147-156,147-156,147-149,157-169,160-169,160-169,160-162,170-174] { RW: () }
Load: unknown address ?acquire_wlock[()]
```

Duration: 0.001103500000000035

---
##  code/2pc1.hny

### Summary

Duration is good: ✅

Output is good: ✅

### Baseline Output

```
Cannot operate on constant ('balance', 'code/2pc1.hny', 16, 21) ErrorToken(line=16, message="Cannot operate on constant ('balance', 'code/2pc1.hny', 16, 21)", column=29, lexeme='-=', filename='code/2pc1.hny', is_eof_error=False)
```

Duration: 0.0009908999999999613

### Current Output

```
Line 16:29 at code/2pc1.hny, Cannot operate on constant ('balance', 'code/2pc1.hny', 16, 21)
```

Duration: 0.0008952999999999878

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
Harmony assertion failed
```

Duration: 0.0015988000000000113

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
Harmony assertion failed
```

Duration: 0.0017459999999999698

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
Loading code/linkedlist.hco
```

Duration: 0.0014167000000000485

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/linkedlist.hco
```

Duration: 0.001376199999999994

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
Loading code/barriertest2.hco
```

Duration: 0.001379100000000022

### Current Output

```
nworkers = 16
#states (6272)
6272 components
No issues
Loading code/barriertest2.hco
```

Duration: 0.0014314999999999745

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
Loading code/oo.hco
```

Duration: 0.0015826999999999924

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/oo.hco
```

Duration: 0.0012271999999999839

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
Loading code/queuefix.hco
```

Duration: 0.0014725000000000432

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queuefix.hco
```

Duration: 0.0012815999999999939

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
Loading code/hello3.hco
```

Duration: 0.0011126000000000191

### Current Output

```
nworkers = 16
#states (3)
3 components
No issues
Loading code/hello3.hco
```

Duration: 0.0011799999999999589

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
Loading code/queueseq.hco
```

Duration: 0.0013889000000000262

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/queueseq.hco
```

Duration: 0.0011856999999999562

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
Loading code/hello1.hco
```

Duration: 0.001135499999999956

### Current Output

```
nworkers = 16
#states (2)
2 components
No issues
Loading code/hello1.hco
```

Duration: 0.0012360999999999622

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
Loading code/consensus.hco
```

Duration: 0.001369100000000012

### Current Output

```
nworkers = 16
#states (4540)
4540 components
No issues
Loading code/consensus.hco
```

Duration: 0.001287499999999997

---