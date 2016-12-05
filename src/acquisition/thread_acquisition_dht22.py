"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import sqlite3
import threading
import time

from lib import com_config, com_dht22, com_logger


class ThreadAcquisitionDHT22(threading.Thread):
    def __init__(self, name, lock, port, delay, counter):
        super().__init__()
        conf = com_config.Config()
        config = conf.getconfig()
        self.name = name
        self.port = port
        self.counter = counter
        self.delay = delay
        self.lock = lock
        self.database = config['SQLITE']['database']
    
    def run(self):
        logger = com_logger.Logger('DHT22:' + self.name)
        logger.info('Start')
        self.gettemphum(self.delay, self.counter)
        logger.info('Stop')

    def gettemphum(self, delay, counter):
        instance = com_dht22.DHT22(self.port, self.name)
        while counter:
            self.lock.acquire()
            
            connection = sqlite3.Connection(self.database)
            cursor = connection.cursor()
            
            instance.set(connection, cursor)
            
            self.lock.release()
            
            counter -= 1
            time.sleep(delay)
