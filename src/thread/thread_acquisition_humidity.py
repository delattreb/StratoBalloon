"""
thread_acquisition_humidity.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import threading
import time

from lib import com_camera, com_logger


class ThreadAcquisitionHumidity(threading.Thread):
    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.name = name
        self.counter = counter
        self.exitFlag = 0

    def run(self):
        logger = com_logger.Logger('Camera Thread')
        logger.log.info('Start')
        self.getHumidity(self.name, self.counter, 10)
        logger.log.info('Stop')

    def getHumidity(self, threadName, delay, counter):
        camera = com_camera.Camera('PICTURE')
        while counter:
            if self.exitFlag:
                threadName.exit()
            time.sleep(delay)
            camera.getPicture('/home/pi/')
            counter -= 1
