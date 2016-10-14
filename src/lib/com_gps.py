"""
com_gps.py v1.0.0
Auteur: Bruno DELATTRE
Date : 04/10/2016
"""

import gpsd
import gpxpy.gpx
import requests

from dal import dal_gps


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
        self.speed = 0
        self.error = ''
    
    def getGoogleMapsImages(self, directory, filename, zoomlevel=15, width=320, height=385, levelprecision=2, traceroute=False, weight=5, nbpoint=4, color='0xff0000',
                            imageformat='png', maptype='roadmap'):
        # Documentation :https://developers.google.com/maps/documentation/static-maps/intro
        
        google_apikey = 'AIzaSyCdP2hiLc0SNX6eB1w_lb7-JQdF6YO3cr4'
        counter = 0
        mapurl = 'https://maps.googleapis.com/maps/api/staticmap?center='
        dal = dal_gps.DAL_GPS()
        rows = dal.getCoordinate(levelprecision)
        
        for row in rows:
            counter += 1
            file = directory + filename + str(counter) + '.png'
            f = open(file, 'wb')
            url = mapurl + str(row[3]) + ',' + str(row[2]) + '&zoom=' + str(zoomlevel) + '&size=' + str(width) + 'x' + str(
                height) + '&visual_refresh=true&maptype=' + maptype + '&format=' + imageformat
            
            if traceroute:
                path = '&path=color:' + color + '|weight:' + str(weight)
                
                index = counter - nbpoint
                if index < 0:
                    index = 0
                for i in range(index, counter):
                    path += '|' + str(rows[i][3]) + ',' + str(rows[i][2])
                url += path
            url += '&key=' + google_apikey
            f.write(requests.get(url).content)
            f.close()
    
    def exportToGpx(self, filename, trackname=''):
        
        # Load GPS data from database
        dal = dal_gps.DAL_GPS()
        rows = dal.getCoordinate(3)
        
        gpx = gpxpy.gpx.GPX()
        
        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx_track.name = trackname
        gpx.tracks.append(gpx_track)
        
        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)
        
        # Create points:
        for row in rows:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(row[3], row[2], row[4], row[1], None, None, None, None, None, row[8], None))
            # You can add routes and waypoints, too...
        
        stream = gpx.to_xml()
        gpx_file = open(filename, 'w')
        gpx_file.write(stream)
        gpx_file.close()
    
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
                self.speed = packet.speed()
                self.error = packet.error
            
            self.altitude = 0
            if self.mode >= 3:
                self.altitude = packet.altitude()
            
            # Record on database
            if self.mode >= 2:
                dalgps = dal_gps.DAL_GPS()
                dalgps.setCoordinate(self.mode, str(self.timeutc[:-5].replace('T', ' ').replace('Z', '')), self.longitude, self.latitude, self.altitude, 0, 0, 0,
                                     self.speed)
        except:
            pass
