"""
thread_acquisition_gps.py v1.0.0
Auteur: Bruno DELATTRE
Date : 06/10/2016
"""

import threading
import time

from lib import com_config, com_logger, com_gps


class ThreadAcquisitionGPS(threading.Thread):
    def __init__(self, name, delay, counter):
        threading.Thread.__init__(self)
        self.name = name
        self.counter = counter
        self.delay = delay
        self.exitFlag = 0

    def run(self):
        logger = com_logger.Logger('GPS:' + self.name)
        logger.log.info('Start')
        self.getGPS(self.name, self.delay, self.counter)
        logger.log.info('Stop')

    def getGPS(self, threadName, delay, counter):
        instance = com_gps.GPS()
        while counter:
            if self.exitFlag:
                threadName.exit()
            time.sleep(delay)
            result = instance.getLocalisation()
            counter -= 1
