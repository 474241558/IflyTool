# -*- coding:utf-8 -*-
import time
import math
import sys
import os
import threading
import logging
from copy import deepcopy
from logging.handlers import RotatingFileHandler

class PerfInfoTool(object):
    
    def __init__(self, time_interval, log_file):
        self.perf_d = {}
        self.lock = threading.Lock()
        self.time_interval = time_interval
        self.show_order_arr = []
        self.handle_arr = []
        self.log_file_name = log_file
        self.init_log()
        self.logger.info("Perf Info Tool init ok..")
        
    def init_log(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        rt_handler = RotatingFileHandler(self.log_file_name, maxBytes=10*1024*1024,backupCount=5)
        stream_hancler = logging.StreamHandler()
        rt_handler.setFormatter(formatter)
        stream_hancler.setFormatter(formatter)
        self.logger.addHandler(rt_handler)
        self.logger.addHandler(stream_hancler)
        
    def add_counter(self, name, p_type):
        #p_type:n代表普通计数器,t代表事务计数器
        if not self.perf_d.has_key(name):
            self.perf_d[name] = {'type':p_type, 'total_value':0, 'change_value':0, 'total_count':0, 'change_count':0, 'last_change_time':0}
        self.logger.info('add counter:%s, type:%s'%(name, p_type))
        
    def add_value(self, name, value):
        p_type = self.perf_d[name]['type']
        self.lock.acquire()
        if p_type=='n':
            self.perf_d[name]['total_value']+=value
            self.perf_d[name]['change_value']+=value
        elif p_type=='t':
            self.perf_d[name]['total_value']+=value
            self.perf_d[name]['change_value']+=value
            self.perf_d[name]['total_count']+=1
            self.perf_d[name]['change_count']+=1
        self.lock.release()
        
    def add_handle(self, fun):
        self.handle_arr.append(fun)
     
    def set_show_order(self,arr):
        self.show_order_arr = arr
    
    def get_change_vps(self, name, t_len):
        p_type = self.perf_d[name]['type']
        if p_type=='n':
            ret_v = 0
            if self.perf_d[name]['last_change_time'] == 0:
                ret_v = self.perf_d[name]['change_value']/t_len
            else:
                ret_v = self.perf_d[name]['change_value']/(time.time() - self.perf_d[name]['last_change_time'])
            return ret_v
        elif p_type=='t':
            ret_v = 0
            if self.perf_d[name]['change_count'] !=0:
                ret_v = self.perf_d[name]['change_value']/self.perf_d[name]['change_count']
            return ret_v
            
    def get_change_vps2(self, perf_d, name):
        p_type = perf_d[name]['type']
        ret_v = 0
        if p_type=='n':
            if perf_d[name]['last_change_time'] == 0:
                ret_v = perf_d[name]['change_value']/self.time_interval
            else:
                ret_v = perf_d[name]['change_value']/(time.time() - perf_d[name]['last_change_time'])
            return round(ret_v,4)
        elif p_type=='t':
            if perf_d[name]['change_count'] !=0:
                ret_v = perf_d[name]['change_value']/perf_d[name]['change_count']
            return round(ret_v,4)
            
    def clear_change(self, lock = True):
        if lock:
            self.lock.acquire()
        for k in self.perf_d:
            self.perf_d[k]['change_value'] = 0
            self.perf_d[k]['change_count'] = 0
            self.perf_d[k]['last_change_time'] = time.time()
        if lock:
            self.lock.release()
            
    def print_handle(self):
        self.is_run = True
        while(self.is_run):
            time.sleep(self.time_interval)
            
            self.lock.acquire()
            perf_d_copy = deepcopy(self.perf_d)
            self.clear_change(False)
            self.lock.release()
            
            k_arr = perf_d_copy.keys()
            p_info_arr = []
            if self.show_order_arr:
                k_arr = self.show_order_arr
            for k in k_arr:
                if perf_d_copy[k]['type'] == 'n':
                    p_info_arr.append([k+"_tv",perf_d_copy[k]['total_value']])
                    p_info_arr.append([k+"_cv",perf_d_copy[k]['change_value']])
                    p_info_arr.append([k+"_pv",self.get_change_vps2(perf_d_copy, k)])
                elif perf_d_copy[k]['type'] == 't':
                    p_info_arr.append([k+"_tv",perf_d_copy[k]['total_count']])
                    p_info_arr.append([k+"_cv",perf_d_copy[k]['change_count']])
                    p_info_arr.append([k+"_pv",self.get_change_vps2(perf_d_copy, k)])
            if not p_info_arr:
                continue
                
            for f in self.handle_arr:
                f(p_info_arr)
            print_str = " | ".join(map(lambda x:x[0]+":["+str(round(x[1],4))+"]", p_info_arr))
            self.logger.info(print_str)
    
    def start(self):
        self.print_thread = threading.Thread(target=PerfInfoTool.print_handle, args=(self,))
        self.print_thread.setDaemon(True)
        self.print_thread.start()
