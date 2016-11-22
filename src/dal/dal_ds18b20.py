"""
dal_ds18b20 v1.0.0
Auteur: Bruno DELATTRE
Date : 19/09/2016
"""

from lib import com_sqlite


class DAL_DS18B20(com_sqlite.SQLite):
    def __init__(self):
        super().__init__()
    
    """ Select"""
    
    """ Insert """
    
    def set_ds18b20(self, name, temperature):
        self.lock.acquire()
        try:
            self.cursor.execute(
                'INSERT INTO  DS18B20 (date, name, temperature) VALUES (datetime("now"),"' + str(name) + '","' + str(temperature) + '")')
            self.connection.commit()
        except:
            self.connection.rollback()
        self.lock.release()
