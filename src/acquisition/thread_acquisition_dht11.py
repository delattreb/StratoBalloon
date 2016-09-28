"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import threading
import time

from lib import com_config, com_dht11, com_logger


class ThreadAcquisitionDHT11(threading.Thread):
    def __init__(self, name, port, delay, counter):
        threading.Thread.__init__(self)
        self.name = name
        self.port = port
        self.counter = counter
        self.delay = delay
        self.exitFlag = 0

    def run(self):
        logger = com_logger.Logger('DHT11:' + self.name)
        logger.log.info('Start')
        self.getTempHum(self.name, self.delay, self.counter)
        logger.log.info('Stop')

    def getTempHum(self, threadName, delay, counter):
        instance = com_dht11.DHT11(self.port)
        while counter:
            if self.exitFlag:
                threadName.exit()
            time.sleep(delay)
            result = instance.read(self.name)
            counter -= 1
