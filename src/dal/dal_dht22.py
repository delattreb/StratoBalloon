"""
dal_dht11 v1.0.0
Auteur: Bruno DELATTRE
Date : 19/09/2016
"""

from lib import com_sqlite


class DAL_DHT22(com_sqlite.SQLite):
    def __init__(self):
        super().__init__()

    """ Select"""

    def get_dht22(self):
        return self.cursor.execute('SELECT date, temperature, humidity  FROM DHT22 ORDER by id').fetchall()

    """ Insert """

    def set_dht22(self, date, name, temperature, humidity):
        try:
            self.cursor.execute(
                'INSERT INTO  DHT22 (date, name, temperature, humidity) VALUES ("' + str(date) + '","' + str(name) + '","' + str(temperature) + '","' + str(
                    humidity) + '")')
            self.connection.commit()
        except:
            self.connection.rollback()
