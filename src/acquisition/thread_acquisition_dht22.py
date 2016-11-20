"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import threading
import time

from lib import com_dht22, com_logger
from dal import dal_dht22


class ThreadAcquisitionDHT22(threading.Thread):
    def __init__(self, name, port, delay, counter):
        super().__init__()
        
        self.name = name
        self.port = port
        self.counter = counter
        self.delay = delay
        self.exitFlag = 0
    
    def run(self):
        threadlock.acquire()
        
        dal = dal_dht22.DAL_DHT22()
        logger = com_logger.Logger('DHT22:' + self.name)
        logger.info('Start')
        self.getTempHum(self.name, self.delay, self.counter, dal)
        logger.info('Stop')
        
        threadlock.release()
    
    def getTempHum(self, threadName, delay, counter, dal):
        while counter:
            time.sleep(delay)
            instance = com_dht22.DHT22(self.port, self.name)
            result = instance.set(dal)
            counter -= 1

threadlock = threading.Lock()
