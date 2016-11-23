"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import threading
import time
import sqlite3

from dal import dal_dht22
from lib import com_dht22, com_logger, com_config


class ThreadAcquisitionDHT22(threading.Thread):
    def __init__(self, name, lock, port, delay, counter):
        super().__init__()
        
        self.name = name
        self.port = port
        self.counter = counter
        self.delay = delay
        self.lock = lock

    
    def run(self):
        logger = com_logger.Logger('DHT22:' + self.name)
        logger.info('Start')
        self.getTempHum(self.name, self.delay, self.counter)
        logger.info('Stop')
    
    def getTempHum(self, threadName, delay, counter):
        instance = com_dht22.DHT22(self.port, self.name)
        while counter:
            self.lock.acquire()
    
            config = com_config.getConfig()
            connection = sqlite3.Connection(config['SQLITE']['database'])
            cursor = connection.cursor()

            instance.set(connection, cursor)
            
            self.lock.release()

            counter -= 1
            time.sleep(delay)
            

