"""
dal_gy9250 v1.0.0
Auteur: Bruno DELATTRE
Date : 20/12/2016
"""


class DAL_GY950:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    """ Select"""
    
    """ Insert """
    
    def set_gy9250(self, name, anglex, angley, anglez, accx, accy, accz, magnx, magny, magnz):
        try:
            self.cursor.execute(
                'INSERT INTO  GY9250 (date, name, anglex, angley, anglez, accx, accy, accz, magnx, magny, magnz) VALUES (datetime("now","localtime"),"' + str(name) +
                '","' + str(anglex) + '","' + str(angley) + '","' + str(anglez) +
                '","' + str(accx) + '","' + str(accy) + '","' + str(accz) +
                '","' + str(magnx) + '","' + str(magny) + '","' + str(magnz)
                + '")')
            self.connection.commit()
        except:
            self.connection.rollback()
