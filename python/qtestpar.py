import queue, threading, random

NOPS = 4
q = queue.Queue()

def put_test(self):
    print("call put", self)
    q.put(self)
    print("done put", self)

def get_test(self):
    print("call get", self)
    try:
        v = q.get(block=False)
        print("done get", self, v)
    except queue.Empty:
        print("done get empty", self)

nputs = random.randint(1, NOPS - 1)
for i in range(nputs):
    threading.Thread(target=put_test, args=(i,)).start()
for i in range(NOPS - nputs):
    threading.Thread(target=get_test, args=(i,)).start()
