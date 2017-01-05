"""
dal_gy9250 v1.0.0
Auteur: Bruno DELATTRE
Date : 20/12/2016
"""


class DAL_MPU950:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    """ Select"""
    
    """ Insert """

    def set_mpu9250(self, name, gyrox, gyroy, gyroz, accx, accy, accz, magnx, magny, magnz, temp):
        try:
            self.cursor.execute(
                'INSERT INTO  MPU9250 (date, name, gyrox, gyroy, gyroz, accx, accy, accz, magnx, magny, magnz, temp) VALUES (datetime("now","localtime"),"' +
                str(name) + '","' + str(gyrox) + '","' + str(gyroy) + '","' + str(gyroz) + '","' +
                str(accx) + '","' + str(accy) + '","' + str(accz) + '","' +
                str(magnx) + '","' + str(magny) + '","' + str(magnz) + '","' +
                str(temp) + '")')
            self.connection.commit()
        except:
            self.connection.rollback()
