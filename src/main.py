"""
main.py v 1.1.5
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import threading

from acquisition import thread_acquisition_bme280, thread_acquisition_camera, thread_acquisition_ds18b20, thread_acquisition_gps, thread_acquisition_mpu9250
from lib import com_config, com_lcd, com_logger, com_network
from lib.driver import com_gpio_inout, com_gps


def startacquisition():
    # Config
    conf = com_config.Config()
    # TODO : Delete for launch
    conf.setconfig()
    config = conf.getconfig()
    
    # Log
    logger = com_logger.Logger()
    logger.info('Application start')
    
    # LCD
    lcd = com_lcd.LCD()
    
    # GPS
    gps = com_gps.GPS()
    
    # NETWORK
    network = com_network.NETWORK()
    
    # LCD Splash
    lcd.splash(config['LOGGER']['levelconsole'], config['APPLICATION']['name'], config['APPLICATION']['author'], 'v' + config['APPLICATION']['version'])
    
    # Waiting for GPS Fix
    logger.debug('Wait for GPS Fix')
    
    init = False
    while not init:
        gps.getlocalisation(0, 0, False)
        lcd.displaygpsinformation(gps.mode, gps.longitude, gps.latitude, gps.altitude, gps.lonprecision, gps.latprecision, gps.altprecision, gps.hspeed, gps.sats,
                                  gps.track)
        init = network.settime(gps.mode, str(gps.timeutc[:-5].replace('T', ' ').replace('Z', '')))
    
    # Waiting for Init acquisition
    gpioinout = com_gpio_inout.GPIOINOT()
    logger.debug('Wait for input acquisition')
    while not gpioinout.getacquisition():
        gps.getlocalisation(0, 0, False)
        lcd.displaygpsinformation(gps.mode, gps.longitude, gps.latitude, gps.altitude, gps.lonprecision, gps.latprecision, gps.altprecision, gps.hspeed, gps.sats,
                                  gps.track)
        # lcd.displaysensor()
    
    # Blink LED
    gpioinout.blink(0.2, 5)
    
    # Display trigger and switch off lcd display
    logger.info('Count down')
    lcd.displaystart(int(config['ACQUISITION']['trigger']))
    logger.info('Switch off LCD')
    lcd.displayoff()
    logger.info('Start acquition')
    
    threadlock = threading.Lock()
    # Create new threads
    if int(config['RASPBERRY']['number']) == 1:
        camera1_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera N°1", threadlock, 1)
        ds18b20_thread = thread_acquisition_ds18b20.ThreadAcquisitionDS18B20('DS18B20 Ext', threadlock, config['GPIO']['DS18B20_1'], float(config['GPIO'][
                                                                                                                                               'DS18B20_1_delay']), int(config['GPIO']['DS18B20_1_nb']))
        bme280_thread = thread_acquisition_bme280.ThreadAcquisitionBME280('BME280', threadlock, float(config['GPIO']['BME280_delay']), int(config['GPIO']['BME280_nb']))
        mpu9250_thread = thread_acquisition_mpu9250.ThreadAcquisitionMPU9250('GY9250', threadlock, float(config['GPIO']['MPU9250_delay']), int(config['GPIO']['MPU9250_nb']))
        # dht22_thread = thread_acquisition_dht22.ThreadAcquisitionDHT22('Interior', threadlock,
        #                                                               int(config['GPIO']['DHT22_INTERIOR_PORT']), int(config['GPIO']['DHT22_INTERIOR_delay']),
        #                                                               int(config['GPIO']['DHT22_INTERIOR_nb']), int(config['GPIO']['DHT22_LED_ACQUISITION']))
        # Start Thread
        camera1_thread.start()
        ds18b20_thread.start()
        bme280_thread.start()
        mpu9250_thread.start()
        # dht22_thread.start()
        # Wait end for each thread
        camera1_thread.join()
        ds18b20_thread.join()
        bme280_thread.join()
        mpu9250_thread.join()
        # dht22_thread.join()
    
    # Create new threads
    if int(config['RASPBERRY']['number']) == 2:
        camera2_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera N°2", threadlock, 2)
        gps_thread = thread_acquisition_gps.ThreadAcquisitionGPS("GPS", threadlock, float(config['GPS']['delay']), int(config['GPS']['nb']))
        # Start Thread
        camera2_thread.start()
        gps_thread.start()
        # Wait end for each thread
        camera2_thread.join()
        gps_thread.join()
    
    logger.info('Application stop')
    gpio = com_gpio_inout.GPIOINOT()
    gpio.cleanup()


startacquisition()
