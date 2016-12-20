"""
dal_bme280 v1.0.0
Auteur: Bruno DELATTRE
Date : 20/12/2016
"""


class DAL_BME280:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    """ Select"""
    
    """ Insert """
    
    def set_bme280(self, name, temperature, humidity, pression):
        try:
            self.cursor.execute(
                'INSERT INTO  BME280 (date, name, temperature, humidity, pression) VALUES (datetime("now","localtime"),"' + str(name) + '","' + str(temperature) + '","' + str(humidity) + '","' + str(pression) +
                '")')
            self.connection.commit()
        except:
            self.connection.rollback()
