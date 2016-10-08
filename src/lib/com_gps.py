"""
com_gps.py v1.0.0
Auteur: Bruno DELATTRE
Date : 04/10/2016
"""

import gpsd

from dal import dal_gps


# source
# https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=51788

class GPS:
    def __init__(self):
        self.mode = 0
        self.longitude = 0.0
        self.latitude = 0.0
        self.altitude = 0.0
        self.timeutc = ''
        self.longiture_precision = 0
        self.latitude_precision = 0
        self.altitude_precision = 0
        self.error = ''
    
    def getTime(self):
        ret = ''
        try:
            # Connect to the local gpsd
            gpsd.connect()
            
            # Get gps position
            packet = gpsd.get_current()
            
            self.mode = packet.mode
            if self.mode >= 1:  # Check if mode 1 give time UTC
                self.timeutc = packet.time
                ret = str(self.timeutc[:-5].replace('T', ' ').replace('Z', ''))
        except:
            pass
        return ret
    
    def getLocalisation(self):
        try:
            # Connect to the local gpsd
            gpsd.connect()
            
            # Get gps position
            packet = gpsd.get_current()
            
            # See the inline docs for GpsResponse for the available data
            self.mode = packet.mode
            if self.mode >= 2:
                self.longitude = packet.lon
                self.latitude = packet.lat
                self.timeutc = packet.time
                self.error = packet.error
            
            self.altitude = 0
            if self.mode >= 3:
                self.altitude = packet.altitude()
            
            # Record on database
            if self.mode >= 2:
                dalgps = dal_gps.DAL_GPS()
                dalgps.set_gps(self.mode, str(self.timeutc.replace('T', ' ').replace('Z', '')), self.longitude, self.latitude, self.altitude, 0, 0, 0)
        except:
            pass
