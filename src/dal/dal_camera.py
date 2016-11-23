"""
dal_camera v1.0.0
Auteur: Bruno DELATTRE
Date : 16/09/2016
"""


class DAL_Camera:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    """ Select"""
    
    def get_last_picture_id(self):
        rows = self.cursor.execute('SELECT id_picture FROM camera')
        index = 0
        for row in rows:
            index = row[0]
        return index
    
    def get_last_video_id(self):
        rows = self.cursor.execute('SELECT id_video FROM camera')
        index = 0
        for row in rows:
            index = row[0]
        return index
    
    """ Update """
    
    def set_last_picture_id(self, value):
        try:
            self.cursor.execute('UPDATE camera SET id_picture = "' + str(value) + '"')
            self.connection.commit()
        except:
            self.connection.rollback()
    
    def set_last_video_id(self, value):
        try:
            self.cursor.execute('UPDATE camera SET id_video = "' + str(value) + '"')
            self.connection.commit()
        except:
            self.connection.rollback()
