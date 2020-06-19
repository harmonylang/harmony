import threading

def incrementer(self):
    global count
    count = count + 1
    done[self] = True

def main():
    while not (done[0] and done[1]):
        pass
    assert count == 2, count

def spawn(f, a):
    threading.Thread(target=f, args=a).start()

count = 0
done = [ False, False ]
spawn(incrementer, (0,))
spawn(incrementer, (1,))
spawn(main, ())
