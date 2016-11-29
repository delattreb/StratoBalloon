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
        config = com_config.getConfig()
        self.name = name
        self.counter = counter
        self.delay = delay
        self.lock = lock
        self.database = config['SQLITE']['database']
    
    def run(self):
        logger = com_logger.Logger('Camera Thread')
        logger.info('Start')
        self.getPicture(self.delay, self.counter)
        logger.info('Stop')
    
    def getPicture(self, delay, counter):
        instance = com_camera.Camera('PICTURE')
        while counter:
            self.lock.acquire()
            
            connection = sqlite3.Connection(self.database)
            cursor = connection.cursor()
            
            instance.getPicture(connection, cursor)
            
            self.lock.release()
            
            counter -= 1
            time.sleep(delay)
