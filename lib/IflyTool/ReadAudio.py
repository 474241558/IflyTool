#-*-coding:u8-*-
import time

class ReadAudio(object):

    def __init__(self,file_path, has_header = -1,is_sleep = True, per_read_size = 1280, per_second_size = 32000, speed = 1):
        self.video_fo = open(file_path,'rb')
        self.has_header = has_header
        self.per_read_size = per_read_size
        self.per_second_size = per_second_size
        self.is_sleep = is_sleep
        self.all_read_size = 0
        self.speed = speed
        self.start_read_time = 0
        self.last_read_time = 0
        self.last_read_time_2 = 0
        #最后一次读的时间（不为空的一次）
        self.header_proc()
        self.audio_size_len = self.get_len()
        self.is_read_end = False
        
    def read(self):
        if self.start_read_time == 0:
            self.start_read_time =time.time()
        audio_buff = self.video_fo.read(self.per_read_size)
        if len(audio_buff)!=self.per_read_size and len(audio_buff)>0:
            self.last_read_time_2 = time.time()
            self.is_read_end = True
        self.last_read_time = time.time()
        self.all_read_size += len(audio_buff)
        if self.all_read_size == self.audio_size_len and len(audio_buff)>0:
            self.last_read_time_2 = time.time()
            self.is_read_end = True
        self.has_read_audio_time = self.all_read_size*1.0/self.per_second_size
        # 睡眠时间等于音频当前时间 减去 从开始读音频到现在花的时间
        self.sleep_time = self.has_read_audio_time - (time.time()-self.start_read_time)
        if self.sleep_time > 0 and self.is_sleep:
            time.sleep(self.sleep_time/self.speed)
        return audio_buff
        
    def get_has_read_audio_time(self):
        return time.time() - self.start_read_time
        
    def get_last_read_time(self):
        if self.last_read_time_2 == 0:
            return self.last_read_time
        else:
            return self.last_read_time_2

    def close(self):
        self.video_fo.close()
        
    def header_proc(self):
        maker=self.video_fo.read(4)
        if b'RIFF' == maker:
            self.has_header = 1
            self.video_fo.seek(44, 0)
        else:
            self.has_header = 0
            self.video_fo.seek(0, 0)
            
    def get_len(self):
        self.video_fo.seek(0, 2)
        all_size = self.video_fo.tell()
        if self.has_header == 1:
            self.video_fo.seek(44, 0)
            return all_size - 44
        else:
            self.video_fo.seek(0, 0)
            return all_size