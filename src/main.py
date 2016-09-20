from lib import com_config, com_logger
from acquisition import thread_acquisition_dht11, thread_acquisition_camera

com_config.setConfig()
config = com_config.getConfig()

logger = com_logger.Logger()
logger.log.info('Application start')

# Create new threads
camera_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera Thread", int(config['CAMERA']['delay']), int(config['CAMERA']['nb']))
dht11_thread = thread_acquisition_dht11.ThreadAcquisitionDHT11('DHT11 Exterior', int(config['GPIO']['DHT11_EXTERIOR_delay']), int(config['GPIO']['DHT11_EXTERIOR_nb']))

camera_thread.start()
dht11_thread.start()

logger.log.info('Application stop')

