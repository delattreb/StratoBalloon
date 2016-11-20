"""
thread_acquisition_camera.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import threading
import time

from dal import dal_camera, dal_picture
from lib import com_camera, com_logger


class ThreadAcquisitionCamera(threading.Thread):
    def __init__(self, name, delay, counter):
        super().__init__()
        
        self.name = name
        self.counter = counter
        self.delay = delay
        
    def run(self):
        threadlock.acquire()
        
        dalcamera = dal_camera.DAL_Camera()
        dalpicture = dal_picture.DAL_Picture()
        logger = com_logger.Logger('Camera Thread')
        logger.info('Start')
        self.getPicture(self.name, self.delay, self.counter, dalcamera, dalpicture)
        logger.info('Stop')

        threadlock.acquire()
    
    def getPicture(self, threadName, delay, counter, dalcamera, dalpicture):
        instance = com_camera.Camera('PICTURE')
        while counter:
            time.sleep(delay)
            instance.getPicture(dalcamera, dalpicture)
            counter -= 1

threadlock = threading.Lock()
