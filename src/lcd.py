"""
lcd.py v1.0.0
Auteur: Bruno DELATTRE
Date : 13/11/2016
"""

import datetime
import time

from lib import com_config, com_dht22, com_ds18b20, com_gps, com_network, com_ssd1306


class LCD:
    def __init__(self):
        self.config = com_config.getConfig()
        self.lcd = com_ssd1306.SSD1306()
        self.network = com_network.NETWORK()
        self.gps = com_gps.GPS()
    
    def displayOff(self):
        self.lcd.clear()
    
    def splash(self):
        splashDuration = 2
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
        dht22.set()
        self.lcd.text(1, 1, 'DHT22: ' + str(dht22.temperature()) + '°C', 0)
        self.lcd.text(85, 1, str(dht22.humidity()) + '%', 0)
        
        # DS18B20
        ds18b20 = com_ds18b20.DS18B20()
        self.lcd.text(1, 11, 'DS18B20 Int: ' + str(ds18b20.read('DS18B20 Interior', self.config['GPIO']['DS18B20_1'])) + '°C', 0)
        # self.lcd.text(1, 21, 'DS18B20 Ext: ' + str(ds18b20.read('DS18B20 Exterior', self.config['GPIO']['DS18B20_2'])) + '°C', 0)
        
        self.lcd.display()
        time.sleep(5)
        self.lcd.clear()
    
    def displayGPSInformation(self):
        self.gps.getLocalisation()
        self.network.setTime(str(self.gps.timeutc[:-5].replace('T', ' ').replace('Z', '')))
        
        if self.gps.mode >= 2:
            self.lcd.clear()
            self.lcd.text(1, 1, datetime.datetime.strftime(datetime.datetime.now(), '%Y %m %d %H:%M:%S'), 0)
            
            self.lcd.text(1, 12, 'Lo:' + str(self.gps.longitude)[:8], 0)
            self.lcd.text(1, 22, 'La:' + str(self.gps.latitude)[:8], 0)
            self.lcd.text(1, 32, 'Al: ' + str(self.gps.altitude), 0)
            
            self.lcd.text(65, 12, '+/-:' + str(self.gps.lonprecision)[:5], 0)
            self.lcd.text(65, 22, '+/-:' + str(self.gps.latprecision)[:5], 0)
            self.lcd.text(65, 32, '+/-:' + str(self.gps.altprecision)[:5], 0)

            self.lcd.text(1, 44, 'SH:' + str(self.gps.hspeed), 0)
            self.lcd.text(65, 44, 'SV:' + str(self.gps.vspeed), 0)
            self.lcd.text(1, 54, 'Sats: ' + str(self.gps.sats), 0)
            self.lcd.text(65, 54, 'track: ' + str(self.gps.track), 0)
            
            self.lcd.display()
            time.sleep(5)
        else:
            time.sleep(5)
    
    def displayStartAcquisition(self):
        self.lcd.text(1, 15, '- START -', 1)
        self.lcd.text(1, 35, 'LAUNCH in: ' + self.config['ACQUISITION']['trigger'] + 's', 1)
        self.lcd.display()
        time.sleep(10)
        self.displayOff()