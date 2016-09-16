"""
com_logger.py v1.0.2
Auteur: Bruno DELATTRE
Date : 14/08/2016
"""

import logging

from lib import com_config


class Logger:
    def __init__(self, name='', file=''):
        config = com_config.getConfig()
        self.level = int(config['LOGGER']['level'])
        self.log = logging
        self.log.basicConfig(filename=file, level=self.level)

        if name:
            self.log = logging.getLogger(name)
