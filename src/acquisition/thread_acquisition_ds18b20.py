"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import threading
import time

from lib import com_ds18b20, com_logger


class ThreadAcquisitionDS18B20(threading.Thread):
    def __init__(self, name, sensor, delay, counter):
        threading.Thread.__init__(self)
        self.name = name
        self.sensor = sensor
        self.counter = counter
        self.delay = delay
        self.exitFlag = 0
    
    def run(self):
        logger = com_logger.Logger('DS18B20:' + self.name)
        logger.log.info('Start')
        self.getTempHum(self.name, self.delay, self.counter)
        logger.log.info('Stop')
    
    def getTempHum(self, threadName, delay, counter):
        instance = com_ds18b20.DS18B20()
        while counter:
            if self.exitFlag:
                threadName.exit()
            time.sleep(delay)
            result = instance.read(self.name, self.sensor)
            counter -= 1
