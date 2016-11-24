"""
com_logger.py v1.0.2
Auteur: Bruno DELATTRE
Date : 14/08/2016
"""

import logging

from lib import com_config
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, name='', file=''):
        self.config = com_config.getConfig()
        self.logger = logging.getLogger()
        self.logger.name = name
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)s : %(name)s - %(message)s', datefmt="%d/%m/%Y %H:%M:%S")
        # First logger (file)
        self.logger.setLevel(logging.DEBUG)
        file_handler = RotatingFileHandler(self.config['LOGGER']['logfile'], 'a', int(self.config['LOGGER']['logfilesize']), 1)
        file_handler.setLevel(int(self.config['LOGGER']['levelfile']))
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # second logger (console)
        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(int(self.config['LOGGER']['levelconsole']))
        steam_handler.setFormatter(formatter)
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
