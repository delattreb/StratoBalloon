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
        self.config['APPLICATION']['author'] = 'Bruno DELATTRE'
        self.config['APPLICATION']['splashduration'] = '1'
        
        # Rasperry N°
        self.config['RASPBERRY'] = {}
        self.config['RASPBERRY']['number'] = '2'  # 1 or 2
        
        # Acquisition
        self.config['ACQUISITION'] = {}
        self.config['ACQUISITION']['trigger'] = '10'  # Wait to start acquisition in second
        
        # LOGGER
        self.config['LOGGER'] = {}
        self.config['LOGGER']['levelconsole'] = '10'  # DEBUG=10 INFO=20 WARNING=30 ERROR=40 #CRITICAL=50
        self.config['LOGGER']['levelfile'] = '10'
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
        # Camera N°1
        self.config['CAMERA_1'] = {}
        self.config['CAMERA_1']['ISO'] = '100'  # 100 - 800
        self.config['CAMERA_1']['pic_resolution_x'] = '2592'
        self.config['CAMERA_1']['pic_resolution_y'] = '1944'
        self.config['CAMERA_1']['vid_resolution_x'] = '1920'
        self.config['CAMERA_1']['vid_resolution_y'] = '1080'
        self.config['CAMERA_1']['framerate'] = '30'
        self.config['CAMERA_1']['rotation'] = '0'  # 0 - 359
        self.config['CAMERA_1']['brightness'] = '0'  # 0 - 100
        self.config['CAMERA_1']['contrast'] = '0'  # -100 - 100
        self.config['CAMERA_1']['raw'] = 'rgba'  # yuv rgb rgba bgr bgra
        self.config['CAMERA_1']['jpegquality'] = '100'
        self.config['CAMERA_1']['image_effect'] = ''  # negative, solarise, posterize, whiteboard, blackboard, sketch, denoise, emboss, oilpaint, hatch, gpen, pastel, watercolour, film, blur, saturation
        self.config['CAMERA_1']['exposure_mode'] = 'auto'  # auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks
        self.config['CAMERA_1']['meter_mode'] = 'average'  # average, spot, backlit, matrix
        self.config['CAMERA_1']['awb'] = 'auto'  # off, auto, sun, cloud, shade, tungsten, fluorescent, incandescent, flash, horizon
        self.config['CAMERA_1']['picture_path'] = 'pictures/'
        self.config['CAMERA_1']['format'] = 'jpeg'  # ‘jpeg’, ‘png’, ‘gif’, ‘bmp’
        self.config['CAMERA_1']['delay'] = '5'
        self.config['CAMERA_1']['nb'] = str(int(((acquisitionduration * 3600) / float(self.config['CAMERA_1']['delay']))))

        # Camera N°2
        self.config['CAMERA_2'] = {}
        self.config['CAMERA_2']['ISO'] = '100'  # 100 - 800
        self.config['CAMERA_2']['pic_resolution_x'] = '2592'
        self.config['CAMERA_2']['pic_resolution_y'] = '1944'
        self.config['CAMERA_2']['vid_resolution_x'] = '1920'
        self.config['CAMERA_2']['vid_resolution_y'] = '1080'
        self.config['CAMERA_2']['framerate'] = '30'
        self.config['CAMERA_2']['rotation'] = '0'  # 0 - 359
        self.config['CAMERA_2']['brightness'] = '0'  # 0 - 100
        self.config['CAMERA_2']['contrast'] = '0'  # -100 - 100
        self.config['CAMERA_2']['raw'] = 'rgba'  # yuv rgb rgba bgr bgra
        self.config['CAMERA_2']['jpegquality'] = '100'
        self.config['CAMERA_2']['image_effect'] = ''  # negative, solarise, posterize, whiteboard, blackboard, sketch, denoise, emboss, oilpaint, hatch, gpen, pastel, watercolour, film, blur, saturation
        self.config['CAMERA_2']['exposure_mode'] = 'auto'  # auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks
        self.config['CAMERA_2']['meter_mode'] = 'average'  # average, spot, backlit, matrix
        self.config['CAMERA_2']['awb'] = 'auto'  # off, auto, sun, cloud, shade, tungsten, fluorescent, incandescent, flash, horizon
        self.config['CAMERA_2']['format'] = 'jpeg'  # ‘jpeg’, ‘png’, ‘gif’, ‘bmp’
        self.config['CAMERA_2']['picture_path'] = 'pictures/'
        self.config['CAMERA_2']['delay'] = '5'
        self.config['CAMERA_2']['nb'] = str(int(((acquisitionduration * 3600) / float(self.config['CAMERA_2']['delay']))))
        
        # GPIO
        self.config['GPIO'] = {}
        
        # DHT22
        self.config['GPIO']['DHT22_INTERIOR_PORT'] = '23'
        self.config['GPIO']['DHT22_INTERIOR_delay'] = '10'
        self.config['GPIO']['DHT22_INTERIOR_nb'] = str(int(((acquisitionduration * 3600) / float(self.config['GPIO']['DHT22_INTERIOR_delay']))))
        # LED
        self.config['GPIO']['DHT22_LED_ACQUISITION'] = '16'
        
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

        # BME280
        self.config['GPIO']['BME280_delay'] = '10'
        self.config['GPIO']['BME280_nb'] = str(int(((acquisitionduration * 3600) / float(self.config['GPIO']['BME280_delay']))))

        # MPU9250
        self.config['GPIO']['MPU9250_delay'] = '0.15'
        self.config['GPIO']['MPU9250_nb'] = str(int(((acquisitionduration * 3600) / float(self.config['GPIO']['MPU9250_delay']))))
        
        # INPUT
        self.config['GPIO']['LED_ACQUISITION'] = '5'
        # INPUT
        self.config['GPIO']['INPUT_ACQUISITION'] = '27'
        
        # GPS
        self.config['GPS'] = {}
        self.config['GPS']['delay'] = '10'
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
