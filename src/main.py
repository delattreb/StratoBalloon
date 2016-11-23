"""
main.py v 1.1.5
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

"""
Post traitement des dates
SELECT datetime(date,'+1 hours','+5 minutes') from coordinate;
select datetime("now", 'localtime')

"""

import threading
import sqlite3

from acquisition import thread_acquisition_camera, thread_acquisition_dht22, thread_acquisition_ds18b20, thread_acquisition_gps
from lib import com_config, com_gpio_inout, com_logger

# Config
com_config.setConfig()
config = com_config.getConfig()

# Log
logger = com_logger.Logger()
logger.info('Application start')

# LCD
# lcd = lcd.LCD()

# LCD Splash
# lcd.splash()

"""
# Waiting for GPS acquisition
logger.debug('Wait for GPS Fix')
gpioinout = com_gpio_inout.GPIOINOT()
while not gpioinout.getacquisition():
    lcd.displayGPSInformation()
time.sleep(3)

# Waiting for Init acquisition
logger.debug('Wait for input acquisition')
gpioinout = com_gpio_inout.GPIOINOT()
while not gpioinout.getacquisition():
    lcd.displatSensor()
gpioinout.blink(0.2, 10)
lcd.displayStartAcquisition()
time.sleep(int(config['APPLICATION']['trigger']))
lcd.displayOff()
"""

#Database connection


# Create new threads
threadlock = threading.Lock()

camera_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera Thread",threadlock, float(config['CAMERA']['delay']), int(config['CAMERA']['nb']))

ds18b20_thread_int = thread_acquisition_ds18b20.ThreadAcquisitionDS18B20('DS18B20 Ext', threadlock,config['GPIO']['DS18B20_1'], float(config['GPIO']['DS18B20_1_delay']),
                                                                         int(config['GPIO']['DS18B20_1_nb']) )

# TODO Lance pigiopd pour lire le capteur DHT22
dht22_thread_int = thread_acquisition_dht22.ThreadAcquisitionDHT22('Interior',threadlock,
                                                                   int(config['GPIO']['DHT22_INTERIOR_PORT']), int(config['GPIO']['DHT22_INTERIOR_delay']),
                                                                   int(config['GPIO']['DHT22_INTERIOR_nb']) )

gps_thread = thread_acquisition_gps.ThreadAcquisitionGPS("GPS", float(config['GPS']['delay']), int(config['GPS']['nb']) )

# dht11_thread_ext = thread_acquisition_dht11.ThreadAcquisitionDHT11('Exterior',threadlock,
#                                                                   int(config['GPIO']['DHT11_EXTERIOR_PORT']), float(config['GPIO']['DHT11_EXTERIOR_delay']),
#                                                                  int(config['GPIO']['DHT11_EXTERIOR_nb']))

# dht11_thread_int = thread_acquisition_dht11.ThreadAcquisitionDHT11('Interior',threadlock,
#                                                                   int(config['GPIO']['DHT11_INTERIOR_PORT']), float(config['GPIO']['DHT11_INTERIOR_delay']),
#                                                                   int(config['GPIO']['DHT11_INTERIOR_nb']))

camera_thread.start()
ds18b20_thread_int.start()
dht22_thread_int.start()
gps_thread.start()
# sr04_thread.start()
# dht11_thread_int.start()
# dht11_thread_ext.start()


# Wait end for each thread
#camera_thread.join()
#ds18b20_thread_int.join()
#dht22_thread_int.join()()
#gps_thread.join()
# sr04_thread.join()()
# dht11_thread_int.join()
# dht11_thread_ext.join()()

logger.info('Application stop')
gpio = com_gpio_inout.GPIOINOT()
gpio.cleanup()
