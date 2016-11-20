"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import threading
import time

from dal import dal_dht11
from lib import com_dht11, com_logger


class ThreadAcquisitionDHT11(threading.Thread):
    def __init__(self, name, port, delay, counter):
        super().__init__()
        
        self.name = name
        self.port = port
        self.counter = counter
        self.delay = delay
    
    def run(self):
        threadlock.acquire()
        
        dal = dal_dht11.DAL_DHT11()
        logger = com_logger.Logger('DHT11:' + self.name)
        logger.info('Start')
        self.getTempHum(self.name, self.delay, self.counter, dal)
        logger.info('Stop')
        
        threadlock.release()
    
    def getTempHum(self, threadName, delay, counter, dal):
        instance = com_dht11.DHT11(self.port)
        while counter:
            time.sleep(delay)
            result = instance.read(self.name, dal)
            counter -= 1

threadlock = threading.Lock()
