"""
dal_picture v1.0.0
Auteur: Bruno DELATTRE
Date : 15/11/2016
"""

from lib import com_sqlite


class DAL_Picture(com_sqlite.SQLite):
    def __init__(self):
        super().__init__()
    
    """ Select"""
    
    """ Update """


    def setpicture(self, name, date):
        try:
            self.cursor.execute('INSERT INTO picture (name, date) VALUES ("' + str(name) + '","' + str(date) + '")')
            self.connection.commit()
        except:
            self.connection.rollback()
