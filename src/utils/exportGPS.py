"""
ExportGPS.py v1.0.0
Auteur: Bruno DELATTRE
Date : 28/11/2016
"""

import datetime
import sqlite3

import gpxpy.gpx
import requests

from dal import dal_gps
from lib import com_config, com_logger


class ExportGPX:
    def __init__(self):
        self.conf = com_config.Config()
        self.config = self.conf.getconfig()
        self.logger = com_logger.Logger()

    def getgooglemapsimages(self, directory, filename, zoomlevel = 15, width = 320, height = 385, levelprecision = 2, traceroute = False, weight = 5, nbpoint = 10,
                            color = '0xff0000',
                            imageformat = 'png', maptype = 'roadmap'):
        self.logger.info('Get Google Images - levelprecision: ' + str(levelprecision) + ' Zoom Level: ' + str(zoomlevel))
        # Documentation :https://developers.google.com/maps/documentation/static-maps/intro
        connection = sqlite3.Connection(self.config['SQLITE']['database'])
        cursor = connection.cursor()
        
        google_apikey = 'AIzaSyCdP2hiLc0SNX6eB1w_lb7-JQdF6YO3cr4'
        counter = 0
        mapurl = 'https://maps.googleapis.com/maps/api/staticmap?center='
        dal = dal_gps.DAL_GPS(connection, cursor)
        rows = dal.getCoordinate(levelprecision)
        
        for row in rows:
            counter += 1
            file = directory + '/' + filename + str(counter) + '.' + imageformat
            f = open(file, 'wb')
            url = mapurl + str(row[2]) + ',' + str(row[3]) + '&zoom=' + str(zoomlevel) + '&size=' + str(width) + 'x' + str(
                height) + '&visual_refresh=true&maptype=' + maptype + '&format=' + imageformat
            
            if traceroute:
                path = '&path=color:' + color + '|weight:' + str(weight)
                
                index = counter - nbpoint
                if index < 0:
                    index = 0
                for i in range(index, counter):
                    path += '|' + str(rows[i][2]) + ',' + str(rows[i][3])
                url += path
            url += '&key=' + google_apikey
            f.write(requests.get(url).content)
            f.close()
            self.logger.debug('Generate file: ' + file)

    def exporttogpx(self, filename, trackname = ''):
        self.logger.info('Export GPX')
        connection = sqlite3.Connection(self.config['SQLITE']['database'])
        cursor = connection.cursor()
        
        # Load GPS data from database
        dal = dal_gps.DAL_GPS(connection, cursor)
        rows = dal.getCoordinate(2)
        
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
            date = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(row[2], row[3], row[4], date, None, None, row[5], row[6], row[7], row[8], None))
            self.logger.debug('Calculation: ' + str(date))
            # You can add routes and waypoints, too...
        self.logger.info('Generate file: ' + filename)
        stream = gpx.to_xml()
        gpx_file = open(filename, 'w')
        gpx_file.write(stream)
        gpx_file.close()
    
    def exportgpx(self):
        self.exporttogpx(self.config['EXPORT']['directorygpx'] + '/' + self.config['EXPORT']['filenamegpx'], 'Work Travel')
    
    def exportimage(self):
        self.getgooglemapsimages(self.config['EXPORT']['directoryimage'], 'img_', 16, 320, 385, 2, True, 5, 80, '0x00ff00', 'png', 'satellite')


conf = com_config.Config()
# conf.setconfig()

exp = ExportGPX()
exp.logger.info('Application start')
exp.exportgpx()
exp.exportimage()
exp.logger.info('Application stop')
