#-*-coding:u8-*-
import IflyTool
from IflyTool import DistributedMessageCollection
import sys

def dmc_server(port):
    import time
    ldcs = DistributedMessageCollection('',port,'ldcs.log','pig.log',5)
    ldcs.add_counter("times_a")
    ldcs.add_counter("times_b")
    ldcs.add_counter("times_c")
    ldcs.add_counter("login_resp_time",'t')
    ldcs.add_counter("login_times")
    print "start...."
    time.sleep(3600)
    
def dmc_client(port):
    import time
    from multiprocessing.managers import BaseManager
    import random
    import json

    BaseManager.register('get_msg_queue')
    m = BaseManager(address=('', port), authkey='iflytek')
    m.connect()
    queue = m.get_msg_queue()
    while(True):
        queue.put({"times_a":1})
        queue.put({"times_b":1})
        queue.put({"times_c":1})
        queue.put({"login_resp_time":random.random()})
        queue.put({"login_times":1})
        time.sleep(0.001)
        
def dmc_size(port):
    import time
    from multiprocessing.managers import BaseManager
    import random
    import json

    BaseManager.register('get_msg_queue')
    m = BaseManager(address=('', port), authkey='iflytek')
    m.connect()
    queue = m.get_msg_queue()
    while(True):
        time.sleep(5)
        print "size:"+str(queue.qsize())
        
if __name__ == "__main__":
    if sys.argv[1] == "server":
        dmc_server(int(sys.argv[2]))
    if sys.argv[1] == "client":
        dmc_client(int(sys.argv[2]))
    if sys.argv[1] == "size":
        dmc_size(int(sys.argv[2]))