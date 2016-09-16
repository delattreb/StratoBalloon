from lib import com_camera, com_config, com_gpio, com_lcd, com_logger

#config = com_config.setConfig()

c = com_camera.Camera()
c.getPicture('', 10, 'text')

g = com_gpio.GPIO()
g.setmodeBOARD()

lcd = com_lcd.LCD()
lcd.rectangle(0, 0, lcd.width_max, 63)

log = com_logger.Logger('toto')



log2 = com_logger.Logger('toto2')



