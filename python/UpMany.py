import threading

N = 10000000
count = 0
done = [ False, False ]

def incrementer(self):
    global count
    for i in range(N):
        count = count + 1
    done[self] = True

def main():
    while not all(done):
        pass
    assert count == 2*N, count
    print("Done")

def spawn(f, a):
    threading.Thread(target=f, args=a).start()

spawn(incrementer, (0,))
spawn(incrementer, (1,))
spawn(main, ())
