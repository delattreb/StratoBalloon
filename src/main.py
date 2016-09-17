from lib import com_camera

# config = com_config.setConfig()

# p = com_camera.Camera('PICTURE')
# p.getPicture('/home/pi/StratoBalloon/src/')

v = com_camera.Camera('VIDEO')
v.getVideo(10, '/home/pi/')
