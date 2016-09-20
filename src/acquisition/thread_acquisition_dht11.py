"""
thread_acquisition_camera.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import datetime
import time

import threading
from lib import com_dht11, com_logger, com_config


class ThreadAcquisitionDHT11(threading.Thread):
    def __init__(self, name, delay, counter):
        threading.Thread.__init__(self)
        self.name = name
        self.counter = counter
        self.delay = delay
        self.exitFlag = 0

    def run(self):
        logger = com_logger.Logger('DHT11 Thread')
        logger.log.info('Start')
        self.getdht11(self.name, self.delay, self.counter)
        logger.log.info('Stop')

    def getdht11(self, threadName, delay, counter):
        config = com_config.getConfig()
        instance = com_dht11.DHT11(int(config['GPIO']['DHT11_INTERIOR_PORT']))
        while counter:
            if self.exitFlag:
                threadName.exit()
            time.sleep(delay)
            result = instance.read(self.name)
            counter -= 1
