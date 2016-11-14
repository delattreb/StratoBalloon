"""
com_gpio.py v1.0.2
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

try:
    from RPi import GPIO
except:
    GPIO = None

from lib import com_logger


def is_plugged(function):
    def plugged(*original_args, **original_kwargs):
        return function(*original_args, **original_kwargs)
    
    if not GPIO:
        logger = com_logger.Logger('GPIO')
        logger.log.warning('GPIO not present')
    
    return plugged


class GPIODialog:
    @is_plugged
    def __init__(self, name='', file=''):
        self.importlib = GPIO
        self.logger = com_logger.Logger(name, file)
        # self.setwarnings(False)
        self.IN = GPIO.IN if GPIO != None else None
        self.OUT = GPIO.OUT if GPIO != None else None
        self.LOW = GPIO.LOW if GPIO != None else None
        self.HIGH = GPIO.HIGH if GPIO != None else None
        self.PUD_UP = GPIO.PUD_UP if GPIO != None else None
        self.PUD_DOWN = GPIO.PUD_DOWN if GPIO != None else None
        self.RISING = GPIO.RISING if GPIO != None else None
    
    def __delete__(self, instance):
        if GPIO != None:
            self.cleanup()
    
    def setwarnings(self, state):
        if GPIO != None:
            GPIO.setwarnings(state)
    
    def setmodeBOARD(self):
        if GPIO != None:
            GPIO.setmode(GPIO.BOARD)
            # self.logger.log.debug('setMode')
    
    def setmodeBCM(self):
        if GPIO != None:
            GPIO.setmode(GPIO.BCM)
            # self.logger.log.debug('setmodeBCM')
    
    def getmode(self):
        if GPIO != None:
            # self.logger.log.debug('getmode')
            return GPIO.getmode()
    
    def setupIO(self, IO_number, mode):
        if GPIO != None:
            GPIO.setup(IO_number, mode)
            # self.logger.log.debug('setupIO')
    
    def getIO(self, IO_number):
        if GPIO != None:
            # self.logger.log.debug('getIO')
            return GPIO.input(IO_number)
    
    def setIO(self, IO_number, state):
        if GPIO != None:
            # self.logger.log.debug('setIO')
            GPIO.output(IO_number, state)
    
    def switchIO(self, IO_number):
        if GPIO != None:
            # self.logger.log.debug('switchIO')
            GPIO.output(IO_number, not self.getIO(IO_number))
    
    def getSetupIO(self, IO_number):
        if GPIO != None:
            # self.logger.log.debug('getSetupIO')
            # On peut interroger l'E/S afin de connaître son état de configuration.
            # Les valeurs renvoyées sont alors GPIO.INPUT, GPIO.OUTPUT, GPIO.SPI, GPIO.I2C, GPIO.HARD_PWM, GPIO.SERIAL ou GPIO.UNKNOWN.
            return GPIO.gpio_function(IO_number)
    
    def cleanup(self):
        if GPIO != None:
            # self.logger.log.debug('cleanup')
            GPIO.cleanup()
    
    def PWM(self, IO_number, frequence, rapport_cyclique, nouveau_rapport_cyclique, nouvelle_frequence):
        if GPIO != None:
            # self.logger.log.debug('PWM')
            p = GPIO.PWM(IO_number, frequence)
            p.start(rapport_cyclique)  # ici, rapport_cyclique vaut entre 0.0 et 100.0
            p.ChangeFrequency(nouvelle_frequence)
            p.ChangeDutyCycle(nouveau_rapport_cyclique)
            p.stop()
    
    def pull(self, IO_number):
        if GPIO != None:
            # self.logger.log.debug('pull')
            # Afin d'éviter de laisser flottante toute entrée, il est possible de connecter des résistances de pull-up ou de pull-down, au choix, en interne.
            # Pour information, une résistance de pull-up ou de pull-down a pour but d'éviter de laisser une entrée ou une sortie dans un état incertain, en forçant une connexion à la masse ou à un potentiel donné.
            GPIO.setup(IO_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(IO_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    def setup(self, IO_number, mode):
        if GPIO != None:
            # self.logger.log.debug('setup:' + 'IO:' + str(IO_number) + ' Mode:' + str(mode))
            GPIO.setup(IO_number, mode)
    
    def setuppud(self, IO_number, mode, pud):
        if GPIO != None:
            # self.logger.log.debug('setup')
            GPIO.setup(IO_number, mode, pud)
    
    def wait_edge(self, IO_number):
        if GPIO != None:
            # self.logger.log.debug('wait_edge')
            # La première consiste à bloquer l'exécution du programme jusqu'à ce que l'événement se produise.
            return GPIO.wait_for_edge(IO_number, GPIO.RISING)
    
    def event_detect(self, IO_number):
        if GPIO != None:
            self.logger.log.debug('event_detect')
            GPIO.add_event_detect(IO_number, GPIO.RISING)
            while True:
                if GPIO.event_detected(IO_number):
                    print("Bouton appuye")
    
    def callBack(self, IO_number):
        if GPIO != None:
            self.logger.log.debug('callBack')
            
            def my_callback(IO_number):
                print("un evenement s'est produit")
            
            # ici on ajoute une tempo de 75 ms pour eviter l'effet rebond
            GPIO.add_event_detect(IO_number, GPIO.BOTH, callback=my_callback, bouncetime=75)
            # votre programme ici
    
    def remove_callBack(self, IO_number):
        if GPIO != None:
            GPIO.remove_event_detect(IO_number)
