"""
com_camera.py v1.0.1
Auteur: Bruno DELATTRE
Date : 15/09/2016
"""

# Source https://www.raspberrypi.org/learning/getting-started-with-picamera/worksheet/

try:
    from picamera import PiCamera
except Exception as exp:
    PiCamera = None
from time import sleep

from dal import dal_camera, dal_picture
from lib import com_config, com_logger


def is_plugged(function):
    def plugged(*original_args, **original_kwargs):
        return function(*original_args, **original_kwargs)
    
    if not PiCamera:
        logger = com_logger.Logger('CAMERA')
        logger.warning('Camera not plugged')
    
    return plugged


class Camera:
    @is_plugged
    def __init__(self, mode, cameranumber):
        if PiCamera is not None:
            self.imgName = 'PIC_'
            self.vidName = 'VID_'
            self.cameranumber = cameranumber
            
            conf = com_config.Config()
            config = conf.getconfig()
            logger = com_logger.Logger(self.cameranumber)
            
            self.camera = PiCamera()
            if mode == 'PICTURE':
                self.camera.resolution = (int(config[self.cameranumber]['pic_resolution_x']), int(config[self.cameranumber]['pic_resolution_y']))
                logger.info('Camera mode PICTURE: ' + config[self.cameranumber]['pic_resolution_x'] + ' ' + config[self.cameranumber]['pic_resolution_y'])
            if mode == 'VIDEO':
                self.camera.resolution = (int(config[self.cameranumber]['vid_resolution_x']), int(config[self.cameranumber]['vid_resolution_y']))
                logger.debug('Camera mode VIDEO: ' + config[self.cameranumber]['vid_resolution_x'] + ' ' + config[self.cameranumber]['vid_resolution_y'])
                self.camera.framerate = int(config[self.cameranumber]['framerate'])

            self.camera.rotation = int(config[self.cameranumber]['rotation'])
            # self.camera.brightness = int(config[self.cameranumber]['brightness'])
            # self.camera.contrast = int(config[self.cameranumber]['contrast'])
            if len(config[self.cameranumber]['image_effect']) > 0:
                self.camera.image_effect = config[self.cameranumber]['image_effect']
            self.camera.exposure_mode = config[self.cameranumber]['exposure_mode']
            self.camera.meter_mode = config[self.cameranumber]['meter_mode']
            self.camera.awb_mode = config[self.cameranumber]['awb']
            self.camera.raw_format = config[self.cameranumber]['raw']
            self.path = config[self.cameranumber]['picture_path']
            self.camera.iso = int(config[self.cameranumber]['ISO'])
            self.quality = int(config[self.cameranumber]['jpegquality'])
    
    def getpicture(self, connection, cursor):
        if PiCamera is not None:
            dalcamera = dal_camera.DAL_Camera(connection, cursor)
            dalpicture = dal_picture.DAL_Picture(connection, cursor)
            
            index = dalcamera.get_last_picture_id()
            name = self.path + self.imgName + str(index) + '.jpg'
            # self.camera.start_preview()
            # sleep(2)
            self.camera.capture(name, bayer = True, quality = self.quality)
            
            dalcamera.set_last_picture_id(index + 1)
            dalpicture.setpicture(name)

            logger = com_logger.Logger(self.cameranumber)
            logger.info('Picture taken:' + name)

    def getvideo(self, duration, connection, cursor):
        if PiCamera is not None:
            dal = dal_camera.DAL_Camera(connection, cursor)
            dalpicture = dal_picture.DAL_Picture(connection, cursor)
            
            index = dal.get_last_video_id()
            name = self.path + self.vidName + str(index) + '.h264'
            self.camera.start_recording(name)
            sleep(duration)
            self.camera.stop_recording()
            
            dal.set_last_video_id(index + 1)
            dalpicture.setvideo(name)

            logger = com_logger.Logger(self.cameranumber)
            logger.debug('Video taken: ' + name)
