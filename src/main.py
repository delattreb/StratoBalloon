from lib import com_camera, com_config, com_gpio, com_lcd

#config = com_config.setConfig()

c = com_camera.Camera()
c.getPicture('', 10, 'text')

g = com_gpio.GPIO()
g.setmodeBOARD()

lcd = com_lcd.LCD()
lcd.rectangle(0, 0, lcd.width_max, 63)
