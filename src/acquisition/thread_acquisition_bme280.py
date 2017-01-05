"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import sqlite3
import threading
from time import sleep

from lib import com_config, com_logger
from lib.driver import com_bme280


class ThreadAcquisitionBME280(threading.Thread):
    def __init__(self, name, lock, bus, i2caddr, delay, counter):
        super().__init__()
        conf = com_config.Config()
        config = conf.getconfig()
        self.name = name
        self.lock = lock
        self.bus = bus
        self.i2caddr = i2caddr
        self.delay = delay
        self.counter = counter
        self.database = config['SQLITE']['database']
    
    def run(self):
        logger = com_logger.Logger('BME280:' + self.name)
        logger.info('Start')
        self.gettemphumpres()
        logger.info('Stop')
    
    def gettemphumpres(self):
        instance = com_bme280.BME280(self.bus, self.i2caddr)
        while self.counter:
            self.lock.acquire()
            
            connection = sqlite3.Connection(self.database)
            cursor = connection.cursor()
            
            instance.read()
            # TODO call dal when driver is full operational
            # instance.read(self.name, connection, cursor)
            
            self.lock.release()
            
            self.counter -= 1
            sleep(self.delay)
