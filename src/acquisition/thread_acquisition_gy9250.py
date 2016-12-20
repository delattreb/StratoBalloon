"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import sqlite3
import threading
import time

from lib import com_config, com_logger
from lib.driver import com_gy9250


class ThreadAcquisitionGY9250(threading.Thread):
    def __init__(self, name, lock, mpu_addr, mag_addr, chip_id, delay, counter):
        super().__init__()
        conf = com_config.Config()
        config = conf.getconfig()
        self.name = name
        self.lock = lock
        self.mpu_addr = mpu_addr
        self.mag_addr = mag_addr
        self.chip_id = chip_id
        self.delay = delay
        self.counter = counter
        self.database = config['SQLITE']['database']
    
    def run(self):
        logger = com_logger.Logger('BME280:' + self.name)
        logger.info('Start')
        self.gettemphumpres()
        logger.info('Stop')
    
    def gettemphumpres(self):
        instance = com_gy9250.GY9250(self.mpu_addr, self.mag_addr, self.chip_id)
        while self.counter:
            self.lock.acquire()
            
            connection = sqlite3.Connection(self.database)
            cursor = connection.cursor()
            
            # TODO check how read sensor
            # instance.read()
            # TODO call dal when driver is full operational
            # instance.read(self.name, connection, cursor)
            
            self.lock.release()
            
            self.counter -= 1
            time.sleep(self.delay)