from lib import com_logger
from thread import thread_acquisition_camera

# config = com_config.setConfig()

logger = com_logger.Logger()
logger.log.info('Application start')

# Create new threads
camera_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera Thread", 5)

# Start new Threads
camera_thread.start()

logger.log.info('Application stop')
