import threading
import time


class Thread1(threading.Thread):
    def __init__(self, name, counter, delay):
        super().__init__()
        self.name = name
        self.counter = counter
        self.delay = delay
    
    def run(self):
        self.job(self.counter, self.delay)
    
    def job(self, counter, delay):
        while counter:
            print(self.name)
            threadlock.acquire()
            
            for i in range(10):
                f = open('test.txt', 'a')
                f.write('T1-' + self.name + ' - ' + str(i) + '\n')
                time.sleep(delay)
                f.close()
            
            threadlock.release()
            counter -= 1


class Thread2(threading.Thread):
    def __init__(self, name, counter, delay):
        super().__init__()
        self.name = name
        self.counter = counter
        self.delay = delay
    
    def run(self):
        self.job(self.counter, self.delay)
    
    def job(self, counter, delay):
        while counter:
            print(self.name)
            threadlock.acquire()
            
            for i in range(10):
                f = open('test.txt', 'a')
                f.write('T2-' + self.name + ' - ' + str(i) + '\n')
                time.sleep(delay)
                f.close()
            
            threadlock.release()
            counter -= 1


threadlock = threading.Lock()

t1 = Thread1('t1', 10, 0)
t2 = Thread1('t2', 10, 0)
t3 = Thread1('t3', 10, 0)

t4 = Thread2('t4', 10, 0)
t5 = Thread2('t5', 10, 0)
t6 = Thread2('t6', 10, 0)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
