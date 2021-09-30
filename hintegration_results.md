# Integration Test Results

---
### code/prog1.hny

Average duration: 0.19326603412628174

Expected output:
```
#states 2
2 components, 0 bad states
No issues
```

---
### code/prog2.hny

Average duration: 0.14266810417175294

Expected output:
```
#states 10
Safety Violation
T0: __init__() [0-3,17-25] { shared: True }
T1: g() [13-16] { shared: False }
T2: f() [4-8] { shared: False }
Harmony assertion failed
```

---
### code/Up.hny

Average duration: 0.1477525234222412

Expected output:
```
#states 44
Safety Violation
T0: __init__() [0-5,33-41] { count: 0, done: [ False, False ] }
T1: incrementer(0) [6-9] { count: 0, done: [ False, False ] }
T2: incrementer(1) [6-20] { count: 1, done: [ False, True ] }
T1: incrementer(0) [10-29] { count: 1, done: [ True, True ] }
Harmony assertion failed
```

---
### code/UpEnter.hny

Average duration: 0.15733299255371094

Expected output:
```
#states 60
60 components, 1 bad states
Non-terminating state
T0: __init__() [0-7,55-63] { count: 0, done: [ False, False ], entered: [ False, False ] }
T1: incrementer(0) [8-18] { count: 0, done: [ False, False ], entered: [ True, False ] }
T2: incrementer(1) [8-25] { count: 0, done: [ False, False ], entered: [ True, True ] }
T1: incrementer(0) [19-25] { count: 0, done: [ False, False ], entered: [ True, True ] }

```

---
### code/csbarebones.hny

Average duration: 0.14854893684387208

Expected output:
```
#states 7
Safety Violation
T0: __init__() [0,1,28-36] { }
T1: thread(0) [2-4] { }
T2: thread(1) [2-21] { }
Harmony assertion failed
```

---
### code/cs.hny

Average duration: 0.15816910266876222

Expected output:
```
#states 17
Safety Violation
T0: __init__() [0,1,29-37] { }
T1: thread(0) [2-4(choose True),5] { }
T2: thread(1) [2-4(choose True),5-22] { }
Harmony assertion failed
```

---
### code/naiveLock.hny

Average duration: 0.14987118244171144

Expected output:
```
#states 49
Safety Violation
T0: __init__() [0-3,37-45] { lockTaken: False }
T1: thread(0) [4-6(choose True),7-10] { lockTaken: False }
T2: thread(1) [4-6(choose True),7-11] { lockTaken: True }
T1: thread(0) [11-28] { lockTaken: True }
Harmony assertion failed
```

---
### code/naiveFlags.hny

Average duration: 0.15049197673797607

Expected output:
```
#states 45
15 components, 1 bad states
Non-terminating state
T0: __init__() [0-3,48-56] { flags: [ False, False ] }
T1: thread(0) [4-6(choose True),7-17] { flags: [ True, False ] }
T2: thread(1) [4-6(choose True),7-17] { flags: [ True, True ] }

```

---
### code/naiveTurn.hny

Average duration: 0.1654672861099243

Expected output:
```
#states 28
21 components, 2 bad states
Non-terminating state
T0: __init__() [0-3,39-47] { turn: 0 }
T1: thread(0) [4-6(choose True),7-11] { turn: 1 }
T2: thread(1) [4-6(choose False),7,37,38] { turn: 1 }

```

---
### code/Peterson.hny

Average duration: 0.16028890609741211

Expected output:
```
#states 104
37 components, 0 bad states
No issues
```

---
### code/PetersonInductive.hny

Average duration: 0.16164054870605468

Expected output:
```
#states 104
37 components, 0 bad states
No issues
```

---
### code/csonebit.hny

Average duration: 0.18033347129821778

Expected output:
```
#states 73
18 components, 0 bad states
Active busy waiting
T0: __init__() [0-5,61-69] { flags: [ False, False ] }
T1: thread(0) [6-8(choose True),9-19] { flags: [ True, False ] }
T2: thread(1) [6-8(choose True),9-19] { flags: [ True, True ] }

```

---
### code/PetersonMethod.hny

Average duration: 0.1607203722000122

Expected output:
```
#states 104
37 components, 0 bad states
No issues
```

---
### code/spinlock.hny

Average duration: 0.15589530467987062

Expected output:
```
#states 401
124 components, 0 bad states
No issues
```

---
### code/csTAS.hny

Average duration: 0.14212350845336913

Expected output:
```
#states 322
157 components, 0 bad states
No issues
```

---
### code/UpLock.hny

Average duration: 0.30850508213043215

Expected output:
```
#states 49
49 components, 0 bad states
No issues
```

---
### -msynch=synchS code/UpLock.hny

Average duration: 0.258350133895874

Expected output:
```
#states 59
59 components, 0 bad states
No issues
```

---
### code/xy.hny

Average duration: 0.14911892414093017

Expected output:
```
#states 19
Safety Violation
T0: __init__() [0-9,54-62] { x: 0, y: 100 }
T1: setX(50) [10-16] { x: 50, y: 100 }
T2: checker() [32-35,20-30,36-50] { x: 50, y: 100 }
Harmony assertion failed: (50, 100)
```

---
### code/atm.hny

Average duration: 0.3779441356658936

Expected output:
```
#states 2885
Invariant Violation
T0: __init__() [0-5,369-371,1047-1062,769-773,762-767,774,775,1063-1066(choose 0),1067-1070,1052-1062,769-773,762-767,774,775,1063-1066(choose 1),1067-1070,1052-1054,1071-1074,1101,1191-1205(choose 1),1206-1209(choose 1),1210-1213,1193-1205(choose 1),1206-1209(choose 1),1210-1213,1193-1195,1214,1215] { accounts: [ { .balance: 0, .lock: False }, { .balance: 1, .lock: False } ], bag: (), list: (), synch: () }
T1: customer(1, 1, 1) [1164-1168,1102-1110,785-788,727-738,789-791,1111-1126,793-807,1127,1128,1169-1185,1130-1138,785-788,727-730] { accounts: [ { .balance: 0, .lock: False }, { .balance: 1, .lock: False } ], bag: (), list: (), synch: () }
T2: customer(2, 1, 1) [1164-1168,1102-1110,785-788,727-738,789-791,1111-1126,793-807,1127,1128,1169-1185,1130-1138,785-788,727-738,789-791,1139-1160,793-807,1161,1162,1186-1190] { accounts: [ { .balance: 0, .lock: False }, { .balance: 0, .lock: False } ], bag: (), list: (), synch: () }
T1: customer(1, 1, 1) [731-738,789-791,1139-1160,793-797] { accounts: [ { .balance: 0, .lock: False }, { .balance: -1, .lock: True } ], bag: (), list: (), synch: () }

```

---
### code/queuedemo.hny

Average duration: 0.3909579038619995

Expected output:
```
#states 912
912 components, 0 bad states
No issues
```

---
### -msynch=synchS code/queuedemo.hny

Average duration: 0.3242910623550415

Expected output:
```
#states 1998
1998 components, 0 bad states
No issues
```

---
### code/qtestseq.hny

Average duration: 0.35657336711883547

Expected output:
```
#states 600
600 components, 0 bad states
No issues
```

---
### code/qtest1.hny

Average duration: 0.37526867389678953

Expected output:
```
#states 5058
5058 components, 0 bad states
No issues
```

---
### -msynch=synchS code/qtest1.hny

Average duration: 0.33595943450927734

Expected output:
```
#states 7218
7218 components, 0 bad states
No issues
```

---
### code/qtest2.hny

Average duration: 0.3470431327819824

Expected output:
```
#states 219
219 components, 0 bad states
No issues
```

---
### -msynch=synchS code/qtest2.hny

Average duration: 0.32375731468200686

Expected output:
```
#states 309
309 components, 0 bad states
No issues
```

---
### code/qtest4.hny

Average duration: 0.41494390964508054

Expected output:
```
#states 122
122 components, 0 bad states
No issues
```

---
### -mqueue=queueMS code/queuedemo.hny

Average duration: 0.43009965419769286

Expected output:
```
#states 2095
2095 components, 0 bad states
Data race (?alloc.pool[0].next)
T0: __init__() [0-7,371-373,1049-1055,1254-1256,1096-1100,1056-1074,1101-1113,771-775,764-769,776,777,1114-1118,771-775,764-769,776,777,1119-1121,1257-1286] { alloc: { .next: 1, .pool: [ { .next: None, .value: () } ] }, bag: (), demoq: { .hdlock: False, .head: ?alloc.pool[0], .tail: ?alloc.pool[0], .tllock: False }, list: (), queue: (), synch: () }
T3: sender(?demoq, 1) [1223-1234,1123-1133,1056-1074,1134-1139,787-790,729-740,791-793,1140-1147] { alloc: { .next: 2, .pool: [ { .next: None, .value: () }, { .next: None, .value: 1 } ] }, bag: (), demoq: { .hdlock: False, .head: ?alloc.pool[0], .tail: ?alloc.pool[0], .tllock: True }, list: (), queue: (), synch: () }
T1: receiver(?demoq) [1238-1242,1164-1170,787-790,729-740,791-793,1171-1179] { alloc: { .next: 2, .pool: [ { .next: None, .value: () }, { .next: None, .value: 1 } ] }, bag: (), demoq: { .hdlock: True, .head: ?alloc.pool[0], .tail: ?alloc.pool[0], .tllock: True }, list: (), queue: (), synch: () }

```

---
### -mqueue=queueMS -msynch=synchS code/queuedemo.hny

Average duration: 0.35074625015258787

Expected output:
```
#states 3287
3287 components, 0 bad states
Data race (?alloc.pool[0].next)
T0: __init__() [0-7,805-811,1010-1012,852-856,812-830,857-869,420-424,407-418,425,426,870-874,420-424,407-418,425,426,875-877,1013-1042] { alloc: { .next: 1, .pool: [ { .next: None, .value: () } ] }, demoq: { .hdlock: { .acquired: False, .suspended: () }, .head: ?alloc.pool[0], .tail: ?alloc.pool[0], .tllock: { .acquired: False, .suspended: () } }, list: (), queue: (), synch: () }
T3: sender(?demoq, 1) [979-990,879-889,812-830,890-895,428-434,458-465,896-903] { alloc: { .next: 2, .pool: [ { .next: None, .value: () }, { .next: None, .value: 1 } ] }, demoq: { .hdlock: { .acquired: False, .suspended: () }, .head: ?alloc.pool[0], .tail: ?alloc.pool[0], .tllock: { .acquired: True, .suspended: () } }, list: (), queue: (), synch: () }
T1: receiver(?demoq) [994-998,920-926,428-434,458-465,927-935] { alloc: { .next: 2, .pool: [ { .next: None, .value: () }, { .next: None, .value: 1 } ] }, demoq: { .hdlock: { .acquired: True, .suspended: () }, .head: ?alloc.pool[0], .tail: ?alloc.pool[0], .tllock: { .acquired: True, .suspended: () } }, list: (), queue: (), synch: () }

```

---
### code/lltest.hny

Average duration: 0.4619007587432861

Expected output:
```
#states 9498
9498 components, 0 bad states
No issues
```

---
### -msynch=synchS code/lltest.hny

Average duration: 0.4981526374816895

Expected output:
```
#states 18377
18377 components, 0 bad states
No issues
```

---
### code/RWtest.hny

Average duration: 0.3037494897842407

Expected output:
```
#states 949
258 components, 0 bad states
Active busy waiting
T0: __init__() [0-7,371-373,1201-1203,1050-1056,771-775,764-769,776,777,1057-1065,1204,1205,1263-1274,1265-1274,1265-1274,1265-1267,1275,1276] { RW: (), bag: (), list: (), rw: { .lock: False, .nreaders: 0, .nwriters: 0 }, synch: () }
T1: thread() [1206-1208(choose True),1209-1211(choose .read),1212-1217,1067-1072,787-790,729-740,791-793,1073-1080,1094-1107,795-809,1108,1109,1218] { RW: (), bag: (), list: (), rw: { .lock: False, .nreaders: 1, .nwriters: 0 }, synch: () }
T2: thread() [1206-1208(choose True),1209-1211(choose .write),1212-1214,1235-1237,1135-1140,787-790,729-740,791-793,1141-1144] { RW: (), bag: (), list: (), rw: { .lock: True, .nreaders: 1, .nwriters: 0 }, synch: () }

```

---
### -msynch=synchS code/RWtest.hny

Average duration: 0.26844801902771

Expected output:
```
#states 2735
452 components, 0 bad states
Active busy waiting
T0: __init__() [0-7,957-959,806-812,420-424,407-418,425,426,813-821,960,961,1019-1030,1021-1030,1021-1030,1021-1023,1031,1032] { RW: (), list: (), rw: { .lock: { .acquired: False, .suspended: () }, .nreaders: 0, .nwriters: 0 }, synch: () }
T1: thread() [962-964(choose True),965-967(choose .read),968-973,823-828,428-434,458-465,829-836,850-863,467-491,511,512,864,865,974] { RW: (), list: (), rw: { .lock: { .acquired: False, .suspended: () }, .nreaders: 1, .nwriters: 0 }, synch: () }
T2: thread() [962-964(choose True),965-967(choose .write),968-970,991-993,891-896,428-434,458-465,897-900] { RW: (), list: (), rw: { .lock: { .acquired: True, .suspended: () }, .nreaders: 1, .nwriters: 0 }, synch: () }

```

---
### -mRW=RWsbs code/RWtest.hny

Average duration: 0.3242312431335449

Expected output:
```
#states 1757
558 components, 0 bad states
No issues
```

---
### -mRW=RWsbs -msynch=synchS code/RWtest.hny

Average duration: 0.29497442245483396

Expected output:
```
#states 4212
897 components, 0 bad states
No issues
```

---
### -mRW=RWfair code/RWtest.hny

Average duration: 0.32951064109802247

Expected output:
```
#states 1248
387 components, 0 bad states
No issues
```

---
### -mRW=RWfair -msynch=synchS code/RWtest.hny

Average duration: 0.292344069480896

Expected output:
```
#states 3137
635 components, 0 bad states
No issues
```

---
### code/BBhoaretest.hny

Average duration: 0.3992868423461914

Expected output:
```
#states 1045
1045 components, 0 bad states
No issues
```

---
### -msynch=synchS code/BBhoaretest.hny

Average duration: 0.3493434190750122

Expected output:
```
#states 4127
4127 components, 0 bad states
No issues
```

---
### -mRW=RWcv code/RWtest.hny

Average duration: 0.3205997943878174

Expected output:
```
#states 1673
349 components, 0 bad states
No issues
```

---
### -mRW=RWcv -msynch=synchS code/RWtest.hny

Average duration: 0.2858255624771118

Expected output:
```
#states 4301
666 components, 0 bad states
No issues
```

---
### code/qsorttest.hny

Average duration: 0.27140982151031495

Expected output:
```
#states 454
454 components, 0 bad states
No issues
```

---
### code/Diners.hny

Average duration: 0.3721343755722046

Expected output:
```
#states 9095
1700 components, 1 bad states
Non-terminating state
T0: __init__() [0-5,369-371,1047-1051,769-773,762-767,774,775,1052-1056,1102-1113,1104-1113,1104-1113,1104-1113,1104-1113,1104-1106,1114,1115] { bag: (), forks: [ False, False, False, False, False ], list: (), synch: () }
T1: diner(0) [1057-1072(choose True),1073-1078,785-788,727-738,789-791,1079-1084,785-788,727-730] { bag: (), forks: [ True, False, False, False, False ], list: (), synch: () }
T2: diner(1) [1057-1072(choose True),1073-1078,785-788,727-738,789-791,1079-1084,785-788,727-730] { bag: (), forks: [ True, True, False, False, False ], list: (), synch: () }
T3: diner(2) [1057-1072(choose True),1073-1078,785-788,727-738,789-791,1079-1084,785-788,727-730] { bag: (), forks: [ True, True, True, False, False ], list: (), synch: () }
T4: diner(3) [1057-1072(choose True),1073-1078,785-788,727-738,789-791,1079-1084,785-788,727-730] { bag: (), forks: [ True, True, True, True, False ], list: (), synch: () }
T5: diner(4) [1057-1072(choose True),1073-1078,785-788,727-738,789-791,1079-1084,785-788,727-730] { bag: (), forks: [ True, True, True, True, True ], list: (), synch: () }

```

---
### -msynch=synchS code/Diners.hny

Average duration: 0.6538099050521851

Expected output:
```
#states 32476
6416 components, 1 bad states
Non-terminating state
T0: __init__() [0-5,803-807,418-422,405-416,423,424,808-812,858-869,860-869,860-869,860-869,860-869,860-862,870,871] { forks: [ { .acquired: False, .suspended: () }, { .acquired: False, .suspended: () }, { .acquired: False, .suspended: () }, { .acquired: False, .suspended: () }, { .acquired: False, .suspended: () } ], list: (), synch: () }
T1: diner(0) [813-828(choose True),829-834,426-432,456-463,835-840,426-430] { forks: [ { .acquired: True, .suspended: () }, { .acquired: False, .suspended: () }, { .acquired: False, .suspended: () }, { .acquired: False, .suspended: () }, { .acquired: False, .suspended: () } ], list: (), synch: () }
T5: diner(4) [813-828(choose True),829-834,426-432,456-463,835-840,426-442] { forks: [ { .acquired: True, .suspended: [ CONTEXT(.diner) ] }, { .acquired: False, .suspended: () }, { .acquired: False, .suspended: () }, { .acquired: False, .suspended: () }, { .acquired: True, .suspended: () } ], list: (), synch: () }
T4: diner(3) [813-828(choose True),829-834,426-432,456-463,835-840,426-442] { forks: [ { .acquired: True, .suspended: [ CONTEXT(.diner) ] }, { .acquired: False, .suspended: () }, { .acquired: False, .suspended: () }, { .acquired: True, .suspended: () }, { .acquired: True, .suspended: [ CONTEXT(.diner) ] } ], list: (), synch: () }
T3: diner(2) [813-828(choose True),829-834,426-432,456-463,835-840,426-442] { forks: [ { .acquired: True, .suspended: [ CONTEXT(.diner) ] }, { .acquired: False, .suspended: () }, { .acquired: True, .suspended: () }, { .acquired: True, .suspended: [ CONTEXT(.diner) ] }, { .acquired: True, .suspended: [ CONTEXT(.diner) ] } ], list: (), synch: () }
T2: diner(1) [813-828(choose True),829-834,426-432,456-463,835-840,426-442] { forks: [ { .acquired: True, .suspended: [ CONTEXT(.diner) ] }, { .acquired: True, .suspended: () }, { .acquired: True, .suspended: [ CONTEXT(.diner) ] }, { .acquired: True, .suspended: [ CONTEXT(.diner) ] }, { .acquired: True, .suspended: [ CONTEXT(.diner) ] } ], list: (), synch: () }
T1: diner(0) [431-442] { forks: [ { .acquired: True, .suspended: [ CONTEXT(.diner) ] }, { .acquired: True, .suspended: [ CONTEXT(.diner) ] }, { .acquired: True, .suspended: [ CONTEXT(.diner) ] }, { .acquired: True, .suspended: [ CONTEXT(.diner) ] }, { .acquired: True, .suspended: [ CONTEXT(.diner) ] } ], list: (), synch: () }

```

---
### code/DinersAvoid.hny

Average duration: 0.8372457981109619

Expected output:
```
#states 39884
2129 components, 0 bad states
No issues
```

---
### code/bank.hny

Average duration: 0.3105450630187988

Expected output:
```
#states 2582
2582 components, 9 bad states
Non-terminating state
T0: __init__() [0-5,369-371,1047-1062,769-773,762-767,774,775,1063-1066(choose 1),1067-1070,1052-1062,769-773,762-767,774,775,1063-1066(choose 1),1067-1070,1052-1054,1071-1074,1178-1189,1180-1189,1180-1182,1190,1191] { accounts: [ { .balance: 1, .lock: False }, { .balance: 1, .lock: False } ], bag: (), list: (), synch: () }
T1: thread() [1150-1152(choose 0),1153-1159(choose 1),1160-1173(choose 1),1174,1175,1075-1083,785-788,727-738,789-791,1084-1110,785-788,727-730] { accounts: [ { .balance: 0, .lock: True }, { .balance: 1, .lock: False } ], bag: (), list: (), synch: () }
T2: thread() [1150-1152(choose 1),1153-1159(choose 0),1160-1173(choose 1),1174,1175,1075-1083,785-788,727-738,789-791,1084-1110,785-788,727-730] { accounts: [ { .balance: 0, .lock: True }, { .balance: 0, .lock: True } ], bag: (), list: (), synch: () }

```

---
### code/counter.hny

Average duration: 0.32015578746795653

Expected output:
```
#states 620
620 components, 0 bad states
No issues
```

---
### code/qbarrier.hny

Average duration: 0.3427712440490723

Expected output:
```
#states 2338
2338 components, 0 bad states
No issues
```

---
### -msynch=synchS code/qbarrier.hny

Average duration: 0.42091128826141355

Expected output:
```
#states 6285
6285 components, 0 bad states
No issues
```

---
### code/barriertest.hny

Average duration: 0.3696366548538208

Expected output:
```
#states 6135
6135 components, 0 bad states
No issues
```

---
### -msynch=synchS code/barriertest.hny

Average duration: 0.4256071805953979

Expected output:
```
#states 18741
18741 components, 0 bad states
No issues
```

---
### code/trap.hny

Average duration: 0.13113906383514404

Expected output:
```
#states 9
9 components, 0 bad states
No issues
```

---
### code/trap2.hny

Average duration: 0.13362650871276854

Expected output:
```
#states 23
Safety Violation
T0: __init__() [0-7,36-40] { count: 0, done: False }
T1: main() [17-24,interrupt,8-15,24-32] { count: 1, done: True }
Harmony assertion failed
```

---
### code/trap3.hny

Average duration: 0.27455883026123046

Expected output:
```
#states 11
Safety Violation
T0: __init__() [0-5,369-371,1047-1051,769-773,762-767,774,775,1052-1057,1102-1106] { bag: (), count: 0, countlock: False, done: False, list: (), synch: () }
T1: main() [1075-1081,785-788,727-738,789-791,1082-1089,793-807,1090] { bag: (), count: 1, countlock: False, done: False, list: (), synch: () }

```

---
### code/trap4.hny

Average duration: 0.1375603199005127

Expected output:
```
#states 11
11 components, 0 bad states
No issues
```

---
### code/trap5.hny

Average duration: 0.1361842393875122

Expected output:
```
#states 11
11 components, 0 bad states
No issues
```

---
### code/trap6.hny

Average duration: 0.28180837631225586

Expected output:
```
#states 117
117 components, 0 bad states
No issues
```

---
### -msynch=synchS code/trap6.hny

Average duration: 0.23428306579589844

Expected output:
```
#states 161
161 components, 0 bad states
No issues
```

---
### code/hw.hny

Average duration: 0.3068248987197876

Expected output:
```
#states 15737
13748 components, 0 bad states
No issues
```

---
### code/abptest.hny

Average duration: 0.16082513332366943

Expected output:
```
#states 1536
608 components, 0 bad states
No issues
```

---