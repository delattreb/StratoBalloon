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

    def getLastPictureId(self):
        rows = self.cursor.execute('SELECT id_picture FROM camera')
        id = 0
        for row in rows:
            id = row[0]
        return id

    def getLastVideoId(self):
        rows = self.cursor.execute('SELECT id_video FROM camera')
        id = 0
        for row in rows:
            id = row[0]
        return id

    """ Update """

    def setLastPictureId(self, value):
        try:
            self.cursor.execute('UPDATE camera SET id_picture = ' + value)
            self.connection.commit()
        except:
            self.connection.rollback()

    def setLastVideoId(self, value):
        try:
            self.cursor.execute('UPDATE camera SET id_video = ' + value)
            self.connection.commit()
        except:
            self.connection.rollback()
