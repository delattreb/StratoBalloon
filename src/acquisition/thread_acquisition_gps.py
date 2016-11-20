"""
thread_acquisition_gps.py v1.0.0
Auteur: Bruno DELATTRE
Date : 06/10/2016
"""

import threading
import time

from dal import dal_gps
from lib import com_gps, com_logger


class ThreadAcquisitionGPS(threading.Thread):
    def __init__(self, name, delay, counter):
        super().__init__()
        
        self.name = name
        self.counter = counter
        self.delay = delay
    
    def run(self):
        threadlock.acquire()
        
        dal = dal_gps.DAL_GPS()
        logger = com_logger.Logger('GPS:' + self.name)
        logger.info('Start')
        self.getGPS(self.name, self.delay, self.counter, dal)
        logger.info('Stop')

        threadlock.release()
    
    def getGPS(self, threadName, delay, counter, dal):
        instance = com_gps.GPS()
        while counter:
            time.sleep(delay)
            result = instance.getLocalisation(dal)
            counter -= 1


threadlock = threading.Lock()
