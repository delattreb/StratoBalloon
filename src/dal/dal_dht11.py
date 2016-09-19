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

    def get_dht11(self):
        return self.cursor.execute('SELECT date, temperature, humidity  FROM DHT11 ORDER by id').fetchall()

    """ Insert """

    def set_dht11(self, date, temperature, humidity):
        try:
            self.cursor.execute(
                'INSERT INTO  DHT11 (date, temperature, humidity) VALUES ("' + str(date) + '","' + str(temperature) + '","' + str(humidity) + '")')
            self.connection.commit()
        except:
            self.connection.rollback()
