"""
com_gps.py v1.0.0
Auteur: Bruno DELATTRE
Date : 04/10/2016
"""

import gpsd


class GPS:
    def __init__(self):
        pass
        

    
    def getLocalisation(self):
        try:
            # Connect to the local gpsd
            gpsd.connect()

            # Get gps position
            packet = gpsd.get_current()
            
            # See the inline docs for GpsResponse for the available data
            self.response = packet
        except:
            pass
