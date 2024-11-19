import threading

N = 1000
shared = 0

def inc(x):
    return x + 1

def f():
    global shared
    for i in range(N):
        shared = inc(shared)

t1 = threading.Thread(target=f)
t2 = threading.Thread(target=f)
t1.start()
t2.start()
t1.join()
t2.join()
assert shared == 2*N
