"""
com_config.py v 1.0.2
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import configparser
import os.path

config_file = "config/config.ini"


def setConfig():
    config = configparser.ConfigParser()

    # region Config
    # LOGGER
    config['LOGGER'] = {}
    config['LOGGER']['level'] = '10'
    # Info: DEBUG=10 INFO= 20 WARNING=30 ERROR=40 #CRITICAL=50

    # SQLite
    config['SQLITE'] = {}
    config['SQLITE']['database'] = 'database.db'

    # Camera
    config['CAMERA'] = {}
    config['CAMERA']['pic_resolution_x'] = '3280'
    config['CAMERA']['pic_resolution_y'] = '2464'
    config['CAMERA']['vid_resolution_x'] = '1920'
    config['CAMERA']['vid_resolution_y'] = '1080'
    config['CAMERA']['framerate'] = '30'
    config['CAMERA']['rotation'] = '0'
    config['CAMERA']['brightness'] = '0'
    config['CAMERA']['contrast'] = '0'
    config['CAMERA']['image_effect'] = ''
    config['CAMERA']['exposure_mode'] = ''
    config['CAMERA']['delay'] = '5'
    config['CAMERA']['nb'] = '3'

    # GPIO
    config['GPIO'] = {}
    config['GPIO']['DHT11_INTERIOR_PORT'] = '25'
    config['GPIO']['DHT11_EXTERIOR_PORT'] = '24'
    config['GPIO']['DHT11_INTERIOR_delay'] = '2'
    config['GPIO']['DHT11_INTERIOR_nb'] = '30'
    config['GPIO']['DHT11_EXTERIOR_delay'] = '2'
    config['GPIO']['DHT11_EXTERIOR_nb'] = '30'

    # Directory
    config['DIRECTORY'] = {}
    config['DIRECTORY']['picture_path'] = '/home/pi/'
    # endregion

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, config_file)
    with open(db_path, 'w') as configfile:
        config.write(configfile)


def getConfig():
    config = configparser.RawConfigParser()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, config_file)
    config.read(db_path)
    return config
