"""
main.py v 1.1.5
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import threading
import time

from acquisition import thread_acquisition_bme280, thread_acquisition_dht22, thread_acquisition_gy9250
from lib import com_config, com_lcd, com_logger
from lib.driver import com_gpio_inout

# TODO try catch on all thread acquisition

# Config
conf = com_config.Config()
conf.setconfig()
config = conf.getconfig()

# Log
logger = com_logger.Logger()
logger.info('Application start')

# LCD
lcd = com_lcd.LCD()

# LCD Splash
lcd.splash()

# Waiting for GPS Fix
logger.debug('Wait for GPS Fix')
lcd.displaygpsinformation()
time.sleep(3)

gpioinout = com_gpio_inout.GPIOINOT()
# Waiting for Init acquisition

while not gpioinout.getacquisition():
    logger.info('Wait for input acquisition')
    lcd.displaysensor()
    time.sleep(3)

gpioinout.blink(0.2, 10)

logger.info('Wait for trigger')
lcd.displaystartacquisition()
logger.info('Start acquition')

# Create new threads
threadlock = threading.Lock()

# camera_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera Thread", threadlock, float(config['CAMERA']['delay']), int(config['CAMERA']['nb']))

# ds18b20_thread_int = thread_acquisition_ds18b20.ThreadAcquisitionDS18B20('DS18B20 Ext', threadlock, config['GPIO']['DS18B20_1'], float(config['GPIO'][
#                                                                                                                                          'DS18B20_1_delay']),
#                                                                       int(config['GPIO']['DS18B20_1_nb']))

bme280_thread_int = thread_acquisition_bme280.ThreadAcquisitionBME280('BME280', threadlock, int(config['GPIO']['BME280_bus']), int(config['GPIO']['BME280_i2caddr']),
                                                                      float(config['GPIO']['BME280_delay']), int(config['GPIO']['BME280_nb']))

gy9250_thread_int = thread_acquisition_gy9250.ThreadAcquisitionGY9250('GY9250', threadlock, int(config['GPIO']['GY9250_mpu_addr']), int(config['GPIO']['GY9250_mag_addr']),
                                                                      int(config['GPIO']['GY9250_chipid']), float(config['GPIO']['BME280_delay']),
                                                                      int(config['GPIO']['BME280_nb']))

# TODO be carrefull output for DHT22 and output to blink manually
dht22_thread_int = thread_acquisition_dht22.ThreadAcquisitionDHT22('Interior', threadlock,
                                                                   int(config['GPIO']['DHT22_INTERIOR_PORT']), int(config['GPIO']['DHT22_INTERIOR_delay']),
                                                                   int(config['GPIO']['DHT22_INTERIOR_nb']), int(config['GPIO']['DHT22_LED_ACQUISITION']))

# gps_thread = thread_acquisition_gps.ThreadAcquisitionGPS("GPS", threadlock, float(config['GPS']['delay']), int(config['GPS']['nb']))

# camera_thread.start()
# ds18b20_thread_int.start()
dht22_thread_int.start()
# gps_thread.start()

# Wait end for each thread
# camera_thread.join()
# ds18b20_thread_int.join()
dht22_thread_int.join()
# gps_thread.join()

logger.info('Application stop')
gpio = com_gpio_inout.GPIOINOT()
gpio.cleanup()
