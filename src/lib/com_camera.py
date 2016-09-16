"""
com_camera.py v1.0.0
Auteur: Bruno DELATTRE
Date : 15/09/2016
"""

# Source https://www.raspberrypi.org/learning/getting-started-with-picamera/worksheet/

try:
    from picamera import PiCamera
except:
    PiCamera = None

from time import sleep

from dal import dal_camera
from lib import com_config
from lib import com_logger


def is_camera_plugged(fonction, *param, **param2):
    def not_plugged(self, *param, **param2):
        logger = com_logger.Logger('CAMERA')
        logger.log.debug('Camera not plugged')

    if not PiCamera:
        return not_plugged

    return fonction(*param, **param2)

class Camera:
    @is_camera_plugged
    def __init__(self):
        config = com_config.getConfig()

        self.camera = PiCamera()
        self.camera.resolution = (int(config['CAMERA']['resolution_x']), int(config['CAMERA']['resolution_y']))
        self.camera.framerate = config['CAMERA']['framerate']
        self.camera.rotation = config['CAMERA']['rotation']
        self.camera.brightness = config['CAMERA']['brightness']
        self.camera.contrast = config['CAMERA']['contrast']
        self.camera.image_effect = config['CAMERA']['image_effect']
        self.camera.exposure_mode = config['CAMERA']['exposure_mode']

    @is_camera_plugged
    def __get_last_picture_id(self):
        d = dal_camera.DAL_Camera()
        return d.get_last_picture_id()

    @is_camera_plugged
    def __set_last_picture_id(self, value):
        d = dal_camera.DAL_Camera()
        d.set_last_picture_id(value)

    @is_camera_plugged
    def __get_last_video_id(self):
        d = dal_camera.DAL_Camera()
        return d.get_last_video_id()

    @is_camera_plugged
    def __set_last_video_id(self, value):
        d = dal_camera.DAL_Camera()
        d.set_last_picture_id(value)

    @is_camera_plugged
    def getPicture(self, path, textsize='', text=''):
        id = self.__get_last_picture_id()
        self.camera.start_preview()

        self.camera.annotate_text_size = textsize
        self.camera.annotate_text = text

        self.camera.capture(path + str(id))
        self.camera.stop_preview()
        self.__set_last_picture_id(id + 1)

    @is_camera_plugged
    def getVideo(self, duration, path):
        id = self.__get_last_video_id()
        self.camera.start_recording(path + id)
        sleep(duration)
        self.camera.stop_recording()
        self.__set_last_video_id(id + 1)
