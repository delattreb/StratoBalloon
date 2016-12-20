"""
com_sr04.py v1.0.2
Auteur: Bruno DELATTRE
Date : 28/09/2016
"""

import time

from lib import com_logger
from lib.driver import com_gpio


class SR04:
    def __init__(self, port_triger, port_echo):
        self.port_triger = port_triger
        self.port_echo = port_echo

        self.gpio = com_gpio.GPIODialog('SR04')
        if self.gpio.importlib is not None:
            self.gpio.setmodebcm()

            self.gpio.setup(self.port_triger, self.gpio.OUT)
            self.gpio.setup(self.port_echo, self.gpio.IN)

            self.gpio.setio(self.port_triger, False)
            time.sleep(2)  # Attente changement etat

    def __delete__(self, instance):
        self.gpio.cleanup()

    def getdistance(self):
        if self.gpio.importlib is not None:
            self.gpio.setio(self.port_triger, True)
            time.sleep(0.00001)
            self.gpio.setio(self.port_triger, False)
            pulse_start = 0
            pulse_end = 0

            while self.gpio.getio(self.port_echo) == 0:
                pulse_start = time.time()

            while self.gpio.getio(self.port_echo) == 1:
                pulse_end = time.time()

            distance = round((pulse_end - pulse_start) * 17150, 2)

            logger = com_logger.Logger()
            logger.info('Distance: ' + str(distance))

            return distance
