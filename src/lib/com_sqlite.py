"""
com_sqlite v1.0.3
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import sqlite3
import threading

from lib import com_config


class SQLite:
    def __init__(self):
        config = com_config.getConfig()
        self.connection = sqlite3.Connection(config['SQLITE']['database'])
        self.cursor = self.connection.cursor()
        self.lock = threading.Lock()
    
    def __del__(self):
        self.connection.close()
        self.cursor.close()
