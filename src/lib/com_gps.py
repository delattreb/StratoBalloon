"""
com_gps.py v1.0.0
Auteur: Bruno DELATTRE
Date : 04/10/2016
"""

import gpsd

from dal import dal_gps
from lib import com_logger


class GPS:
    def __init__(self):
        self.mode = 0
        self.sats = 0
        self.track = 0
        self.longitude = 0.0
        self.latitude = 0.0
        self.altitude = 0.0
        self.timeutc = ''
        self.latprecision = 0.0
        self.lonprecision = 0.0
        self.altprecision = 0.0
        self.hspeed = 0.0
        self.vspeed = 0.0
        
        # Connect to the local gpsd
        gpsd.connect()

    def gettime(self):
        ret = ''
        try:
            packet = gpsd.get_current()
            
            self.mode = packet.mode
            if self.mode >= 1:  # Check if mode 1 give time UTC
                self.timeutc = packet.time
                ret = str(self.timeutc[:-5].replace('T', ' ').replace('Z', ''))
        except:
            pass
        return ret

    def getlocalisation(self, connection, cursor, setdb = True):
        dal = dal_gps.DAL_GPS(connection, cursor)
        logger = com_logger.Logger('GPS')
        try:
            # Get gps position
            packet = gpsd.get_current()
            
            # Debug info GPS
            logger.debug('mode:' + str(packet.mode))
            logger.debug('lon:' + str(packet.lon))
            logger.debug('lat:' + str(packet.lat))
            logger.debug('alt:' + str(packet.alt))
            logger.debug('hspeed:' + str(packet.hspeed))
            # logger.debug('vspeed:' + str(packet.speed_vertical()))
            logger.debug('lon +/-:' + str(packet.error['x']))
            logger.debug('lat +/-:' + str(packet.error['y']))
            logger.debug('alt +/-:' + str(packet.error['v']))
            logger.debug('sats:' + str(packet.sats))
            logger.debug('track:' + str(packet.track))
            logger.debug('time:' + str(packet.time))
            
            # See the inline docs for GpsResponse for the available data
            self.altitude = 0.0
            self.mode = packet.mode
            if self.mode >= 2:
                self.sats = packet.sats
                self.track = packet.track
                self.longitude = packet.lon
                self.latitude = packet.lat
                self.timeutc = packet.time
                self.hspeed = packet.hspeed
                self.lonprecision = packet.error['x']
                self.latprecision = packet.error['y']
            
            if self.mode >= 3:
                self.altitude = packet.altitude()
                self.altprecision = packet.error['v']
                # self.vspeed = packet.speed_vertical()
            
            if self.mode >= 2:
                if setdb:
                    dal.setCoordinate(self.mode, self.longitude, self.latitude, self.altitude,
                                      self.lonprecision, self.latprecision, self.altprecision, self.hspeed)
                    logger.info('GPS info -> database')
        except:
            logger.error('GPS exception')
