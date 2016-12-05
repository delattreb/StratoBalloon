"""
thread_acquisition_gps.py v1.0.0
Auteur: Bruno DELATTRE
Date : 06/10/2016
"""

import sqlite3
import threading
import time

from lib import com_config, com_gps, com_logger


class ThreadAcquisitionGPS(threading.Thread):
    def __init__(self, name, lock, delay, counter):
        super().__init__()
        conf = com_config.Config()
        config = conf.getconfig()
        self.name = name
        self.counter = counter
        self.delay = delay
        self.lock = lock
        self.database = config['SQLITE']['database']
    
    def run(self):
        logger = com_logger.Logger('GPS:' + self.name)
        logger.info('Start')
        self.getgps(self.delay, self.counter)
        logger.info('Stop')

    def getgps(self, delay, counter):
        instance = com_gps.GPS()
        while counter:
            self.lock.acquire()
            
            connection = sqlite3.Connection(self.database)
            cursor = connection.cursor()

            instance.getlocalisation(connection, cursor)
            
            self.lock.release()
            
            counter -= 1
            time.sleep(delay)
