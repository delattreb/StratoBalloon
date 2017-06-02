"""
com_network.py v1.0.0
Auteur: Bruno DELATTRE
Date : 18/11/2016
"""

import os
import subprocess

from lib import com_logger


class NETWORK:
    def __init__(self):
        self.initTime = False

    @staticmethod
    def getip(interface):
        # Get Ip Adress wlan0 or eth0
        # Interface = wlan0 eth0 eth1 etc...
        try:
            retvalue = os.popen("ifconfig " + interface + " | grep 'inet adr' | cut -c 20-33").readlines()
            if retvalue:
                return str(retvalue[0][:-2])
        except:
            return ''

    def settime(self, mode, utc):
        if not self.initTime:
            logger = com_logger.Logger('TIME UTC')
            if mode >= 2:
                subprocess.call("timedatectl set-time '" + str(utc) + "'", shell = True)
                logger.info('Time set to: ' + str(utc))
                self.initTime = True
        return self.initTime
