"""
thread_acquisition_dht11.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import sqlite3
import threading
import time

from dal import dal_mpu9250
from lib import com_config, com_logger
from lib.driver import com_mpu9250


class ThreadAcquisitionMPU9250(threading.Thread):
    def __init__(self, name, lock, delay, counter):
        super().__init__()
        conf = com_config.Config()
        config = conf.getconfig()
        self.name = name
        self.lock = lock
        self.delay = delay
        self.counter = counter
        self.database = config['SQLITE']['database']
    
    def run(self):
        logger = com_logger.Logger('BME280:' + self.name)
        logger.info('Start')
        self.gettemphumpres()
        logger.info('Stop')
    
    def gettemphumpres(self):
        instance = com_mpu9250.MPU9250()
        instance.ready()
        # rpy = RollPitchYaw.RollPitchYaw()
        while self.counter:
            self.lock.acquire()
            
            connection = sqlite3.Connection(self.database)
            cursor = connection.cursor()

            acc = instance.readaccel()
            gyro = instance.readgyro()
            magn = instance.readlmagnet()
            temp = instance.readtemp()
            
            # calc roll, pitch, yaw
            # roll = rpy.calcRoll(acc)
            # pitch = rpy.calcPitch(acc)
            # yaw = rpy.calcYaw(acc, roll, pitch)

            # print(math.degrees(roll), math.degrees(pitch), math.degrees(yaw))
            dal = dal_mpu9250.DAL_MPU950(connection, cursor)
            dal.set_mpu9250(self.name, gyro[0], gyro[1], gyro[2], acc[0], acc[1], acc[2], magn[0], magn[1], magn[2], temp)
            
            self.lock.release()
            
            self.counter -= 1
            time.sleep(self.delay)
