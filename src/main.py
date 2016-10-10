from acquisition import thread_acquisition_gps
from lib import com_config, com_gps, com_logger

# TODO set config à supprimer
com_config.setConfig()

config = com_config.getConfig()

logger = com_logger.Logger()
logger.log.info('Application start')

#dal_gps.DAL_GPS().delCoordinate()

gps = com_gps.GPS()
gps.getGoogleMapsImages('d:\\image\\', 'img', 18, 640, 300, 3, True, 4, 20)
# gps.exportToGpx('d:\\file.gpx', 'Strato Ballon Trace')


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

gps_thread = thread_acquisition_gps.ThreadAcquisitionGPS("GPS", float(config['GPS']['delay']), int(config['GPS']['nb']))
# camera_thread.start()
# dht11_thread_int.start()
# dht11_thread_ext.start()
# sr04_thread.start()
gps_thread.start()

logger.log.info('Application stop')
