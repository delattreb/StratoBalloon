from lib import com_camera, com_config      , com_gpio


config = com_config.setConfig()

camera = com_camera.Camera()
camera.getPicture('')

g = com_gpio.GPIO()
g.getIO(4)

