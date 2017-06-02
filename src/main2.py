"""
main.py v 1.1.5
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import threading

from acquisition import thread_acquisition_bme280, thread_acquisition_camera, thread_acquisition_ds18b20, thread_acquisition_mpu9250
from lib import com_config, com_logger
from lib.driver import com_gpio_inout


def startacquisition():
    # Config
    conf = com_config.Config()
    # TODO : Delete for launch
    conf.setconfig()
    config = conf.getconfig()
    
    # Log
    logger = com_logger.Logger()
    logger.info('Application start')
    
    # Waiting for Init acquisition
    gpioinout = com_gpio_inout.GPIOINOT()
    logger.debug('Wait for input acquisition')
    while not gpioinout.getacquisition():
        pass
    
    # Blink LED
    gpioinout.blink(0.2, 5)
    
    logger.info('Start acquition')
    
    threadlock = threading.Lock()
    # Create new threads
    if int(config['RASPBERRY']['number']) == 1:
        camera1_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera N°1", threadlock, 1)
        ds18b20_thread = thread_acquisition_ds18b20.ThreadAcquisitionDS18B20('DS18B20 Ext', threadlock, config['GPIO']['DS18B20_1'], float(config['GPIO'][
                                                                                                                                               'DS18B20_1_delay']), int(config['GPIO']['DS18B20_1_nb']))
        bme280_thread = thread_acquisition_bme280.ThreadAcquisitionBME280('BME280', threadlock, float(config['GPIO']['BME280_delay']), int(config['GPIO']['BME280_nb']))
        mpu9250_thread = thread_acquisition_mpu9250.ThreadAcquisitionMPU9250('GY9250', threadlock, float(config['GPIO']['MPU9250_delay']), int(config['GPIO']['MPU9250_nb']))
        
        # Start Thread
        camera1_thread.start()
        ds18b20_thread.start()
        bme280_thread.start()
        mpu9250_thread.start()
        
        # Wait end for each thread
        camera1_thread.join()
        ds18b20_thread.join()
        bme280_thread.join()
        mpu9250_thread.join()
    
    logger.info('Application stop')
    gpio = com_gpio_inout.GPIOINOT()
    gpio.cleanup()


startacquisition()
