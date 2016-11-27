"""
dal_video v1.0.0
Auteur: Bruno DELATTRE
Date : 15/11/2016
"""


class DAL_Video:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    """ Select"""
    
    """ Update """
    
    def setvideo(self, name):
        try:
            self.cursor.execute('INSERT INTO video (name, date) VALUES ("' + str(name) + '", datetime("now","localtime"))')
            self.connection.commit()
        except:
            self.connection.rollback()
