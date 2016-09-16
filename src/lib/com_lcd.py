"""
com_lcd.py v1.0.1
Auteur: Bruno DELATTRE
Date : 12/08/2016
"""

from PIL import ImageFont

from lib.com_ssd1306 import ssd1306
from lib import com_logger

try:
    from smbus import SMBus
except:
    SMBus = None

# Constant
GAUGE_INTERIOR = 2
SMALL_FONT = 0
DEFAULT_FONT = 1
STRONG_FONT = 2


def is_smbus(fonction, *param, **param2):
    def not_present(self, *param, **param2):
        logger = com_logger.Logger('LCD')
        logger.log.debug('SMBus not present')

    if not SMBus:
        return not_present

    return fonction(*param, **param2)


class LCD:
    width_max = 0
    height_max = 0

    @is_smbus
    def __init__(self):
        self.oled = ssd1306(SMBus(1))

        self.width_max = self.oled.width
        self.height_max = self.oled.height

        # Font
        self.bigFont = ImageFont.truetype('lib/font/FreeSans.ttf', 18)
        self.defaultFont = ImageFont.truetype('lib/font/FreeSans.ttf', 13)
        self.smallFont = ImageFont.truetype('lib/font/FreeSans.ttf', 12)

    @is_smbus
    def text(self, x, y, text, fontHeight):
        draw = self.oled.canvas
        if fontHeight == SMALL_FONT:
            draw.text((x, y), text, font=self.smallFont, fill=1)

        if fontHeight == DEFAULT_FONT:
            draw.text((x, y), text, font=self.defaultFont, fill=1)

        if fontHeight == STRONG_FONT:
            draw.text((x, y), text, font=self.bigFont, fill=1)

    @is_smbus
    def rectangle(self, x, y, width, height):
        self.oled.canvas.rectangle((x, y, x + width, y + height), outline=1, fill=0)

    @is_smbus
    def gauge(self, x, y, width, height, value, max_value):
        # exterior gauge
        self.oled.canvas.rectangle((x, y, x + width, y + height), outline=1, fill=0)
        cal = round((((width - GAUGE_INTERIOR) * value) / max_value), 0)
        # interior
        self.oled.canvas.rectangle(
            (x + (GAUGE_INTERIOR / 2), y + (GAUGE_INTERIOR / 2), (x + (GAUGE_INTERIOR / 2) + cal), (y + height) - (GAUGE_INTERIOR / 2)),
            outline=0, fill=1)
