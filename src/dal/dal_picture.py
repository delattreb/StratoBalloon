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
    
    """ Insert """
    
    def setpicture(self, name):
        
        try:
            self.cursor.execute('INSERT INTO picture (name, date) VALUES ("' + str(name) + '",datetime("now"))')
            self.connection.commit()
        except:
            self.connection.rollback()
