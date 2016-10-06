"""
dal_gps v1.0.0
Auteur: Bruno DELATTRE
Date : 06/10/2016
"""

from lib import com_sqlite


class DAL_GPS(com_sqlite.SQLite):
    def __init__(self):
        super().__init__()
    
    """ Select"""
    
    def get_gps(self):
        return self.cursor.execute(
            'SELECT mode, date, longitude, latitude, altitude, longitude_precision, latitude_precision, altitude_precision FROM coordinate ORDER by date').fetchall()
    
    """ Insert """
    
    def set_gps(self, mode, date, lon, lat, alt, lon_pres, lat_pres, alt_pres):
        try:
            self.cursor.execute(
                'INSERT INTO  coordinate (mode, date, longitude, latitude, altitude, longitude_precision, latitude_precision, altitude_precision) VALUES("' + str(
                    mode) + '", "' + str(date) + '", "' + str(lon) + '", "' + str(lat) + '", "' + str(alt) + '", "' + str(lon_pres) + '", "' + str(lat_pres) +
                '","' + str(alt_pres) + '")')
            
            self.connection.commit()
        except:
            self.connection.rollback()
