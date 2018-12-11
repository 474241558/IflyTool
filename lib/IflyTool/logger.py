#-*-coding:u8-*-

import logging
from logging.handlers import RotatingFileHandler

def get_logger(name, log_file, log_level):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rt_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024,backupCount=5)
    stream_hancler = logging.StreamHandler()
    rt_handler.setFormatter(formatter)
    stream_hancler.setFormatter(formatter)
    logger.addHandler(rt_handler)
    logger.addHandler(stream_hancler)
    return logger