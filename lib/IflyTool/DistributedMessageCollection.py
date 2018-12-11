#-*-coding:u8-*-
import Queue
from collections import deque
from logger import get_logger
import threading
import logging
from multiprocessing.managers import BaseManager
from PerfInfoTool import PerfInfoTool

class LoadData(object):
    lock = threading.Lock()
    def __init__(self):
        self.items = dict()
        self.items['times'] = 0
        self.items['ok_times'] = 0
        self.items['fail_times'] = 0
        self.items['resp_time'] = 0
        
    def collect(self, counter_name, value):

        self.items[counter_name]+=value

class DistributedMessageCollection(object):
    
    lock = threading.Lock()
    load_msg_queue = deque()
    
    def __init__(self, host ,port, log_file, pit_log_file, pit_time_interval):
        self.logger = get_logger(self.__class__.__name__, log_file, logging.INFO)
        self.port = port
        self.host = host
        self.pit = PerfInfoTool(pit_time_interval, pit_log_file)
        self.pit.start()
        BaseManager.register('get_msg_queue', callable=DistributedMessageCollection.get_msg_queue)
        self.manager = BaseManager(address=(host, port), authkey='iflytek')
        self.manager.start()
        self.queue_handle_thread1 = threading.Thread(target=DistributedMessageCollection.queue_thread_handle, args=(self,))
        self.queue_handle_thread1.setDaemon(True)
        self.queue_handle_thread1.start()
    
    def add_counter(self, name, p_type = 'n'):
        self.pit.add_counter(name, p_type)
        
    def get_pit(self):
        return self.pit

    @staticmethod
    def get_msg_queue():
        return DistributedMessageCollection.load_msg_queue
        
    def queue_thread_handle(self):
        queue = self.manager.get_msg_queue()
        while(True):
            msg = queue.get()
            #self.pit_msg_handle2(msg)
    
    def queue_thread_handle2(self):
        queue = self.manager.get_msg_queue()
        while(True):
            if len(queue)>0:
                queue.pop()
            #self.pit_msg_handle2(msg)
            
    def pit_msg_handle(self,msg):
        #专门处理pit对象的消息
        for k,v in msg.items():
            self.pit.add_value(k, v)
            
    def pit_msg_handle2(self,msg):
        #专门处理pit对象的消息
        tmp_arr = msg.split('|')
        self.pit.add_value(tmp_arr[0], float(tmp_arr[1]))
    
class DistributedLoadCounter(object):
    
    def __init__(self, host, port):
        BaseManager.register('get_msg_queue')
        self.manager = BaseManager(address=(host, port), authkey='iflytek')
        self.manager.connect()
        self.msg_queue = self.manager.get_msg_queue()
        
    def collect(self, counter_name, value):
        self.msg_queue.append(counter_name+"|"+str(value))
