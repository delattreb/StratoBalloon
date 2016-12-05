"""
com_config.py v 1.0.2
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import configparser
import os.path

config_file = "config/config.ini"


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
    
    def setconfig(self):
        acquisitionduration = 6  # In hours
        
        # region Config
        # Version
        self.config['APPLICATION'] = {}
        self.config['APPLICATION']['name'] = 'Strato Balloon'
        self.config['APPLICATION']['version'] = '1.3.0'
        self.config['APPLICATION']['author'] = '© Bruno DELATTRE'
        
        # Acquisition
        self.config['ACQUISITION'] = {}
        self.config['ACQUISITION']['trigger'] = '5'
        
        # LOGGER
        self.config['LOGGER'] = {}
        self.config['LOGGER']['levelconsole'] = '20'  # DEBUG=10 INFO=20 WARNING=30 ERROR=40 #CRITICAL=50
        self.config['LOGGER']['levelfile'] = '20'
        self.config['LOGGER']['logfile'] = 'log'
        self.config['LOGGER']['logfilesize'] = '1000000'
        
        # Export
        self.config['EXPORT'] = {}
        self.config['EXPORT']['directorygpx'] = 'export'
        self.config['EXPORT']['filenamegpx'] = 'export.gpx'
        self.config['EXPORT']['directoryimage'] = 'exportpicture'
        
        # SQLite
        self.config['SQLITE'] = {}
        self.config['SQLITE']['database'] = 'database.db'
        
        # Camera v8M 3280x2464 -- v5M 2592x1944
        self.config['CAMERA'] = {}
        self.config['CAMERA']['pic_resolution_x'] = '2592'
        self.config['CAMERA']['pic_resolution_y'] = '1944'
        self.config['CAMERA']['vid_resolution_x'] = '1920'
        self.config['CAMERA']['vid_resolution_y'] = '1080'
        self.config['CAMERA']['framerate'] = '30'
        self.config['CAMERA']['rotation'] = '0'
        self.config['CAMERA']['brightness'] = '0'
        self.config['CAMERA']['contrast'] = '0'
        # negative, solarise, posterize, whiteboard, blackboard, sketch, denoise, emboss, oilpaint, hatch, gpen, pastel, watercolour, film, blur, saturation
        self.config['CAMERA']['image_effect'] = ''
        # auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks
        self.config['CAMERA']['exposure_mode'] = 'auto'
        # average, spot, backlit, matrix
        self.config['CAMERA']['meter_mode'] = 'average'
        # off, auto, sun, cloud, shade, tungsten, fluorescent, incandescent, flash, horizon
        self.config['CAMERA']['awb'] = 'auto'
        self.config['CAMERA']['picture_path'] = 'pictures/'
        self.config['CAMERA']['delay'] = '3'
        self.config['CAMERA']['nb'] = str(int(((acquisitionduration * 3600) / float(self.config['CAMERA']['delay']))))
        
        # GPIO
        self.config['GPIO'] = {}
        
        # DHT11 interior
        self.config['GPIO']['DHT11_INTERIOR_PORT'] = '24'
        self.config['GPIO']['DHT11_INTERIOR_delay'] = '15'
        self.config['GPIO']['DHT11_INTERIOR_nb'] = str(int(((acquisitionduration * 3600) / float(self.config['GPIO']['DHT11_INTERIOR_delay']))))
        
        # DHT11 exterior
        self.config['GPIO']['DHT11_EXTERIOR_PORT'] = '25'
        self.config['GPIO']['DHT11_EXTERIOR_delay'] = '15'
        self.config['GPIO']['DHT11_EXTERIOR_nb'] = str(int(((acquisitionduration * 3600) / float(self.config['GPIO']['DHT11_EXTERIOR_delay']))))
        
        # DHT22
        self.config['GPIO']['DHT22_INTERIOR_PORT'] = '5'
        self.config['GPIO']['DHT22_INTERIOR_delay'] = '10'
        self.config['GPIO']['DHT22_INTERIOR_nb'] = str(int(((acquisitionduration * 3600) / float(self.config['GPIO']['DHT22_INTERIOR_delay']))))
        
        # DS18B20
        self.config['GPIO']['DS18B20_1'] = '/sys/bus/w1/devices/w1_bus_master1/28-0416618c01ff/w1_slave'
        self.config['GPIO']['DS18B20_1_delay'] = '10'
        self.config['GPIO']['DS18B20_1_nb'] = str(int(((acquisitionduration * 3600) / float(self.config['GPIO']['DS18B20_1_delay']))))
        
        self.config['GPIO']['DS18B20_2'] = ''
        self.config['GPIO']['DS18B20_2_delay'] = '10'
        self.config['GPIO']['DS18B20_2_nb'] = str(int(((acquisitionduration * 3600) / float(self.config['GPIO']['DS18B20_2_delay']))))
        
        # SR04
        self.config['GPIO']['SR04_triger_port'] = '22'
        self.config['GPIO']['SR04_echo_port'] = '27'
        self.config['GPIO']['SR04_delay'] = '1'
        self.config['GPIO']['SR04_nb'] = str(int(((acquisitionduration * 3600) / float(self.config['GPIO']['SR04_delay']))))
        
        # LED
        self.config['GPIO']['LED_ACQUISITION'] = '23'
        
        # INPUT
        self.config['GPIO']['INPUT_ACQUISITION'] = '27'
        
        # GPS
        self.config['GPS'] = {}
        self.config['GPS']['delay'] = '1'
        self.config['GPS']['nb'] = str(int(((acquisitionduration * 3600) / float(self.config['GPS']['delay']))))
        
        # endregion
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, config_file)
        with open(db_path, 'w') as configfile:
            self.config.write(configfile)
    
    def getconfig(self):
        self.config = configparser.RawConfigParser()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, config_file)
        self.config.read(db_path)
        return self.config
