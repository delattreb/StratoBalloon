# -*- coding: utf-8 -*-

# import module
import math
from time import sleep

from lib.driver import RollPitchYaw, com_mpu9250


def main():
    mpu = com_mpu9250.MPU9250()
    mpu.ready()
    rpy = RollPitchYaw.RollPitchYaw()
    
    while True:
        # get data(mpu9250)
        accel = mpu.readaccel()
        gyro = mpu.readgyro()
        temp = mpu.readtemp()
        magnet = mpu.readlmagnet()
        
        # calc roll, pitch, yaw
        roll = rpy.calcRoll(accel)
        pitch = rpy.calcPitch(accel)
        yaw = rpy.calcYaw(magnet, roll, pitch)
        
        print(math.degrees(roll), math.degrees(pitch), math.degrees(yaw))
        # print(str(accel))
        
        # sleep
        sleep(0.01)


if __name__ == '__main__':
    main()
