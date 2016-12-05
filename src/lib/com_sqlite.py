"""
com_sqlite v1.0.3
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import sqlite3

from lib import com_config


class SQLite:
    def __init__(self):
        conf = com_config.Config()
        self.config = conf.getconfig()
        self.connection = sqlite3.Connection(self.config['SQLITE']['database'])
        self.cursor = self.connection.cursor()
    
    def __del__(self):
        self.connection.close()
        self.cursor.close()
