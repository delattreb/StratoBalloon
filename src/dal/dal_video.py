"""
dal_video v1.0.0
Auteur: Bruno DELATTRE
Date : 15/11/2016
"""

from lib import com_sqlite


class DAL_Video(com_sqlite.SQLite):
    def __init__(self):
        super().__init__()
    
    """ Select"""
    
    """ Update """
    
    def setvideo(self, name):
        self.lock.acquire()
        try:
            self.cursor.execute('INSERT INTO video (name, date) VALUES ("' + str(name) + '", datetime("now"))')
            self.connection.commit()
        except:
            self.connection.rollback()
        self.lock.release()
