"""
lcd.py v1.0.0
Auteur: Bruno DELATTRE
Date : 13/11/2016
"""

import datetime
import math
import os
import sqlite3
import time

from PIL import ImageFont

from lib import com_config, com_dht22, com_ds18b20, com_gps, com_logger, com_network
from oled.demo_opts import device
from oled.render import canvas


class LCD:
    def __init__(self):
        conf = com_config.Config()
        self.config = conf.getconfig()
        
        self.network = com_network.NETWORK()
        self.gps = com_gps.GPS()
        
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'FreeSans.ttf'))
        self.smallfont = ImageFont.truetype(font_path, 10)
        self.normalfont = ImageFont.truetype(font_path, 14)
        self.bigfont = ImageFont.truetype(font_path, 27)
    
    def splash(self):
        i = 0
        while i <= 127:
            with canvas(device) as draw:
                # with canvas(device) as draw:
                draw.rectangle((0, 0, device.width - 1, 45), fill = 0, outline = 1)
                draw.text((4, 3), self.config['APPLICATION']['name'], fill = "white")
                draw.text((5, 18), 'v' + self.config['APPLICATION']['version'], fill = "white")
                draw.text((5, 32), self.config['APPLICATION']['author'], fill = "white")
                self.progressbarline(draw, 0, 53, 127, 10, i, 127, 2)
            i += 1
    
    @staticmethod
    def progressbarline(draw, x, y, width, height, value, max_value, interior = 2):
        # with canvas(device) as draw:
        interiormini = interior / 2
        
        # Exterior progressbar
        draw.rectangle((x, y, x + width, y + height), outline = 1, fill = 0)
        
        # Interior
        # Horizontal or vertical
        if width > height:  # Horizontal
            cal = round((((width - interior) * value) / max_value), 0)
            draw.rectangle((x + interiormini, y + interiormini, x + interiormini + cal, y + height - interiormini), outline = 0, fill = 1)
        else:  # Vertical
            cal = round((((height - interior) * value) / max_value), 0)
            draw.rectangle((x + interiormini, y + height - interiormini, x + width - interiormini, y + (height - cal) - interiormini), outline = 0, fill = 1)
    
    @staticmethod
    def progressbar(draw, x, y, width, height, value, max_value, thickness, space, interior = 2, border = True):
        interiormini = interior / 2
        
        # Exterior progressbar
        if border:
            draw.rectangle((x, y, x + width, y + height), outline = 1, fill = 0)
        
        # Interior
        # Horizontal or vertical
        if width > height:  # Horizontal
            totalblock = round((width - interior) / (thickness + space), 0)
            cal = int(round(((totalblock * value) / max_value), 0))
            index = x + interiormini
            for i in range(0, cal):
                draw.rectangle((index, y + interiormini, index + thickness, y + height - interiormini), outline = 0, fill = 1)
                index += (thickness + space)
        else:  # Vertical
            totalblock = round((height - interior) / (thickness + space), 0)
            cal = int(round(((totalblock * value) / max_value), 0))
            index = y + height - interiormini
            for i in range(0, cal):
                draw.rectangle((x + interiormini, index, x + width - interiormini, index - thickness), outline = 0, fill = 1)
                index -= (thickness + space)
    
    @staticmethod
    def progresscircle(draw, x, y, radius, thickness, maxsegments, segments, startangle, totalangle, direction):
        anglechange = (totalangle / maxsegments) * (math.pi / 180)
        i = startangle * (math.pi / 180)
        
        ax = x + (math.cos(i) * radius)
        ay = y - (math.sin(i) * radius)
        
        bx = x + (math.cos(i) * (radius + thickness))
        by = y - (math.sin(i) * (radius + thickness))
        
        for cpt in range(segments):  # for optimisation last process cpt is last value to segments new value
            i += direction * anglechange
            
            cx = x + (math.cos(i) * radius)
            cy = y - (math.sin(i) * radius)
            
            dx = x + (math.cos(i) * (radius + thickness))
            dy = y - (math.sin(i) * (radius + thickness))
            
            # TODO one only
            draw.polygon((ax, ay, bx, by, dx, dy), fill = 1, outline = 1)  # Color 1
            # self.oled.surface.polygon((ax, ay, cx, cy, dx, dy), fill = 1, outline = 1)  # Color 2
            
            ax = cx
            ay = cy
            
            bx = dx
            by = dy
    
    def displaysensor(self):
        connection = sqlite3.Connection(self.config['SQLITE']['database'])
        cursor = connection.cursor()
        
        with canvas(device) as draw:
            # DHT22
            dht22 = com_dht22.DHT22(int(self.config['GPIO']['DHT22_INTERIOR_PORT']), 'DHT22')
            temp, hum = dht22.read('DHT22', connection, cursor, False)
            draw.text((1, 1), 'DHT22: ' + str(temp) + '°C', fill = "white")
            draw.text((85, 1), str(hum) + '%', fill = "white")
            
            # DS18B20
            ds18b20 = com_ds18b20.DS18B20()
            draw.text((1, 11), 'DS18B20 Int: ' + str(ds18b20.read('DS18B20 Interior', self.config['GPIO']['DS18B20_1'], connection, cursor, False)) + '°C', fill = "white")
            # self.lcd.text((1, 21), 'DS18B20 Ext:² ' + str(ds18b20.read('DS18B20 Exterior', self.config['GPIO']['DS18B20_2'])) + '°C',  fill = "white")
    
    def displaygpsinformation(self):
        connection = sqlite3.Connection(self.config['SQLITE']['database'])
        cursor = connection.cursor()
        
        init = False
        while not init:
            with canvas(device) as draw:
                self.gps.getlocalisation(connection, cursor, False)
                init = self.network.settime(self.gps.mode, str(self.gps.timeutc[:-5].replace('T', ' ').replace('Z', '')))
                
                if self.gps.mode >= 2:
                    draw.text((1, 1), datetime.datetime.strftime(datetime.datetime.now(), '%Y %m %d %H:%M:%S'), fill = "white")
                    
                    draw.text((1, 12), 'Lo:' + str(self.gps.longitude)[:8], fill = "white")
                    draw.text((1, 22), 'La:' + str(self.gps.latitude)[:8], fill = "white")
                    draw.text((1, 32), 'Al: ' + str(self.gps.altitude), fill = "white")
                    
                    draw.text((65, 12), '+/-:' + str(self.gps.lonprecision)[:5], fill = "white")
                    draw.text((65, 22), '+/-:' + str(self.gps.latprecision)[:5], fill = "white")
                    draw.text((65, 32), '+/-:' + str(self.gps.altprecision)[:5], fill = "white")
                    
                    draw.text((1, 44), 'SH:' + str(self.gps.hspeed), fill = "white")
                    draw.text((65, 44), 'SV:' + str(0), fill = "white")
                    draw.text((1, 54), 'Sats: ' + str(self.gps.sats), fill = "white")
                    draw.text((65, 54), 'track: ' + str(self.gps.track), fill = "white")
                    
                    time.sleep(3)
    
    def displaystartacquisition(self):
        logger = com_logger.Logger()
        cpt = int(self.config['ACQUISITION']['trigger'])
        for i in range(cpt):
            with canvas(device) as draw:
                draw.text((36, 5), '- START -', fill = "white")
                draw.text((55, 35), str(int(self.config['ACQUISITION']['trigger']) - i), fill = "white")
                draw.display()
                time.sleep(1)
                logger.debug('Start in: ' + str(int(self.config['ACQUISITION']['trigger']) - i))
