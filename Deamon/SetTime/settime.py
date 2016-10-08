#!/usr/bin/python
#  -*- coding: utf-8 -*-

"""
chmod +x for Python script
copy to: /usr/local/bin
"""

import os
import sys

if not os.getuid() == 0:
    sys.exit('Needs to be root for running this script.')

import time
import subprocess



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
