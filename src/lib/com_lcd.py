"""
com_lcd.py v1.0.2
Auteur: Bruno DELATTRE
Date : 12/08/2016
"""

from PIL import ImageFont

from lib import com_logger
from lib.com_ssd1306 import ssd1306

try:
    from smbus import SMBus
except:
    SMBus = None


def is_plugged(function):
    def plugged(*original_args, **original_kwargs):
        return function(*original_args, **original_kwargs)
    
    if not SMBus:
        logger = com_logger.Logger('LCD')
        logger.log.warning('LCD not present')
    
    return plugged


class LCD:
    @is_plugged
    def __init__(self):
        # Constant
        self.SMALL_FONT = 0
        self.DEFAULT_FONT = 1
        self.STRONG_FONT = 2
        self.GAUGE_INTERIOR = 2
        
        # Font
        self.__bigFont = ImageFont.truetype('font/FreeSerif.ttf', 18)
        self.__defaultFont = ImageFont.truetype('font/FreeSerif.ttf', 13)
        self.__smallFont = ImageFont.truetype('font/FreeSerif.ttf', 12)
        
        self.oled = ssd1306(SMBus(1)) if SMBus != None else None
        self.width_max = self.oled.width if SMBus != None else 0
        self.height_max = self.oled.height if SMBus != None else 0
    
    def display(self):
        if SMBus != None:
            self.oled.display()
    
    def clear(self):
        if SMBus != None:
            self.oled.cls()
    
    def text(self, x, y, text, fontHeight):
        if SMBus != None:
            draw = self.oled.canvas
            if fontHeight == self.SMALL_FONT:
                draw.text((x, y), text, font=self.__smallFont, fill=1)
            
            if fontHeight == self.DEFAULT_FONT:
                draw.text((x, y), text, font=self.__defaultFont, fill=1)
            
            if fontHeight == self.STRONG_FONT:
                draw.text((x, y), text, font=self.__bigFont, fill=1)
    
    def rectangle(self, x, y, width, height):
        if SMBus != None:
            self.oled.canvas.rectangle((x, y, x + width, y + height), outline=1, fill=0)
    
    def gauge(self, x, y, width, height, value, max_value):
        if SMBus != None:
            # exterior gauge
            self.oled.canvas.rectangle((x, y, x + width, y + height), outline=1, fill=0)
            cal = round((((width - self.GAUGE_INTERIOR) * value) / max_value), 0)
            # interior
            self.oled.canvas.rectangle(
                (x + (self.GAUGE_INTERIOR / 2), y + (self.GAUGE_INTERIOR / 2), (x + (self.GAUGE_INTERIOR / 2) + cal), (y + height) - (self.GAUGE_INTERIOR / 2)),
                outline=0, fill=1)
