"""
dal_dht11 v1.0.0
Auteur: Bruno DELATTRE
Date : 19/09/2016
"""


class DAL_DHT22:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    """ Select"""
    
    """ Insert """
    
    def set_dht22(self, name, temperature, humidity):
        try:
            self.cursor.execute(
                'INSERT INTO  DHT22 (date, name, temperature, humidity) VALUES (datetime("now","localtime"),"' + str(name) + '","' + str(temperature) + '","' + str(
                    humidity) + '")')
            self.connection.commit()
        except:
            self.connection.rollback()
