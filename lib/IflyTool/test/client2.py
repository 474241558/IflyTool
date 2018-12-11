#-*-coding:u8-*-
import time
from multiprocessing.managers import BaseManager
import threading
lock = threading.Lock()
BaseManager.register('get_load_msg_queue')
m = BaseManager(address=('10.1.186.101', 1234), authkey='iflytek')
m.connect()
queue = m.get_load_msg_queue()
count = 0
last_count = 0
thread_num = 5
def fun():
    global queue
    global count
    global last_count
    while(True):
        time.sleep(5)
        print "len:%d"%(queue.qsize())
        print count - last_count
        last_count = count

t = threading.Thread(target=fun)
#t.setDeamon(True)
t.start()

def fun2():
    global queue
    global count
    global lock
    while(True):
        queue.get()
        lock.acquire()
        count+=1
        lock.release()
thread_arr = []

for i in range(thread_num):
    t = threading.Thread(target=fun2)
    t.start()
    thread_arr.append(t)

while(True):
    time.sleep(3600)