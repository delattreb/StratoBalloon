#!/usr/bin/python
#  -*- coding: utf-8 -*-

#check good shebang
import os
import sys

if not os.getuid() == 0:
    sys.exit('Needs to be root for running this script.')
import RPi.GPIO as GPIO
import time
import subprocess

# the button is connected on GPI4 (pin 7)
BTN_IO = 4
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
print('System is going to halt now')
subprocess.call('poweroff')
