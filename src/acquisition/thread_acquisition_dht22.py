"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import threading
import time

from lib import com_dht22, com_logger


class ThreadAcquisitionDHT22(threading.Thread):
    def __init__(self, name, port, delay, counter):
        threading.Thread.__init__(self)
        self.name = name
        self.port = port
        self.counter = counter
        self.delay = delay
        self.exitFlag = 0
    
    def run(self):
        logger = com_logger.Logger('DHT22:' + self.name)
        logger.log.info('Start')
        self.getTempHum(self.name, self.delay, self.counter)
        logger.log.info('Stop')
    
    def getTempHum(self, threadName, delay, counter):
        while counter:
            if self.exitFlag:
                threadName.exit()
            time.sleep(delay)
            instance = com_dht22.DHT22(self.port, self.name)
            result = instance.set()
            counter -= 1
