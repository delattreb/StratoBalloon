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

from dal import dal_camera
from lib import com_config


class Camera:
    def __init__(self):
        config = com_config.getConfig()  # Set camera configuration

        if PiCamera:
            self.camera = PiCamera()
            self.camera.resolution = (int(config['CAMERA']['resolution_x']), int(config['CAMERA']['resolution_y']))
            self.camera.framerate = config['CAMERA']['framerate']
            self.camera.rotation = config['CAMERA']['rotation']
            self.camera.brightness = config['CAMERA']['brightness']
            self.camera.contrast = config['CAMERA']['contrast']
            self.camera.image_effect = config['CAMERA']['image_effect']
            self.camera.exposure_mode = config['CAMERA']['exposure_mode']

    def __get_last_picture_id(self):
        d = dal_camera.DAL_Camera()
        return d.getLastPictureId()

    def __set_last_picture_id(self, value):
        d = dal_camera.DAL_Camera()
        d.setLastPictureId(value)

    def __get_last_video_id(self):
        d = dal_camera.DAL_Camera()
        return d.getLastVideoId()

    def __set_last_video_id(self, value):
        d = dal_camera.DAL_Camera()
        d.setLastPictureId(value)

    def getPictureText(self, path, filename, textsize, text):
        if PiCamera:
            id = self.__get_last_picture_id()
            # self.camera.start_preview()
            # self.camera.annotate_text_size = textsize
            # self.camera.annotate_text = text
            # self.camera.capture(path + id)
            # self.camera.stop_preview()
            self.__set_last_picture_id(id + 1)

    def getPicture(self, path):
        if PiCamera:
            id = self.__get_last_picture_id()
            # self.camera.start_preview()
            # self.camera.capture(path + str(id))
            # self.camera.stop_preview()
            self.__set_last_picture_id(id + 1)

    def getVideo(self, duration, path):
        if PiCamera:
            id = self.__get_last_video_id()
            # self.camera.start_recording(path + id)
            # sleep(duration)
            # self.camera.stop_recording()
            self.__set_last_video_id(id + 1)
