"""
dal_gps v1.0.0
Auteur: Bruno DELATTRE
Date : 06/10/2016
"""


class DAL_GPS:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
    
    """ Select"""
    
    def getCoordinate(self, mode):
        return self.cursor.execute(
            'SELECT mode, date, longitude, latitude, altitude, longitude_precision, latitude_precision, altitude_precision, hspeed FROM coordinate WHERE mode >= ' + str(
                mode) +
            ' ORDER by date').fetchall()
    
    """ Insert """
    
    def setCoordinate(self, mode, lon, lat, alt, lon_pres, lat_pres, alt_pres, speed):
        try:
            self.cursor.execute(
                'INSERT INTO coordinate (mode, date, longitude, latitude, altitude, longitude_precision, latitude_precision, altitude_precision, hspeed) VALUES("' + str(
                    mode) + '",datetime("now","localtime"),"' + str(lon) + '", "' + str(lat) + '", "' + str(alt) + '", "' + str(lon_pres) + '", "' + str(lat_pres) +
                '","' + str(alt_pres) + '","' + str(speed) + '")')
            self.connection.commit()
        except:
            self.connection.rollback()
    
    """ Delete """
    
    def delCoordinate(self):
        try:
            self.cursor.execute('DELETE FROM coordinate')
            self.connection.commit()
        except:
            self.connection.rollback()
