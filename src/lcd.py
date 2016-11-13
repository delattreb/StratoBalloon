"""
lcd.py v1.0.0
Auteur: Bruno DELATTRE
Date : 13/11/2016
"""

import os
import time

from lib import com_config, com_lcd

splashDuration = 6


def getIP():
    # Get Ip Adress
    retvalue = os.popen("ifconfig wlan0 | grep 'inet adr' | cut -c 20-33").readlines()
    if retvalue:
        return str(retvalue[0])


def splash():
    config = com_config.getConfig()
    lcd = com_lcd.LCD()
    
    lcd.rectangle(0, 0, lcd.width_max - 1, lcd.height_max - 1)
    lcd.text(4, 1, config['APPLICATION']['name'], 2)
    lcd.text(4, 17, config['APPLICATION']['version'], 1)
    lcd.text(4, 49, config['APPLICATION']['author'], 0)
    
    lcd.display()
    time.sleep(splashDuration)
    lcd.clear()


def displayInformation():
    # Time
    # Date
    # GPS Lat Long Alt
    # IP
    pass
