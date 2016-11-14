#!/usr/bin/python3.4
#  -*- coding: utf-8 -*-

import os
import sys

if not os.getuid() == 0:
    sys.exit('Needs to be root for running this script.')
import RPi.GPIO as GPIO
import time
import subprocess

# the button is connected on GPIO17
BTN_IO = 17
TIME = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN_IO, GPIO.IN, GPIO.PUD_DOWN)
print('monitoring started')
while True:
    pressedone = (GPIO.input(BTN_IO))
    if pressedone:
        print('pressed')
        time.sleep(TIME)
        if pressedone and (GPIO.input(BTN_IO)):
            break
    else:
        time.sleep(0.1)
GPIO.cleanup()
print('System is going to halt now')
subprocess.call('poweroff')
