import lcd

from lib import com_config, com_gpio_inout, com_logger

# Config
# TODO set config à supprimer
com_config.setConfig()
config = com_config.getConfig()

# Log
logger = com_logger.Logger()
logger.log.info('Application start')

# LCD Splash
lcd.splash()

# Waiting for acquisition
logger.log.debug('Wait for acquisition Input')
gpioinout = com_gpio_inout.GPIOINOT()
while not gpioinout.getacquisition():
    lcd.displayInformation()

gpioinout.blink(5)

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

# sr04_thread = thread_acquisition_sr04.ThreadAcquisitionSR04("Présence", int(config['GPIO']['SR04_triger_port']), int(config['GPIO']['SR04_echo_port']),
#                                                            int(config['GPIO']['SR04_delay']), int(config['GPIO']['SR04_nb']))

# TODO reprendre les paramètres de config
# gps_thread = thread_acquisition_gps.ThreadAcquisitionGPS("GPS", config['GPS']['delay'], config['GPS']['nb'])
# camera_thread.start()
# dht11_thread_int.start()
# dht11_thread_ext.start()
# dht22_thread_int.start()
# sr04_thread.start()
# gps_thread.start()
# ds18b20_thread_int.start()

"""
gps = com_gps.GPS()
gps.getLocalisation()

if gps.response != None:
    print("Mode:" + str(gps.mode))
    if gps.response.mode >= 2:
        print("ERROR:" + str(gps.error))
        print("lat:" + str(gps.latitude))
        print("lon:" + str(gps.longitude))
        print("time:" + gps.timeutc)
    if gps.response.mode >= 3:
        # climb
        print("alt:" + str(gps.altitude))
"""

logger.log.info('Application stop')
gpioinout.cleanup()
