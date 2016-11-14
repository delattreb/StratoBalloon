#!/usr/bin/python3.4
#  -*- coding: utf-8 -*-

import os
import subprocess
import sys
import time

from lib import com_gps

if not os.getuid() == 0:
    sys.exit('Needs to be root for running this script.')

print('monitoring started')
utc = ''
while True:
    gps = com_gps.GPS()
    utc = gps.getTime()
    
    if utc != '':
        print('Time GPS Fix: ' + str(utc))
        break
    else:
        time.sleep(0.1)

subprocess.call("timedatectl set-time '" + str(utc) + "'", shell=True)
