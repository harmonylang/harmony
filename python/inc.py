import threading

shared = 0

def f():
    global shared
    shared += 1

t1 = threading.Thread(target=f)
t2 = threading.Thread(target=f)
t1.start()
t2.start()
t1.join()
t2.join()
assert shared == 2
