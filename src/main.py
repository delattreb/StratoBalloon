from dal import dal_dht11
from lib import com_config, com_logger

from lib import com_gpio

# config = com_config.setConfig()
config = com_config.getConfig()
logger = com_logger.Logger()
logger.log.info('Application start')

# Create new threads
#camera_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera Thread", config['GPIO']['DHT11_EXTERIOR_delay'], config['GPIO']['DHT11_EXTERIOR_nb'])
# camera_thread.start()

logger.log.info('Application stop')

gpio = com_gpio.GPIO()
gpio.setmodeBCM()
gpio.setupIO(25,gpio.IN)
print(gpio.getIO(25))

