from acquisition import thread_acquisition_gps
from lib import com_config, com_gps, com_logger

# TODO set config à supprimer
com_config.setConfig()

config = com_config.getConfig()

logger = com_logger.Logger()
logger.log.info('Application start')

# lcd = com_lcd.LCD()

# Init version etc...
# lcd.rectangle(0, 0, lcd.width_max - 1, lcd.height_max - 1)
# lcd.text(3, 1, 'Strato Balloon', lcd.SMALL_FONT)
# lcd.text(3, 14, config['VERSION']['last'], lcd.SMALL_FONT)
# lcd.display()

# Create new threads
# camera_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera Thread", int(config['CAMERA']['delay']), int(config['CAMERA']['nb']))
# dht11_thread_ext = thread_acquisition_dht11.ThreadAcquisitionDHT11('Exterior',
#                                                                   int(config['GPIO']['DHT11_EXTERIOR_PORT']), int(config['GPIO']['DHT11_EXTERIOR_delay']),
#                                                                  int(config['GPIO']['DHT11_EXTERIOR_nb']))
# dht11_thread_int = thread_acquisition_dht11.ThreadAcquisitionDHT11('Interior',
#                                                                   int(config['GPIO']['DHT11_INTERIOR_PORT']), int(config['GPIO']['DHT11_INTERIOR_delay']),
#                                                                   int(config['GPIO']['DHT11_INTERIOR_nb']))

# sr04_thread = thread_acquisition_sr04.ThreadAcquisitionSR04("Présence", int(config['GPIO']['SR04_triger_port']), int(config['GPIO']['SR04_echo_port']),
#                                                            int(config['GPIO']['SR04_delay']), int(config['GPIO']['SR04_nb']))

# TODO add config for gps thread
gps_thread = thread_acquisition_gps.ThreadAcquisitionGPS("GPS", int(config['GPS']['delay']), int(config['GPS']['nb']))
# camera_thread.start()
# dht11_thread_int.start()
# dht11_thread_ext.start()
# sr04_thread.start()
gps_thread.start()


#gps = com_gps.GPS()
#gps.exportToGpx('d:\\file.gpx')

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
