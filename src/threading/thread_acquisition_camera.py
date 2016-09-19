"""
thread_acquisition_camera.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import threading
import time

from lib import com_camera, com_logger


class ThreadAcquisitionCamera(threading.Thread):
    def __init__(self, name, delay, counter):
        threading.Thread.__init__(self)
        self.name = name
        self.counter = counter
        self.delay = delay
        self.exitFlag = 0

    def run(self):
        logger = com_logger.Logger('Camera Thread')
        logger.log.info('Start')
        self.getPicture(self.name, self.delay, self.counter)
        logger.log.info('Stop')

    def getPicture(self, threadName, delay, counter):
        camera = com_camera.Camera('PICTURE')
        while counter:
            if self.exitFlag:
                threadName.exit()
            time.sleep(delay)
            camera.getPicture('/home/pi/')
            counter -= 1
