"""
com_logger.py v1.0.2
Auteur: Bruno DELATTRE
Date : 14/08/2016
"""

import logging

from lib import com_config


class Logger:
    def __init__(self, name='', file=''):
        self.config = com_config.getConfig()
        self.level = int(self.config['LOGGER']['level'])
        self.log = logging
        if name:
            self.log.getLogger(name)
        self.log.basicConfig(filename=file, level=self.level)
        self.log.basicConfig()
    
    def info(self, strinfo):
        self.log.info(strinfo)
    
    def debug(self, strdebug):
        self.log.debug(strdebug)
    
    def warning(self, strwarning):
        self.log.warning(strwarning)
    
    def error(self, strerror):
        self.log.error(strerror)

    def critical(self, strcritical):
        self.log.critical(strcritical)
