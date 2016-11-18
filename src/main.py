import lcd, time

from lib import com_config, com_gpio_inout, com_logger

# Config
# TODO set config à supprimer
com_config.setConfig()
config = com_config.getConfig()

# Log
logger = com_logger.Logger()
logger.log.info('Application start')

# LCD
lcd = lcd.LCD()

# LCD Splash
lcd.splash()

# Waiting for GPS acquisition
logger.log.debug('Wait for GPS Fix')
gpioinout = com_gpio_inout.GPIOINOT()
while not gpioinout.getacquisition():
    lcd.displayGPSInformation()
gpioinout.blink(0.1, 2)

# Waiting for Init acquisition
logger.log.debug('Wait for input acquisition')
gpioinout = com_gpio_inout.GPIOINOT()
while not gpioinout.getacquisition():
    lcd.displatSensor()
lcd.displayStartAcquisition()
gpioinout.blink(0.1,10)
lcd.displayOff()
time.sleep(int(config['APPLICATION']['trigger']))

# Create new threads
# ds18b20_thread_int = thread_acquisition_ds18b20.ThreadAcquisitionDS18B20('Exterior', config['GPIO']['DS18B20_1'], int(config['GPIO']['DS18B20_1_delay']),
#                                                                         int(config['GPIO']['DS18B20_1_nb']))

# camera_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera Thread", int(config['CAMERA']['delay']), int(config['CAMERA']['nb']))

# dht11_thread_ext = thread_acquisition_dht11.ThreadAcquisitionDHT11('Exterior',
#                                                                   int(config['GPIO']['DHT11_EXTERIOR_PORT']), int(config['GPIO']['DHT11_EXTERIOR_delay']),
#                                                                  int(config['GPIO']['DHT11_EXTERIOR_nb']))

# dht11_thread_int = thread_acquisition_dht11.ThreadAcquisitionDHT11('Interior',
#                                                                   int(config['GPIO']['DHT11_INTERIOR_PORT']), int(config['GPIO']['DHT11_INTERIOR_delay']),
#                                                                   int(config['GPIO']['DHT11_INTERIOR_nb']))

# TODO Lance pigiopd pour livre le capteur DHT22
# dht22_thread_int = thread_acquisition_dht22.ThreadAcquisitionDHT22('Interior',
#                                                                   int(config['GPIO']['DHT22_INTERIOR_PORT']), int(config['GPIO']['DHT22_INTERIOR_delay']),
#                                                                   int(config['GPIO']['DHT22_INTERIOR_nb']))

# TODO reprendre les paramètres de config
# gps_thread = thread_acquisition_gps.ThreadAcquisitionGPS("GPS", config['GPS']['delay'], config['GPS']['nb'])
# camera_thread.start()
# dht11_thread_int.start()
# dht11_thread_ext.start()
# dht22_thread_int.start()
# sr04_thread.start()
# gps_thread.start()
# ds18b20_thread_int.start()

logger.log.info('Application stop')
gpioinout.cleanup()
