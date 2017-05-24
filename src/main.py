"""
main.py v 1.1.5
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import threading
from time import sleep

from acquisition import thread_acquisition_camera, thread_acquisition_dht22, thread_acquisition_ds18b20, thread_acquisition_gps, thread_acquisition_mpu9250
from lib import com_config, com_lcd, com_logger, com_network
from lib.driver import com_gpio_inout, com_gps


class Main:
    def __init__(self):
        # Config
        conf = com_config.Config()
        # TODO delete before run : Set number of Raspberry
        conf.setconfig()
        self.config = conf.getconfig()
        
        # Log
        self.logger = com_logger.Logger()
        self.logger.info('Application start')
        
        # LCD
        self.lcd = com_lcd.LCD()
        
        # GPS
        self.gps = com_gps.GPS()
        
        # NETWORK
        self.network = com_network.NETWORK()
    
    def startacquisition(self):
        # LCD Splash
        self.lcd.splash(self.config['LOGGER']['levelconsole'], self.config['APPLICATION']['name'], self.config['APPLICATION']['author'], 'v' + self.config['APPLICATION']['version'])
        
        # Waiting for GPS Fix
        self.logger.debug('Wait for GPS Fix')
        
        init = False
        while not init:
            self.gps.getlocalisation(0, 0, False)
            self.lcd.displaygpsinformation(self.gps.mode, self.gps.longitude, self.gps.latitude, self.gps.altitude, self.gps.lonprecision, self.gps.latprecision, self.gps.altprecision, self.gps.hspeed, self.gps.sats,
                                           self.gps.track)
            init = self.network.settime(self.gps.mode, str(self.gps.timeutc[:-5].replace('T', ' ').replace('Z', '')))

        # Waiting for Init acquisition
        gpioinout = com_gpio_inout.GPIOINOT()
        self.logger.debug('Wait for input acquisition')
        while not gpioinout.getacquisition():
            self.gps.getlocalisation(0, 0, False)
            self.lcd.displaygpsinformation(self.gps.mode, self.gps.longitude, self.gps.latitude, self.gps.altitude, self.gps.lonprecision, self.gps.latprecision, self.gps.altprecision, self.gps.hspeed, self.gps.sats,
                                           self.gps.track)
            # lcd.displaysensor()
            sleep(3)
        
        # Blink LED
        gpioinout.blink(0.2, 5)
        
        # Display trigger and switch off lcd display
        self.logger.info('Count down')
        self.lcd.displaystart(int(self.config['ACQUISITION']['trigger']))
        self.logger.info('Switch off LCD')
        self.lcd.displayoff()
        self.logger.info('Start acquition')
        
        threadlock = threading.Lock()
        # Create new threads
        if int(self.config['RASPBERRY']['number']) == 1:
            # LCD
            camera1_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera N°1", threadlock, 1)
            ds18b20_thread = thread_acquisition_ds18b20.ThreadAcquisitionDS18B20('DS18B20 Ext', threadlock, self.config['GPIO']['DS18B20_1'], float(self.config['GPIO'][
                                                                                                                                                        'DS18B20_1_delay']), int(self.config['GPIO']['DS18B20_1_nb']))
            mpu9250_thread = thread_acquisition_mpu9250.ThreadAcquisitionMPU9250('GY9250', threadlock, float(self.config['GPIO']['MPU9250_delay']), int(self.config['GPIO']['MPU9250_nb']))
            dht22_thread = thread_acquisition_dht22.ThreadAcquisitionDHT22('Interior', threadlock,
                                                                           int(self.config['GPIO']['DHT22_INTERIOR_PORT']), int(self.config['GPIO']['DHT22_INTERIOR_delay']),
                                                                           int(self.config['GPIO']['DHT22_INTERIOR_nb']), int(self.config['GPIO']['DHT22_LED_ACQUISITION']))
            # Start Thread
            camera1_thread.start()
            ds18b20_thread.start()
            mpu9250_thread.start()
            dht22_thread.start()
            # Wait end for each thread
            camera1_thread.join()
            ds18b20_thread.join()
            mpu9250_thread.join()
            dht22_thread.join()
        
        # Create new threads
        if int(self.config['RASPBERRY']['number']) == 2:
            camera2_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera N°2", threadlock, 2)
            # bme280_thread = thread_acquisition_bme280.ThreadAcquisitionBME280('BME280', threadlock, float(config['GPIO']['BME280_delay']), int(config['GPIO']['BME280_nb']))
            gps_thread = thread_acquisition_gps.ThreadAcquisitionGPS("GPS", threadlock, float(self.config['GPS']['delay']), int(self.config['GPS']['nb']))
            # Start Thread
            camera2_thread.start()
            # bme280_thread.start()
            gps_thread.start()
            # Wait end for each thread
            # camera2_thread.join()
            # bme280_thread.join()
            # gps_thread.join()
        
        self.logger.info('Application stop')
        gpio = com_gpio_inout.GPIOINOT()
        gpio.cleanup()


main = Main()
main.startacquisition()
