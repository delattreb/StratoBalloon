"""
com_gpio.py v1.0.2
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

try:
    from RPi import GPIO
except Exception as exp:
    GPIO = None

from lib import com_logger


def is_plugged(function):
    def plugged(*original_args, **original_kwargs):
        return function(*original_args, **original_kwargs)
    
    if not GPIO:
        logger = com_logger.Logger('GPIO')
        logger.warning('GPIO not present')
    
    return plugged


class GPIODialog:
    @is_plugged
    def __init__(self, name = ''):
        self.importlib = GPIO
        self.logger = com_logger.Logger(name)
        # self.setwarnings(False)
        self.IN = GPIO.IN if GPIO is not None else None
        self.OUT = GPIO.OUT if GPIO is not None else None
        self.LOW = GPIO.LOW if GPIO is not None else None
        self.HIGH = GPIO.HIGH if GPIO is not None else None
        self.PUD_UP = GPIO.PUD_UP if GPIO is not None else None
        self.PUD_DOWN = GPIO.PUD_DOWN if GPIO is not None else None
        self.RISING = GPIO.RISING if GPIO is not None else None
    
    def __delete__(self, instance):
        if self.importlib is not None:
            self.cleanup()
    
    def setwarnings(self, state):
        if self.importlib is not None:
            GPIO.setwarnings(state)

    def setmodeboard(self):
        if self.importlib is not None:
            GPIO.setmode(GPIO.BOARD)

    def setmodebcm(self):
        if self.importlib is not None:
            GPIO.setmode(GPIO.BCM)
    
    def getmode(self):
        if self.importlib is not None:
            return GPIO.getmode()

    def setupio(self, io_number, mode):
        if self.importlib is not None:
            GPIO.setup(io_number, mode)

    def getio(self, io_number):
        if self.importlib is not None:
            return GPIO.input(io_number)

    def setio(self, io_number, state):
        if self.importlib is not None:
            GPIO.output(io_number, state)

    def switchio(self, io_number):
        if self.importlib is not None:
            GPIO.output(io_number, not self.getio(io_number))

    def getsetupio(self, io_number):
        if self.importlib is not None:
            # self.logger.debug('getsetupio')
            # On peut interroger l'E/S afin de connaître son état de configuration.
            # Les valeurs renvoyées sont alors GPIO.INPUT, GPIO.OUTPUT, GPIO.SPI, GPIO.I2C, GPIO.HARD_PWM, GPIO.SERIAL ou GPIO.UNKNOWN.
            return GPIO.gpio_function(io_number)
    
    def cleanup(self):
        if self.importlib is not None:
            GPIO.cleanup()

    def pwm(self, io_number, frequence, rapport_cyclique, nouveau_rapport_cyclique, nouvelle_frequence):
        if self.importlib is not None:
            p = GPIO.PWM(io_number, frequence)
            p.start(rapport_cyclique)  # ici, rapport_cyclique vaut entre 0.0 et 100.0
            p.ChangeFrequency(nouvelle_frequence)
            p.ChangeDutyCycle(nouveau_rapport_cyclique)
            p.stop()

    def pull(self, io_number):
        if self.importlib is not None:
            # self.logger.debug('pull')
            # Afin d'éviter de laisser flottante toute entrée, il est possible de connecter des résistances de pull-up ou de pull-down, au choix, en interne.
            # Pour information, une résistance de pull-up ou de pull-down a pour but d'éviter de laisser une entrée ou une sortie dans un état incertain, en
            # forçant une connexion à la # masse ou à un potentiel donné.
            GPIO.setup(io_number, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            GPIO.setup(io_number, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

    def setup(self, io_number, mode):
        if self.importlib is not None:
            GPIO.setup(io_number, mode)

    def setuppud(self, io_number, mode, pud):
        if self.importlib is not None:
            GPIO.setup(io_number, mode, pud)

    def wait_edge(self, io_number):
        if self.importlib is not None:
            # La première consiste à bloquer l'exécution du programme jusqu'à ce que l'événement se produise.
            return GPIO.wait_for_edge(io_number, GPIO.RISING)

    def event_detect(self, io_number):
        if self.importlib is not None:
            self.logger.debug('event_detect')
            GPIO.add_event_detect(io_number, GPIO.RISING)
            while True:
                if GPIO.event_detected(io_number):
                    print("Bouton appuye")

    def callback(self, io_number):
        """
        if self.importlib is not None:
            self.logger.debug('callback')
            
            def my_callback(io_number):
                self.logger.debug('Evenent')
    
                # ici on ajoute une tempo de 75 ms pour eviter l'effet rebond
                GPIO.add_event_detect(io_number, GPIO.BOTH, callback = my_callback, bouncetime = 75)
                # votre programme ici
        """
        pass

    def remove_callback(self, io_number):
        if self.importlib is not None:
            GPIO.remove_event_detect(io_number)
