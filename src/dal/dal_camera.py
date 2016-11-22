"""
dal_camera v1.0.0
Auteur: Bruno DELATTRE
Date : 16/09/2016
"""

from lib import com_sqlite


class DAL_Camera(com_sqlite.SQLite):
    def __init__(self):
        super().__init__()
    
    """ Select"""
    
    def get_last_picture_id(self):
        self.lock.acquire()
        rows = self.cursor.execute('SELECT id_picture FROM camera')
        index = 0
        for row in rows:
            index = row[0]
        self.lock.release()
        return index
    
    def get_last_video_id(self):
        self.lock.acquire()
        rows = self.cursor.execute('SELECT id_video FROM camera')
        index = 0
        for row in rows:
            index = row[0]
        self.lock.release()
        return index
    
    """ Update """
    
    def set_last_picture_id(self, value):
        self.lock.acquire()
        try:
            self.cursor.execute('UPDATE camera SET id_picture = "' + str(value) + '"')
            self.connection.commit()
        except:
            self.connection.rollback()
        self.lock.release()
    
    def set_last_video_id(self, value):
        self.lock.acquire()
        try:
            self.cursor.execute('UPDATE camera SET id_video = "' + str(value) + '"')
            self.connection.commit()
        except:
            self.connection.rollback()
        self.lock.release()
