"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import math
import sqlite3
import threading
import time

from lib import com_config, com_logger
from lib.driver import RollPitchYaw, com_gy9250


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
        instance = com_gy9250.MPU9250()
        instance.ready()
        rpy = RollPitchYaw.RollPitchYaw()
        while self.counter:
            self.lock.acquire()
            
            connection = sqlite3.Connection(self.database)
            cursor = connection.cursor()

            accel = instance.readaccel()
            gyro = instance.readgyro()
            temp = instance.readtemp()
            magnet = instance.readlmagnet()

            # calc roll, pitch, yaw
            roll = rpy.calcRoll(accel)
            pitch = rpy.calcPitch(accel)
            yaw = rpy.calcYaw(magnet, roll, pitch)

            print(math.degrees(roll), math.degrees(pitch), math.degrees(yaw))
            self.lock.release()
            
            self.counter -= 1
            time.sleep(self.delay)
