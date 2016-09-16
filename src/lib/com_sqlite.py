"""
com_sqlite v1.0.3
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import sqlite3

from lib import com_config


class SQLite:
    def __init__(self):
        self.connection, self.cursor = self.connect()

    def __del__(self):
        self.connection.close()

    def connect(self):
        config = com_config.getConfig()
        con = sqlite3.connect(config['SQLITE']['database'])
        cursor = con.cursor()
        return con, cursor

