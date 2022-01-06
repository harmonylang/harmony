# Integration Test Results

---
### code/prog1.hny

Average duration: 0.42333221435546875

Expected output:
```
nworkers = 16
#states 2 (time 0.001+0.000)
2 components
No issues
Loading code/prog1.hco
```

---
### code/prog2.hny

Average duration: 0.411318302154541

Expected output:
```
nworkers = 16
#states 11 (time 0.002+0.000)
Safety Violation
Loading code/prog2.hco
T0: __init__() [0-3,17-25] { shared: True }
T2: g() [13-16] { shared: False }
T1: f() [4-8] { shared: False }
Harmony assertion failed
```

---
### code/Up.hny

Average duration: 0.4696049690246582

Expected output:
```
nworkers = 16
#states 44 (time 0.005+0.000)
Safety Violation
Loading code/Up.hco
T0: __init__() [0-5,35-43] { count: 0, done: [ False, False ] }
T2: incrementer(1) [6-9] { count: 0, done: [ False, False ] }
T1: incrementer(0) [6-20] { count: 1, done: [ True, False ] }
T2: incrementer(1) [10-24,26-31] { count: 1, done: [ True, True ] }
Harmony assertion failed
```

---
### code/UpEnter.hny

Average duration: 0.48082423210144043

Expected output:
```
nworkers = 16
#states 60 (time 0.009+0.000)
60 components
Non-terminating state
Loading code/UpEnter.hco
T0: __init__() [0-7,58-66] { count: 0, done: [ False, False ], entered: [ False, False ] }
T2: incrementer(1) [8-18] { count: 0, done: [ False, False ], entered: [ False, True ] }
T1: incrementer(0) [8-25] { count: 0, done: [ False, False ], entered: [ True, True ] }
T2: incrementer(1) [19-25] { count: 0, done: [ False, False ], entered: [ True, True ] }

```

---
### code/csbarebones.hny

Average duration: 0.4334714412689209

Expected output:
```
nworkers = 16
#states 5 (time 0.002+0.000)
Safety Violation
Loading code/csbarebones.hco
T0: __init__() [0,1,18-26] { }
T1: thread() [2-4] { }
T2: thread() [2-4] { }
T1: thread() [5-12] { }
Harmony assertion failed
```

---
### code/cs.hny

Average duration: 0.43940114974975586

Expected output:
```
nworkers = 16
#states 11 (time 0.004+0.000)
Safety Violation
Loading code/cs.hco
T0: __init__() [0,1,19-27] { }
T1: thread() [2-4(choose True),5] { }
T2: thread() [2-4(choose True),5] { }
T1: thread() [6-13] { }
Harmony assertion failed
```

---
### code/naiveLock.hny

Average duration: 0.4581570625305176

Expected output:
```
nworkers = 16
#states 49 (time 0.008+0.000)
Safety Violation
Loading code/naiveLock.hco
T0: __init__() [0-3,31-39] { lockTaken: False }
T2: thread(1) [4-7(choose True),8-12,14] { lockTaken: False }
T1: thread(0) [4-7(choose True),8-12,14,15] { lockTaken: True }
T2: thread(1) [15-23] { lockTaken: True }
Harmony assertion failed
```

---
### code/naiveFlags.hny

Average duration: 0.49667859077453613

Expected output:
```
nworkers = 16
#states 45 (time 0.004+0.000)
15 components
Non-terminating state
Loading code/naiveFlags.hco
T0: __init__() [0-3,42-50] { flags: [ False, False ] }
T2: thread(1) [4-6(choose True),7-17] { flags: [ False, True ] }
T1: thread(0) [4-6(choose True),7-17] { flags: [ True, True ] }

```

---
### code/naiveTurn.hny

Average duration: 0.9538962841033936

Expected output:
```
nworkers = 16
#states 28 (time 0.006+0.000)
21 components
Non-terminating state
Loading code/naiveTurn.hco
T0: __init__() [0-3,32-40] { turn: 0 }
T1: thread(0) [4-6(choose True),7-11] { turn: 1 }
T2: thread(1) [4-6(choose False),7,30,31] { turn: 1 }

```

---
### code/Peterson.hny

Average duration: 1.5986309051513672

Expected output:
```
nworkers = 16
#states 104 (time 0.009+0.000)
37 components
No issues
Loading code/Peterson.hco
```

---
### code/PetersonInductive.hny

Average duration: 1.437129259109497

Expected output:
```
nworkers = 16
#states 104 (time 0.010+0.001)
37 components
No issues
Loading code/PetersonInductive.hco
```

---
### code/csonebit.hny

Average duration: 1.6532816886901855

Expected output:
```
nworkers = 16
#states 73 (time 0.009+0.000)
18 components
Active busy waiting
Loading code/csonebit.hco
T0: __init__() [0-5,52-60] { flags: [ False, False ] }
T2: thread(1) [6-8(choose True),9-19] { flags: [ False, True ] }
T1: thread(0) [6-8(choose True),9-19] { flags: [ True, True ] }

```

---
### code/PetersonMethod.hny

Average duration: 1.6807661056518555

Expected output:
```
nworkers = 16
#states 104 (time 0.010+0.000)
37 components
No issues
Loading code/PetersonMethod.hco
```

---
### code/spinlock.hny

Average duration: 1.5738370418548584

Expected output:
```
nworkers = 16
#states 473 (time 0.016+0.001)
148 components
No issues
Loading code/spinlock.hco
```

---
### code/csTAS.hny

Average duration: 0.2909064292907715

Expected output:
```
harmony: error: file named 'code/csTAS.hny' does not exist.
```

---
### code/UpLock.hny

Average duration: 2.264772415161133

Expected output:
```
nworkers = 16
#states 57 (time 0.016+0.000)
57 components
No issues
Loading code/UpLock.hco
```

---
### -msynch=synchS code/UpLock.hny

Average duration: 1.9711027145385742

Expected output:
```
nworkers = 16
#states 59 (time 0.011+0.000)
59 components
No issues
Loading code/UpLock.hco
```

---
### code/xy.hny

Average duration: 1.6501858234405518

Expected output:
```
nworkers = 16
#states 20 (time 0.004+0.000)
Safety Violation
Loading code/xy.hco
T0: __init__() [0-9,54-62] { x: 0, y: 100 }
T2: setX(50) [10-16] { x: 50, y: 100 }
T1: checker() [32-35,20-30,36-50] { x: 50, y: 100 }
Harmony assertion failed: (50, 100)
```

---
### code/atm.hny

Average duration: 2.484768867492676

Expected output:
```
nworkers = 16
#states 4110 (time 0.102+0.006)
Invariant Violation
Loading code/atm.hco
T0: __init__() [0-5,369-371,1039-1054,766-770,759-764,771,772,1055-1058(choose 1),1059-1062,1044-1054,766-770,759-764,771,772,1055-1058(choose 0),1059-1062,1044-1046,1063-1066,1094,1183-1197(choose 0),1198-1201(choose 1),1202-1205,1185-1197(choose 0),1198-1201(choose 1),1202-1205,1185-1187,1206,1207] { accounts: [ { "balance": 1, "lock": False }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }
T2: customer(2, 0, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-785] { accounts: [ { "balance": 1, "lock": False }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }
T1: customer(1, 0, 1) [1157-1161,1095-1103,782-789,793-799,1104-1119,801-815,1120,1121,1162-1178,1123-1131,782-789,793-799,1132-1153,801-815,1154,1155,1179-1182] { accounts: [ { "balance": 0, "lock": False }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }
T2: customer(2, 0, 1) [786-789,793-799,1132-1153,801-804] { accounts: [ { "balance": -1, "lock": True }, { "balance": 0, "lock": False } ], bag: (), list: (), synch: () }

```

---
### code/queuedemo.hny

Average duration: 1.8059873580932617

Expected output:
```
nworkers = 16
#states 80 (time 0.010+0.001)
80 components
No issues
Loading code/queuedemo.hco
```

---
### -msynch=synchS code/queuedemo.hny

Average duration: 1.7955279350280762

Expected output:
```
nworkers = 16
#states 80 (time 0.008+0.000)
80 components
No issues
Loading code/queuedemo.hco
```

---
### code/qtestseq.hny

Average duration: 2.3205618858337402

Expected output:
```
nworkers = 16
#states 600 (time 0.014+0.003)
600 components
No issues
Loading code/qtestseq.hco
```

---
### code/qtest1.hny

Average duration: 1.7567479610443115

Expected output:
```
nworkers = 16
#states 274 (time 0.011+0.001)
274 components
No issues
Loading code/qtest1.hco
```

---
### -msynch=synchS code/qtest1.hny

Average duration: 1.8086047172546387

Expected output:
```
nworkers = 16
#states 274 (time 0.010+0.001)
274 components
No issues
Loading code/qtest1.hco
```

---
### code/qtest2.hny

Average duration: 1.7564477920532227

Expected output:
```
nworkers = 16
#states 55 (time 0.015+0.001)
55 components
No issues
Loading code/qtest2.hco
```

---
### -msynch=synchS code/qtest2.hny

Average duration: 1.8700048923492432

Expected output:
```
nworkers = 16
#states 55 (time 0.014+0.001)
55 components
No issues
Loading code/qtest2.hco
```

---
### code/qtest4.hny

Average duration: 1.630185604095459

Expected output:
```
nworkers = 16
#states 10 (time 0.005+0.000)
10 components
No issues
Loading code/qtest4.hco
```

---
### -mqueue=queueMS code/queuedemo.hny

Average duration: 2.658066511154175

Expected output:
```
nworkers = 16
#states 3125 (time 0.045+0.011)
3125 components
No issues
Loading code/queuedemo.hco
```

---
### -mqueue=queueMS -msynch=synchS code/queuedemo.hny

Average duration: 2.318704843521118

Expected output:
```
nworkers = 16
#states 3287 (time 0.039+0.009)
3287 components
No issues
Loading code/queuedemo.hco
```

---
### code/lltest.hny

Average duration: 2.130471706390381

Expected output:
```
nworkers = 16
#states 2 (time 0.001+0.000)
Safety Violation
Loading code/lltest.hco
T0: __init__() [0-7,371-373,1041-1047,1331-1334] { alloc: { "next": 0, "pool": () }, bag: (), linkedlist: (), list: (), synch: () }
Load: unknown address ?LinkedList[()]
```

---
### -msynch=synchS code/lltest.hny

Average duration: 2.2518246173858643

Expected output:
```
nworkers = 16
#states 2 (time 0.001+0.000)
Safety Violation
Loading code/lltest.hco
T0: __init__() [0-7,801-807,1091-1094] { alloc: { "next": 0, "pool": () }, linkedlist: (), list: (), synch: () }
Load: unknown address ?LinkedList[()]
```

---
### code/RWtest.hny

Average duration: 1.4946441650390625

Expected output:
```
nworkers = 16
#states 135 (time 0.015+0.001)
27 components
No issues
Loading code/RWtest.hco
```

---
### -msynch=synchS code/RWtest.hny

Average duration: 1.273233413696289

Expected output:
```
nworkers = 16
#states 135 (time 0.012+0.001)
27 components
No issues
Loading code/RWtest.hco
```

---
### -mRW=RWsbs code/RWtest.hny

Average duration: 2.724811553955078

Expected output:
```
nworkers = 16
#states 1943 (time 0.044+0.004)
619 components
No issues
Loading code/RWtest.hco
```

---
### -mRW=RWsbs -msynch=synchS code/RWtest.hny

Average duration: 2.2352519035339355

Expected output:
```
nworkers = 16
#states 4212 (time 0.046+0.007)
897 components
No issues
Loading code/RWtest.hco
```

---
### -mRW=RWfair code/RWtest.hny

Average duration: 2.0847527980804443

Expected output:
```
nworkers = 16
#states 1438 (time 0.035+0.002)
449 components
No issues
Loading code/RWtest.hco
```

---
### -mRW=RWfair -msynch=synchS code/RWtest.hny

Average duration: 2.3165173530578613

Expected output:
```
nworkers = 16
#states 3137 (time 0.037+0.005)
635 components
No issues
Loading code/RWtest.hco
```

---
### code/BBhoaretest.hny

Average duration: 0.2996859550476074

Expected output:
```
harmony: error: file named 'code/BBhoaretest.hny' does not exist.
```

---
### -msynch=synchS code/BBhoaretest.hny

Average duration: 0.2860832214355469

Expected output:
```
harmony: error: file named 'code/BBhoaretest.hny' does not exist.
```

---
### -mRW=RWcv code/RWtest.hny

Average duration: 2.6327157020568848

Expected output:
```
nworkers = 16
#states 1902 (time 0.077+0.004)
406 components
No issues
Loading code/RWtest.hco
```

---
### -mRW=RWcv -msynch=synchS code/RWtest.hny

Average duration: 2.3571035861968994

Expected output:
```
nworkers = 16
#states 4301 (time 0.048+0.007)
666 components
No issues
Loading code/RWtest.hco
```

---
### code/qsorttest.hny

Average duration: 2.0118608474731445

Expected output:
```
nworkers = 16
#states 454 (time 0.010+0.001)
454 components
No issues
Loading code/qsorttest.hco
```

---
### code/Diners.hny

Average duration: 2.418895721435547

Expected output:
```
nworkers = 16
#states 23905 (time 0.049+0.076)
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

---
### -msynch=synchS code/Diners.hny

Average duration: 2.5911693572998047

Expected output:
```
nworkers = 16
#states 32476 (time 0.081+0.129)
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

---
### code/DinersAvoid.hny

Average duration: 7.234955549240112

Expected output:
```
nworkers = 16
#states 86214 (time 0.300+0.267)
5589 components
No issues
Loading code/DinersAvoid.hco
```

---
### code/bank.hny

Average duration: 2.17228102684021

Expected output:
```
nworkers = 16
#states 3359 (time 0.020+0.004)
3359 components
Non-terminating state
Loading code/bank.hco
T0: __init__() [0-5,369-371,1039-1054,766-770,759-764,771,772,1055-1058(choose 2),1059-1062,1044-1054,766-770,759-764,771,772,1055-1058(choose 2),1059-1062,1044-1046,1063-1066,1170-1181,1172-1181,1172-1174,1182,1183] { accounts: [ { "balance": 2, "lock": False }, { "balance": 2, "lock": False } ], bag: (), list: (), synch: () }
T1: thread() [1142-1144(choose 0),1145-1151(choose 1),1152-1165(choose 1),1166,1167,1067-1075,782-789,793-799,1076-1102,782-785] { accounts: [ { "balance": 1, "lock": True }, { "balance": 2, "lock": False } ], bag: (), list: (), synch: () }
T2: thread() [1142-1144(choose 1),1145-1151(choose 0),1152-1165(choose 2),1166,1167,1067-1075,782-789,793-799,1076-1102,782-785] { accounts: [ { "balance": 1, "lock": True }, { "balance": 0, "lock": True } ], bag: (), list: (), synch: () }

```

---
### code/counter.hny

Average duration: 2.4341418743133545

Expected output:
```
nworkers = 16
#states 601 (time 0.020+0.002)
601 components
No issues
Loading code/counter.hco
```

---
### code/qbarrier.hny

Average duration: 2.3117570877075195

Expected output:
```
nworkers = 16
#states 1664 (time 0.046+0.005)
1664 components
No issues
Loading code/qbarrier.hco
```

---
### -msynch=synchS code/qbarrier.hny

Average duration: 2.4962146282196045

Expected output:
```
nworkers = 16
#states 4927 (time 0.116+0.019)
4927 components
No issues
Loading code/qbarrier.hco
```

---
### code/barriertest.hny

Average duration: 2.4356768131256104

Expected output:
```
nworkers = 16
#states 2802 (time 0.086+0.008)
2802 components
No issues
Loading code/barriertest.hco
```

---
### -msynch=synchS code/barriertest.hny

Average duration: 2.5073978900909424

Expected output:
```
nworkers = 16
#states 7425 (time 0.092+0.014)
7425 components
No issues
Loading code/barriertest.hco
```

---
### code/trap.hny

Average duration: 1.416321039199829

Expected output:
```
nworkers = 16
#states 3 (time 0.002+0.000)
3 components
Non-terminating state
Loading code/trap.hco
T0: __init__() [0-7,34-38] { count: 0, done: False }
T1: main() [17-20] { count: 0, done: False }

```

---
### code/trap2.hny

Average duration: 0.3404374122619629

Expected output:
```
Line 1:5 at code/trap2.hny, constant cannot be an lvalue: ('ok', 'code/trap2.hny', 4, 19)

```

---
### code/trap3.hny

Average duration: 2.094348907470703

Expected output:
```
nworkers = 16
#states 4 (time 0.002+0.000)
Safety Violation
Loading code/trap3.hco
T0: __init__() [0-5,369-371,1039-1043,766-770,759-764,771,772,1044-1049,1096-1100] { bag: (), count: 0, countlock: False, done: False, list: (), synch: () }
T1: main() [1067-1073,782-789,793-799,1074] { bag: (), count: 0, countlock: True, done: False, list: (), synch: () }

```

---
### code/trap4.hny

Average duration: 1.1638460159301758

Expected output:
```
nworkers = 16
#states 5 (time 0.003+0.000)
5 components
Non-terminating state
Loading code/trap4.hco
T0: __init__() [0-7,44-48] { count: 0, done: False }
T1: main() [17-30] { count: 1, done: False }

```

---
### code/trap5.hny

Average duration: 1.527555227279663

Expected output:
```
nworkers = 16
#states 5 (time 0.003+0.000)
5 components
Non-terminating state
Loading code/trap5.hco
T0: __init__() [0-7,52-56] { count: 0, done: False }
T1: main() [31-37,8-20,38] { count: 1, done: False }

```

---
### code/trap6.hny

Average duration: 2.1372439861297607

Expected output:
```
nworkers = 16
#states 34 (time 0.009+0.000)
34 components
Non-terminating state
Loading code/trap6.hco
T0: __init__() [0-5,369-371,1039-1045,766-770,759-764,771,772,1046-1049,1109-1117] { bag: (), count: 0, countlock: False, done: [ False, False ], list: (), synch: () }
T1: thread(0) [1085-1092,1050-1056,782-789,793-799,1057-1064,801-815,1065-1070,1093] { bag: (), count: 1, countlock: False, done: [ False, False ], list: (), synch: () }
T2: thread(1) [1085-1092,1050-1056,782-789,793-799,1057-1064,801-815,1065-1070,1093] { bag: (), count: 2, countlock: False, done: [ False, False ], list: (), synch: () }

```

---
### -msynch=synchS code/trap6.hny

Average duration: 1.9558701515197754

Expected output:
```
nworkers = 16
#states 36 (time 0.014+0.000)
36 components
Non-terminating state
Loading code/trap6.hco
T0: __init__() [0-5,799-805,417-421,404-415,422,423,806-809,869-877] { count: 0, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }
T1: thread(0) [845-852,810-816,425-431,455-462,817-824,464-488,508,509,825-830,853] { count: 1, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }
T2: thread(1) [845-852,810-816,425-431,455-462,817-824,464-488,508,509,825-830,853] { count: 2, countlock: { "acquired": False, "suspended": () }, done: [ False, False ], list: (), synch: () }

```

---
### code/hw.hny

Average duration: 2.887232542037964

Expected output:
```
nworkers = 16
#states 23864 (time 0.091+0.133)
18524 components
No issues
Loading code/hw.hco
```

---
### code/abptest.hny

Average duration: 1.691161870956421

Expected output:
```
nworkers = 16
#states 1536 (time 0.079+0.006)
608 components
No issues
Loading code/abptest.hco
```

---
### test/DinersVar.hny

Average duration: 2.5708718299865723

Expected output:
```
nworkers = 16
#states 23905 (time 0.052+0.072)
4285 components
Non-terminating state
Loading test/DinersVar.hco
T0: __init__() [0-5,369-371,1039-1043,766-770,759-764,771,772,1044-1048,1094-1105,1096-1105,1096-1105,1096-1105,1096-1105,1096-1098,1106,1107] { bag: (), forks: [ False, False, False, False, False ], list: (), synch: () }
T3: diner(2) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ False, False, True, False, False ], list: (), synch: () }
T1: diner(0) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, False, False ], list: (), synch: () }
T5: diner(4) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, False, True ], list: (), synch: () }
T4: diner(3) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, False, True, True, True ], list: (), synch: () }
T2: diner(1) [1049-1064(choose True),1065-1070,782-789,793-799,1071-1076,782-785] { bag: (), forks: [ True, True, True, True, True ], list: (), synch: () }

```

---