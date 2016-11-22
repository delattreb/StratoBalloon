"""
dal_dht11 v1.0.0
Auteur: Bruno DELATTRE
Date : 19/09/2016
"""

from lib import com_sqlite


class DAL_DHT11(com_sqlite.SQLite):
    def __init__(self):
        super().__init__()
    
    """ Select"""
      
    """ Insert """
    
    def set_dht11(self, name, temperature, humidity):
        self.lock.acquire()
        try:
            self.cursor.execute(
                'INSERT INTO  DHT11 (date, name, temperature, humidity) VALUES (datetime("now"), ' + str(name) + '","' + str(temperature) + '","' + str(
                    humidity) + '")')
            self.connection.commit()
        except:
            self.connection.rollback()
        self.lock.release()
