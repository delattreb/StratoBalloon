"""
com_camera.py v1.0.1
Auteur: Bruno DELATTRE
Date : 15/09/2016
"""

# Source https://www.raspberrypi.org/learning/getting-started-with-picamera/worksheet/

try:
    from picamera import PiCamera
except:
    PiCamera = None

import datetime
from time import sleep

from dal import dal_video
from lib import com_config, com_logger


def is_plugged(function):
    def plugged(*original_args, **original_kwargs):
        return function(*original_args, **original_kwargs)
    
    if not PiCamera:
        logger = com_logger.Logger('CAMERA')
        logger.log.warning('Camera not plugged')
    
    return plugged


class Camera:
    @is_plugged
    def __init__(self, mode):
        if PiCamera != None:
            self.imgName = 'PIC_'
            self.vidName = 'VID_'
            
            config = com_config.getConfig()
            logger = com_logger.Logger('CAMERA')
            
            self.camera = PiCamera()
            if mode == 'PICTURE':
                self.camera.resolution = (int(config['CAMERA']['pic_resolution_x']), int(config['CAMERA']['pic_resolution_y']))
                logger.log.debug('Init Camera mode PICTURE: ' + config['CAMERA']['pic_resolution_x'] + ' ' + config['CAMERA']['pic_resolution_y'])
            if mode == 'VIDEO':
                self.camera.resolution = (int(config['CAMERA']['vid_resolution_x']), int(config['CAMERA']['vid_resolution_y']))
                logger.log.debug('Init Camera mode VIDEO: ' + config['CAMERA']['vid_resolution_x'] + ' ' + config['CAMERA']['vid_resolution_y'])
                self.camera.framerate = int(config['CAMERA']['framerate'])
            
            self.camera.rotation = config['CAMERA']['rotation']
            # self.camera.brightness = config['CAMERA']['brightness']
            # self.camera.contrast = config['CAMERA']['contrast']
            # self.camera.image_effect = config['CAMERA']['image_effect']
            # self.camera.exposure_mode = config['CAMERA']['exposure_mode']
            self.path = config['CAMERA']['picture_path']
    
    
    def getPicture(self, dalcamera, dalpicture):
        if PiCamera != None:
            id = dalcamera.get_last_picture_id()
            name = self.path + self.imgName + str(id) + '.jpg'
            #self.camera.capture(name) #TODO comment

            dalcamera.set_last_picture_id(id + 1)
            dalpicture.setpicture(name, str(datetime.datetime.now()))
            
            logger = com_logger.Logger('CAMERA')
            logger.log.debug('Picture taken:' + name)
    
    def getVideo(self, duration: int, dal):
        if PiCamera != None:
            id = dal.get_last_video_id()
            name = self.path + self.vidName + str(id) + '.h264'
            self.camera.start_recording(name)
            sleep(duration)
            self.camera.stop_recording()
            dal.set_last_video_id(id + 1)
            
            dal.setvideo(name, str(datetime.datetime.now()))
            
            logger = com_logger.Logger('CAMERA')
            logger.log.debug('Video taken: ' + name)
