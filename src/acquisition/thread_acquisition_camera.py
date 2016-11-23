"""
thread_acquisition_camera.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import sqlite3
import threading
import time

from lib import com_camera, com_config, com_logger


class ThreadAcquisitionCamera(threading.Thread):
    def __init__(self, name, lock, delay, counter):
        super().__init__()
        
        self.name = name
        self.counter = counter
        self.delay = delay
        self.lock = lock
    
    def run(self):
        logger = com_logger.Logger('Camera Thread')
        logger.info('Start')
        self.getPicture(self.name, self.delay, self.counter)
        logger.info('Stop')
    
    def getPicture(self, threadName, delay, counter):
        instance = com_camera.Camera('PICTURE')
        while counter:
            self.lock.acquire()
            
            config = com_config.getConfig()
            connection = sqlite3.Connection(config['SQLITE']['database'])
            cursor = connection.cursor()
            
            instance.getPicture(connection, cursor)
            
            self.lock.release()
            
            counter -= 1
            time.sleep(delay)
