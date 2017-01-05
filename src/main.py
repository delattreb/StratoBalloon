"""
main.py v 1.1.5
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import threading
from time import sleep

from acquisition import thread_acquisition_bme280, thread_acquisition_camera, thread_acquisition_dht22, thread_acquisition_ds18b20, thread_acquisition_gps, thread_acquisition_mpu9250
from lib import com_config, com_lcd, com_logger
from lib.driver import com_gpio_inout

# Config
conf = com_config.Config()
# TODO delete before run : Set number of Raspberry
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
sleep(3)

gpioinout = com_gpio_inout.GPIOINOT()
# Waiting for Init acquisition
while not gpioinout.getacquisition():
    logger.info('Wait for input acquisition')
    lcd.displaysensor()
    sleep(3)

# Blink LED
gpioinout.blink(0.2, 10)

logger.info('Wait for trigger')
lcd.displaystartacquisition()
logger.info('Start acquition')

threadlock = threading.Lock()
# Create new threads
if config['RASPBERRY']['number'] == 1:
    # LCD
    camera1_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera N°1", threadlock, float(config['CAMERA1']['delay']), int(config['CAMERA1']['nb']))
    ds18b20_thread = thread_acquisition_ds18b20.ThreadAcquisitionDS18B20('DS18B20 Ext', threadlock, config['GPIO']['DS18B20_1'], float(config['GPIO'][
                                                                                                                                           'DS18B20_1_delay']), int(config['GPIO']['DS18B20_1_nb']))
    mpu9250_thread = thread_acquisition_mpu9250.ThreadAcquisitionMPU9250('GY9250', threadlock, float(config['GPIO']['MPU9250_delay']), int(config['GPIO']['MPU9250_nb']))
    dht22_thread = thread_acquisition_dht22.ThreadAcquisitionDHT22('Interior', threadlock,
                                                                   int(config['GPIO']['DHT22_INTERIOR_PORT']), int(config['GPIO']['DHT22_INTERIOR_delay']),
                                                                   int(config['GPIO']['DHT22_INTERIOR_nb']), int(config['GPIO']['DHT22_LED_ACQUISITION']))
    # Start Thread
    camera1_thread.start()
    ds18b20_thread.start()
    mpu9250_thread.start()
    dht22_thread.start()

# Create new threads
if config['RASPBERRY']['number'] == 2:
    camera2_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera N°2", threadlock, float(config['CAMERA2']['delay']), int(config['CAMERA2']['nb']))
    bme280_thread = thread_acquisition_bme280.ThreadAcquisitionBME280('BME280', threadlock, int(config['GPIO']['BME280_bus']), int(config['GPIO']['BME280_i2caddr']),
                                                                      float(config['GPIO']['BME280_delay']), int(config['GPIO']['BME280_nb']))
    gps_thread = thread_acquisition_gps.ThreadAcquisitionGPS("GPS", threadlock, float(config['GPS']['delay']), int(config['GPS']['nb']))
    # Start Thread
    camera2_thread.start()
    bme280_thread.start()
    gps_thread.start()

# Wait end for each thread
"""
camera1_thread.join()
camera2_thread.join()
ds18b20_thread.join()
bme280_thread.join()
mpu9250_thread.join()
dht22_thread.join()
gps_thread.join()
"""

logger.info('Application stop')
gpio = com_gpio_inout.GPIOINOT()
gpio.cleanup()
