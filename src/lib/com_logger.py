"""
com_logger.py v1.0.2
Auteur: Bruno DELATTRE
Date : 14/08/2016
"""

import logging
from colorlog import ColoredFormatter

from lib import com_config
from logging.handlers import RotatingFileHandler

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'WARNING':  YELLOW,
    'INFO':     WHITE,
    'DEBUG':    BLUE,
    'CRITICAL': YELLOW,
    'ERROR':    RED,
    'RED':      RED,
    'GREEN':    GREEN,
    'YELLOW':   YELLOW,
    'BLUE':     BLUE,
    'MAGENTA':  MAGENTA,
    'CYAN':     CYAN,
    'WHITE':    WHITE,
}

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


class ColorFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        # can't do super(...) here because Formatter is an old school class
        logging.Formatter.__init__(self, *args, **kwargs)
    
    def format(self, record):
        levelname = record.levelname
        color = COLOR_SEQ % (30 + COLORS[levelname])
        message = logging.Formatter.format(self, record)
        message = message.replace("$RESET", RESET_SEQ) \
            .replace("$BOLD", BOLD_SEQ) \
            .replace("$COLOR", color)
        for k, v in COLORS.items():
            message = message.replace("$" + k, COLOR_SEQ % (v + 30)) \
                .replace("$BG" + k, COLOR_SEQ % (v + 40)) \
                .replace("$BG-" + k, COLOR_SEQ % (v + 40))
        return message + RESET_SEQ


class Logger:
    def __init__(self, name='', file=''):
        self.config = com_config.getConfig()
        self.logger = logging.getLogger()
        self.logger.ColorFormatter = ColorFormatter
        self.logger.name = name
        
        # Formatter
        formatterfile = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s : %(name)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
        formatterconsole = ColoredFormatter('%(asctime)s.%(msecs)03d %(log_color)s%(levelname)s : %(name)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
        
        # First logger (file)
        self.logger.setLevel(logging.DEBUG)
        file_handler = RotatingFileHandler(self.config['LOGGER']['logfile'], 'a', int(self.config['LOGGER']['logfilesize']), 1)
        file_handler.setLevel(int(self.config['LOGGER']['levelfile']))
        file_handler.setFormatter(formatterfile)
        self.logger.addHandler(file_handler)
        
        # second logger (console)
        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(int(self.config['LOGGER']['levelconsole']))
        steam_handler.setFormatter(formatterconsole)
        self.logger.addHandler(steam_handler)
    
    def info(self, strinfo):
        self.logger.info(strinfo)
    
    def debug(self, strdebug):
        self.logger.debug(strdebug)
    
    def warning(self, strwarning):
        self.logger.warning(strwarning)
    
    def error(self, strerror):
        self.logger.error(strerror)
    
    def critical(self, strcritical):
        self.logger.critical(strcritical)
