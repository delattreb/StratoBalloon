"""
thread_acquisition_camera.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import threading
import time

from lib import com_config, com_logger, com_sr04


class ThreadAcquisitionSR04(threading.Thread):
    def __init__(self, name, port_triger, port_echo, delay, counter):
        threading.Thread.__init__(self)
        self.name = name
        self.port_triger = port_triger
        self.port_echo = port_echo
        self.counter = counter
        self.delay = delay
        self.exitFlag = 0

    def run(self):
        logger = com_logger.Logger('SR04:' + self.name)
        logger.log.info('Start')
        self.getsr04(self.name, self.delay, self.counter)
        logger.log.info('Stop')

    def getsr04(self, threadName, delay, counter):
        instance = com_sr04.SR04(self.port_triger, self.port_echo)
        while counter:
            if self.exitFlag:
                threadName.exit()
            time.sleep(delay)
            result = instance.getDistance()
            counter -= 1
