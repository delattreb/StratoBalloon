"""
ExportGPS.py v1.0.0
Auteur: Bruno DELATTRE
Date : 28/11/2016
"""

from lib import com_config
from dal import dal_gps
import gpxpy.gpx
import requests
import sqlite3
import datetime


class ExportGPX:
    def getGoogleMapsImages(self, directory, filename, zoomlevel=15, width=320, height=385, levelprecision=2, traceroute=False, weight=5, nbpoint=10, color='0xff0000',
                            imageformat='png', maptype='roadmap'):
        """
        :param directory:
        :param filename:
        :param zoomlevel:
        :param width:
        :param height:
        :param levelprecision:
        :param traceroute:
        :param weight:
        :param nbpoint:
        :param color:
        :param imageformat:
        :param maptype: roadmap, satellite, hybrid et terrain
        :return:
        """
        # Documentation :https://developers.google.com/maps/documentation/static-maps/intro
        config = com_config.getConfig()
        connection = sqlite3.Connection(config['SQLITE']['database'])
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
    
    def exportToGpx(self, filename, trackname=''):
        config = com_config.getConfig()
        connection = sqlite3.Connection(config['SQLITE']['database'])
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
            # You can add routes and waypoints, too...
        
        stream = gpx.to_xml()
        gpx_file = open(filename, 'w')
        gpx_file.write(stream)
        gpx_file.close()
    
    def exportgpx(self):
        config = com_config.getConfig()
        self.exportToGpx(config['EXPORT']['directorygpx'] + '/' + config['EXPORT']['filenamegpx'], 'Work Travel')
    
    def exportimage(self):
        config = com_config.getConfig()
        self.getGoogleMapsImages(config['EXPORT']['directoryimage'], 'img_', 16, 320, 385, 2, True, 5, 80, '0x00ff00', 'png', 'satellite')


com_config.setConfig()
exp = ExportGPX()
exp.exportgpx()
exp.exportimage()
