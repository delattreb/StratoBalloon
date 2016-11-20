"""
com_network.py v1.0.0
Auteur: Bruno DELATTRE
Date : 18/11/2016
"""

import os
import subprocess


class NETWORK:
    def __init__(self):
        self.initTime = False
    
    def getIP(self):
        # Get Ip Adress wlan0 or eth0
        try:
            retvalue = os.popen("ifconfig wlan0 | grep 'inet adr' | cut -c 20-33").readlines()
            if retvalue:
                return str(retvalue[0][:-2])
        except:
            return ''
    
    def setTime(self, utc):
        if not self.initTime:
            subprocess.call("timedatectl set-time '" + str(utc) + "'", shell=True)
            self.initTime = True
