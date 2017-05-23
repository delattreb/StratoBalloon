"""
thread_acquisition_camera.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import sqlite3
import threading
import time

from lib import com_config, com_logger
from lib.driver import com_camera


class ThreadAcquisitionCamera(threading.Thread):
    def __init__(self, name, lock, cemeranumber):
        super().__init__()
        conf = com_config.Config()
        config = conf.getconfig()
        self.name = name
        self.cameranumber = 'CAMERA_' + str(cemeranumber)
        self.counter = int(config[self.cameranumber]['nb'])
        self.delay = float(config[self.cameranumber]['delay'])
        self.lock = lock
        self.database = config['SQLITE']['database']
    
    def run(self):
        logger = com_logger.Logger('Camera Thread')
        logger.info('Start')
        self.getpicture()
        logger.info('Stop')

    def getpicture(self):
        instance = com_camera.Camera('PICTURE', self.cameranumber)
        nextacq = time.time()
        while self.counter:
            if time.time() >= nextacq:
                nextacq += self.delay
                self.lock.acquire()
        
                connection = sqlite3.Connection(self.database)
                cursor = connection.cursor()
        
                instance.getpicture(connection, cursor)
        
                self.lock.release()
        
                self.counter -= 1
