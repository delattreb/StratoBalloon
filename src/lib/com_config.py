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

    # LOGGER
    config['LOGGER'] = {}
    config['LOGGER']['level'] = '10'
    # Info: DEBUG=10 INFO= 20 WARNING=30 ERROR=40 #CRITICAL=50

    # EMAIL
    config['EMAIL'] = {}
    config['EMAIL']['from'] = 'delattreb@gmail.com'
    config['EMAIL']['to'] = 'delattreb@gmail.com'
    config['EMAIL']['password'] = '!KillBill100!'
    config['EMAIL']['username'] = 'delattreb'

    # SQLite
    config['SQLITE'] = {}
    config['SQLITE']['database'] = 'database.db'

    # Camera
    config['CAMERA'] = {}
    config['CAMERA']['resolution_x'] = '2592'
    config['CAMERA']['resolution_y'] = '1944'
    config['CAMERA']['framerate'] = '30'
    config['CAMERA']['rotation'] = '0'
    config['CAMERA']['brightness'] = '0'
    config['CAMERA']['contrast'] = '0'
    config['CAMERA']['image_effect'] = ''
    config['CAMERA']['exposure_mode'] = ''

    # Directory
    config['DIRECTORY'] = {}
    config['DIRECTORY']['picture_path'] = 'c:\\'

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
