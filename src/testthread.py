import sqlite3
import threading
import time

from dal import dal_camera, dal_picture
from lib import com_config, com_logger


class Thread1(threading.Thread):
    def __init__(self, name, lock, counter, delay):
        super().__init__()
        self.name = name
        self.counter = counter
        self.delay = delay
        self.lock = lock
    
    def run(self):
        self.job(self.counter, self.delay)
    
    def job(self, counter, delay):
        while counter:
            logger.debug(self.name)
            self.lock.acquire()
            
            config = com_config.getConfig()
            connection = sqlite3.Connection(config['SQLITE']['database'])
            cursor = connection.cursor()
            
            dalcamera = dal_camera.DAL_Camera(connection, cursor)
            index = dalcamera.get_last_picture_id()
            dalcamera.set_last_picture_id(index + 1)
            
            dalpicture = dal_picture.DAL_Picture(connection, cursor)
            dalpicture.setpicture(self.name)
            
            time.sleep(delay)
            counter -= 1
            self.lock.release()


class Thread2(threading.Thread):
    def __init__(self, name, lock, counter, delay):
        super().__init__()
        self.name = name
        self.counter = counter
        self.delay = delay
        self.lock = lock
    
    def run(self):
        self.job(self.counter, self.delay)
    
    def job(self, counter, delay):
        while counter:
            logger.debug(self.name)
            self.lock.acquire()
            
            config = com_config.getConfig()
            connection = sqlite3.Connection(config['SQLITE']['database'])
            cursor = connection.cursor()
            
            dal = dal_camera.DAL_Camera(connection, cursor)
            index = dal.get_last_picture_id()
            dal.set_last_picture_id(index + 1)
            
            dalpicture = dal_picture.DAL_Picture(connection, cursor)
            dalpicture.setpicture(self.name)
            
            time.sleep(delay)
            counter -= 1
            self.lock.release()


com_config.setConfig()
com_config.setConfig()
config = com_config.getConfig()

logger = com_logger.Logger('Thread')

logger.info('message is info')
logger.debug('message is debug')
logger.warning('message is warning')
logger.error('message is error')
logger.critical('message is critical')

threadlock = threading.Lock()

t1 = Thread1('t1', threadlock, 10, 0)
t2 = Thread1('t2', threadlock, 10, 0)
t3 = Thread1('t3', threadlock, 10, 0)

t4 = Thread2('t4', threadlock, 10, 0)
t5 = Thread2('t5', threadlock, 10, 0)
t6 = Thread2('t6', threadlock, 10, 0)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
