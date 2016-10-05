"""
com_gps.py v1.0.0
Auteur: Bruno DELATTRE
Date : 04/10/2016
"""

import os

from gps import *


class GPS:
    def __init__(self):
        self.latitude = 0
        self.longiture = 0
        self.timeutc = 0
        self.altitude = 0
        self.speed = 0
        self.satellites = 0

    def getLocalisation(self):
        session = gps(mode=WATCH_ENABLE)
        try:
            while True:
                donnees = session.next()
                if donnees['class'] == "TPV":
                    os.system('clear')
                    self.latitude = session.fix.latitude
                    self.longitude = session.fix.longitude
                    self.timeutc = session.utc
                    self.altitude = session.fix.altitude
                    self.speed = session.fix.speed
                    self.satellites = session.satellites
        except KeyError:
            pass
        except KeyboardInterrupt:
            print("closed by user")
        except StopIteration:
            print("GPSD off")
        finally:
            session = None
