"""
lcd.py v1.0.0
Auteur: Bruno DELATTRE
Date : 13/11/2016
"""

import datetime
import time

from lib import com_config, com_dht22, com_ds18b20, com_gps, com_network, com_ssd1306

splashDuration = 5


class LCD():
    def __init__(self):
        self.config = com_config.getConfig()
        self.lcd = com_ssd1306.SSD1306()
    
    def displayOff(self):
        self.lcd.clear()
    
    def splash(self):
        self.lcd.rectangle(0, 0, self.lcd.width_max - 1, self.lcd.height_max - 1)
        self.lcd.text(4, 1, self.config['APPLICATION']['name'], 2)
        self.lcd.text(4, 17, self.config['APPLICATION']['version'], 1)
        self.lcd.text(4, 49, self.config['APPLICATION']['author'], 0)
        
        self.lcd.display()
        time.sleep(splashDuration)
        self.lcd.clear()
    
    def displatSensor(self):
        # DHT22
        dht22 = com_dht22.DHT22(int(self.config['GPIO']['DHT22_INTERIOR_PORT']), 'DHT22')
        self.lcd.text(1, 1, 'DHT22: ' + str(dht22.temperature()) + '°C', 0)
        self.lcd.text(20, 1, 'DHT22: ' + str(dht22.humidity()) + '%', 0)
        
        # DS18B20
        ds18b20 = com_ds18b20.DS18B20()
        self.lcd.text(1, 11, 'DS18B20 Int: ' + str(ds18b20.read('DS18B20 Interior', self.config['GPIO']['DS18B20_1'])) + '°C', 0)
        self.lcd.text(1, 21, 'DS18B20 Ext: ' + str(ds18b20.read('DS18B20 Exterior', self.config['GPIO']['DS18B20_2'])) + '°C', 0)
        
        self.lcd.display()
        time.sleep(5)
    
    def displayGPSInformation(self):
        network = com_network.NETWORK()
        gps = com_gps.GPS()
        gps.getLocalisation()
        utc = gps.getTime()
        
        network.setTime(utc)
        
        self.lcd.text(1, 1, 'T: ' + datetime.datetime.strftime(datetime.datetime.now(), '%Y %m %d %H:%M:%S'), 0)
        
        if gps.mode > 1:
            self.lcd.text(1, 11, 'G: ' + gps.utc.replace(' ', '').replace('-', ' ').replace('T', ' ').replace('Z', ''), 0)
            self.lcd.text(1, 21, 'Lat: ' + str(gps.latitude), 0)
            self.lcd.text(1, 31, 'Lon: ' + str(gps.longitude), 0)
            self.lcd.text(1, 41, 'Alt: ' + str(gps.altitude), 0)
        
        self.lcd.text(1, 51, 'Ip: ' + network.getIP(), 0)
        
        self.lcd.display()
        time.sleep(5)
    
    def displayStartAcquisition(self):
        self.lcd.text(1, 15, '- START -', 1)
        self.lcd.text(1, 35, 'LAUNCH in: ' + self.config['APPLICATION']['trigger'] + 's', 1)
        self.lcd.display()
