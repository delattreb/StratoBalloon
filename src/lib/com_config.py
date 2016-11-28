"""
com_config.py v 1.0.2
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import configparser
import os.path

config_file = "config/config.ini"


def setConfig():
    acquisitionDuration = 6  # In hours
    config = configparser.ConfigParser()
    
    # region Config
    # Version
    config['APPLICATION'] = {}
    config['APPLICATION']['name'] = 'Strato Balloon'
    config['APPLICATION']['version'] = '1.3.0'
    config['APPLICATION']['author'] = '© Bruno DELATTRE'
    
    # Acquisition
    config['ACQUISITION'] = {}
    config['ACQUISITION']['trigger'] = '20'
    
    # LOGGER
    config['LOGGER'] = {}
    config['LOGGER']['levelconsole'] = '10'  # DEBUG=10 INFO=20 WARNING=30 ERROR=40 #CRITICAL=50
    config['LOGGER']['levelfile'] = '20'
    config['LOGGER']['logfile'] = 'log'
    config['LOGGER']['logfilesize'] = '1000000'
    
    # Export
    config['EXPORT'] = {}
    config['EXPORT']['directorygpx'] = 'export'
    config['EXPORT']['filenamegpx'] = 'export.gpx'
    config['EXPORT']['directoryimage'] = 'exportpicture'

    # SQLite
    config['SQLITE'] = {}
    config['SQLITE']['database'] = 'database.db'
    
    # Camera v8M 3280x2464 -- v5M 2592x1944
    config['CAMERA'] = {}
    config['CAMERA']['pic_resolution_x'] = '2592'
    config['CAMERA']['pic_resolution_y'] = '1944'
    config['CAMERA']['vid_resolution_x'] = '1920'
    config['CAMERA']['vid_resolution_y'] = '1080'
    config['CAMERA']['framerate'] = '30'
    config['CAMERA']['rotation'] = '0'
    config['CAMERA']['brightness'] = '0'
    config['CAMERA']['contrast'] = '0'
    # negative, solarise, posterize, whiteboard, blackboard, sketch, denoise, emboss, oilpaint, hatch, gpen, pastel, watercolour, film, blur, saturation
    config['CAMERA']['image_effect'] = ''
    # auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks
    config['CAMERA']['exposure_mode'] = 'auto'
    # average, spot, backlit, matrix
    config['CAMERA']['meter_mode'] = 'average'
    # off, auto, sun, cloud, shade, tungsten, fluorescent, incandescent, flash, horizon
    config['CAMERA']['awb'] = 'auto'
    config['CAMERA']['picture_path'] = 'pictures/'
    config['CAMERA']['delay'] = '5'
    config['CAMERA']['nb'] = str(int(((acquisitionDuration * 3600) / float(config['CAMERA']['delay']))))
    
    # GPIO
    config['GPIO'] = {}
    
    # DHT11 interior
    config['GPIO']['DHT11_INTERIOR_PORT'] = '24'
    config['GPIO']['DHT11_INTERIOR_delay'] = '15'
    config['GPIO']['DHT11_INTERIOR_nb'] = str(int(((acquisitionDuration * 3600) / float(config['GPIO']['DHT11_INTERIOR_delay']))))
    
    # DHT11 exterior
    config['GPIO']['DHT11_EXTERIOR_PORT'] = '25'
    config['GPIO']['DHT11_EXTERIOR_delay'] = '15'
    config['GPIO']['DHT11_EXTERIOR_nb'] = str(int(((acquisitionDuration * 3600) / float(config['GPIO']['DHT11_EXTERIOR_delay']))))
    
    # DHT22
    config['GPIO']['DHT22_INTERIOR_PORT'] = '5'
    config['GPIO']['DHT22_INTERIOR_delay'] = '10'
    config['GPIO']['DHT22_INTERIOR_nb'] = str(int(((acquisitionDuration * 3600) / float(config['GPIO']['DHT22_INTERIOR_delay']))))
    
    # DS18B20
    config['GPIO']['DS18B20_1'] = '/sys/bus/w1/devices/w1_bus_master1/28-0416618c01ff/w1_slave'
    config['GPIO']['DS18B20_1_delay'] = '10'
    config['GPIO']['DS18B20_1_nb'] = str(int(((acquisitionDuration * 3600) / float(config['GPIO']['DS18B20_1_delay']))))
    
    config['GPIO']['DS18B20_2'] = ''
    config['GPIO']['DS18B20_2_delay'] = '10'
    config['GPIO']['DS18B20_2_nb'] = str(int(((acquisitionDuration * 3600) / float(config['GPIO']['DS18B20_2_delay']))))
    
    # SR04
    config['GPIO']['SR04_triger_port'] = '22'
    config['GPIO']['SR04_echo_port'] = '27'
    config['GPIO']['SR04_delay'] = '1'
    config['GPIO']['SR04_nb'] = str(int(((acquisitionDuration * 3600) / float(config['GPIO']['SR04_delay']))))
    
    # LED
    config['GPIO']['LED_ACQUISITION'] = '23'
    
    # INPUT
    config['GPIO']['INPUT_ACQUISITION'] = '27'
    
    # GPS
    config['GPS'] = {}
    config['GPS']['delay'] = '0.5'
    config['GPS']['nb'] = str(int(((acquisitionDuration * 3600) / float(config['GPS']['delay']))))
    
    # endregion
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, config_file)
    with open(db_path, 'w') as configfile:
        config.write(configfile)


def getConfig():
    config = configparser.RawConfigParser()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, config_file)
    config.read(db_path)
    return config
