#-*-coding:u8-*-
import time
from multiprocessing.managers import BaseManager
import random
import json

BaseManager.register('get_load_msg_queue')
m = BaseManager(address=('10.1.186.101', 1234), authkey='iflytek')
m.connect()
queue = m.get_load_msg_queue()
while(True):
    queue.put({"times_a":1})
    queue.put({"times_b":1})
    queue.put({"times_c":1})
    queue.put({"login_resp_time":random.random()})
    queue.put({"login_times":1})
    time.sleep(0.001)
#login_resp_time
'''
json.dumps({"times_a",random.randint(1,10)})
queue.put(json.dumps({"times_a":random.randint(1,10)}))
    queue.put(json.dumps({"times_b":random.randint(1,10)}))
    queue.put(json.dumps({"times_c":random.randint(1,10)}))
    queue.put(json.dumps({"login_resp_time":random.random()}))
    time.sleep(0.1)
'''