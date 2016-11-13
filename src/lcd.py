"""
lcd.py v1.0.0
Auteur: Bruno DELATTRE
Date : 13/11/2016
"""

import datetime
import os
import time

from lib import com_config, com_gps, com_lcd

splashDuration = 5


def getIP():
    # Get Ip Adress wlan0 or eth0
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
    gps = com_gps.GPS()
    gps.getLocalisation()
    lcd = com_lcd.LCD()
    
    lcd.text(1, 1, 'T: ' + datetime.datetime.strftime(datetime.datetime.now(), '%d %m %Y %H:%M:%S'), 0)
    
    if gps.mode > 1:
        lcd.text(1, 11, 'G: ' + gps.utc.replace(' ', '').replace('-', ' ').replace('T', ' ').replace('Z', ''), 0)
        lcd.text(1, 21, 'Lat: ' + str(gps.latitude), 0)
        lcd.text(1, 31, 'Lon: ' + str(gps.longitude), 0)
        lcd.text(1, 41, 'Alt: ' + str(gps.altitude), 0)
    
    lcd.text(1, 51, 'Ip: ' + getIP(), 0)
    
    lcd.display()
    time.sleep(5)
