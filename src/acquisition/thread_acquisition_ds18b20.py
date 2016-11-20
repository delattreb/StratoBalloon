"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import threading
import time
import sqlite3

from lib import com_ds18b20, com_logger
from dal import dal_ds18b20

class ThreadAcquisitionDS18B20(threading.Thread):
    def __init__(self, name, sensor, delay, counter):
        super().__init__()

        self.name = name
        self.sensor = sensor
        self.counter = counter
        self.delay = delay
        self.cursor = sqlite3.Cursor()
    
    def run(self):
        threadlock.acquire()
        
        dal = dal_ds18b20.DAL_DS18B20()
        logger = com_logger.Logger('DS18B20:' + self.name)
        logger.info('Start')
        self.getTempHum(self.name, self.delay, self.counter, dal)
        logger.info('Stop')
        
        threadlock.release()
    
    def getTempHum(self, threadName, delay, counter, dal):
        instance = com_ds18b20.DS18B20()
        while counter:
            time.sleep(delay)
            result = instance.read(self.name, self.sensor, dal)
            counter -= 1

threadlock = threading.Lock()
