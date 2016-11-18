"""
com_network.py v1.0.0
Auteur: Bruno DELATTRE
Date : 18/11/2016
"""

import os


class NETWORK():
    def __init__(self):
        pass
    
    def getIP(self):
        # Get Ip Adress wlan0 or eth0
        retvalue = os.popen("ifconfig wlan0 | grep 'inet adr' | cut -c 20-33").readlines()
        if retvalue:
            return str(retvalue[0])
