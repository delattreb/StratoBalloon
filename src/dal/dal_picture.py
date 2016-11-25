"""
dal_picture v1.0.0
Auteur: Bruno DELATTRE
Date : 15/11/2016
"""


class DAL_Picture:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    """ Select"""
    
    """ Update """
    
    """ Insert """
    
    def setpicture(self, name):
        try:
            self.cursor.execute('INSERT INTO picture (name, date) VALUES ("' + str(name) + '",datetime("now"))')
            self.connection.commit()
        except:
            self.connection.rollback()
    
    def setvideo(self, name):
        try:
            self.cursor.execute('INSERT INTO video (name, date) VALUES ("' + str(name) + '",datetime("now"))')
            self.connection.commit()
        except:
            self.connection.rollback()
