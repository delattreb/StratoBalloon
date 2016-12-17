"""
thread_acquisition_sr04.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import threading
import time

from lib import com_logger
from lib.driver import com_sr04


class ThreadAcquisitionSR04(threading.Thread):
    def __init__(self, name, port_triger, port_echo, delay, counter, threadlock):
        super().__init__()
        
        self.name = name
        self.port_triger = port_triger
        self.port_echo = port_echo
        self.counter = counter
        self.delay = delay
        self.threadlock = threadlock
    
    def run(self):
        logger = com_logger.Logger('SR04:' + self.name)
        logger.info('Start')
        self.getsr04()
        logger.info('Stop')

    def getsr04(self):
        instance = com_sr04.SR04(self.port_triger, self.port_echo)
        while self.counter:
            time.sleep(self.delay)
            self.threadlock.acquire()
            instance.getdistance()
            self.threadlock.release()
            self.counter -= 1
