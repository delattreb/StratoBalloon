"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import sqlite3
import threading
import time

from lib import com_config, com_logger
from lib.driver import com_dht11


class ThreadAcquisitionDHT11(threading.Thread):
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
        logger = com_logger.Logger('DHT11:' + self.name)
        logger.info('Start')
        self.gettemphum()
        logger.info('Stop')

    def gettemphum(self):
        instance = com_dht11.DHT11(self.port)
        nextacq = time.time()
        while self.counter:
            if time.time() >= nextacq:
                nextacq += self.delay
                self.lock.acquire()
        
                connection = sqlite3.Connection(self.database)
                cursor = connection.cursor()
        
                instance.read(self.name, connection, cursor)
        
                self.lock.release()
        
                self.counter -= 1
