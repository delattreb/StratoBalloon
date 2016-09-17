"""
com_gpio.py v1.0.2
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

# TODO ATTENTION : l'import de la lib GPIO et l'exploitation doivent se faire en mode ROOT (sudo du script)

try:
    from RPi import GPIO as GPIOlib
except:
    GPIOlib = None

from lib import com_logger


def is_plugged(function):
    def plugged(*original_args, **original_kwargs):
        return function(*original_args, **original_kwargs)

    if not GPIOlib:
        logger = com_logger.Logger('GPIO')
        logger.log.warning('GPIO not present')

    return plugged


class GPIO:
    @is_plugged
    def __init__(self, name='', file=''):
        self.logger = com_logger.Logger(name, file)

    def setmodeBOARD(self):
        if GPIOlib != None:
            GPIOlib.setmode(GPIOlib.BOARD)
            self.logger.log.debug('setMode')

    def setmodeBCM(self):
        if GPIOlib != None:
            GPIOlib.setmode(GPIOlib.BCM)
            self.logger.log.debug('setmodeBCM')

    def getmode(self):
        if GPIOlib != None:
            self.logger.log.debug('getmode')
            return GPIOlib.getmode()

    def setupIO(self, IO_number, mode):
        if GPIOlib != None:
            GPIOlib.setup(IO_number, mode)
            self.logger.log.debug('setupIO')
            # GPIOlib.setup(12, GPIOlib.IN)                    # broche 12 est une entree numerique
            # GPIOlib.setup(12, GPIOlib.OUT)                   # broche 12 est une sortie numerique
            # GPIOlib.setup(12, GPIOlib.OUT, initial=GPIOlib.HIGH)# broche 12 est une sortie initialement a l'etat haut*

    def getIO(self, IO_number):
        if GPIOlib != None:
            self.logger.log.debug('getIO')
            return GPIOlib.input(IO_number)

    def setIO(self, IO_number, state):
        if GPIOlib != None:
            self.logger.log.debug('setIO')
            # TODO vérifier la valeur de la constante LOW et HIGH peut etre 0 ou 1
            if state == 0:
                GPIOlib.output(IO_number, GPIOlib.LOW)
            if state == 1:
                GPIOlib.output(IO_number, GPIOlib.HIGH)

    def switchIO(self, IO_number):
        if GPIOlib != None:
            self.logger.log.debug('switchIO')
            GPIOlib.output(IO_number, not self.getIO(IO_number))

    def getsetupIO(self, IO_number):
        if GPIOlib != None:
            self.logger.log.debug('getsetupIO')
            # On peut interroger l'E/S afin de connaître son état de configuration.
            # Les valeurs renvoyées sont alors GPIOlib.INPUT, GPIOlib.OUTPUT, GPIOlib.SPI, GPIOlib.I2C, GPIOlib.HARD_PWM, GPIOlib.SERIAL ou GPIOlib.UNKNOWN.
            return GPIOlib.gpio_function(IO_number)

    def cleanup(self):
        if GPIOlib != None:
            self.logger.log.debug('cleanup')
            GPIOlib.cleanup()

    def PWM(self, IO_number, frequence, rapport_cyclique, nouveau_rapport_cyclique, nouvelle_frequence):
        if GPIOlib != None:
            self.logger.log.debug('PWM')
            p = GPIOlib.PWM(IO_number, frequence)
            p.start(rapport_cyclique)  # ici, rapport_cyclique vaut entre 0.0 et 100.0
            p.ChangeFrequency(nouvelle_frequence)
            p.ChangeDutyCycle(nouveau_rapport_cyclique)
            p.stop()

    def pull(self, IO_number):
        if GPIOlib != None:
            self.logger.log.debug('pull')
            # Afin d'éviter de laisser flottante toute entrée, il est possible de connecter des résistances de pull-up ou de pull-down, au choix, en interne.
            # Pour information, une résistance de pull-up ou de pull-down a pour but d'éviter de laisser une entrée ou une sortie dans un état incertain, en forçant une connexion à la masse ou à un potentiel donné.
            GPIOlib.setup(IO_number, GPIOlib.IN, pull_up_down=GPIOlib.PUD_UP)
            GPIOlib.setup(IO_number, GPIOlib.IN, pull_up_down=GPIOlib.PUD_DOWN)

    def wait_edge(self, IO_number):
        if GPIOlib != None:
            self.logger.log.debug('wait_edge')
            # La première consiste à bloquer l'exécution du programme jusqu'à ce que l'événement se produise.
            return GPIOlib.wait_for_edge(IO_number, GPIOlib.RISING)

    def event_detect(self, IO_number):
        if GPIOlib != None:
            self.logger.log.debug('event_detect')
            GPIOlib.add_event_detect(IO_number, GPIOlib.RISING)
            while True:
                if GPIOlib.event_detected(IO_number):
                    print("Bouton appuye")

    def callBack(self, IO_number):
        if GPIOlib != None:
            self.logger.log.debug('callBack')

            def my_callback(IO_number):
                print("un evenement s'est produit")

            # ici on ajoute une tempo de 75 ms pour eviter l'effet rebond
            GPIOlib.add_event_detect(IO_number, GPIOlib.BOTH, callback=my_callback, bouncetime=75)
            # votre programme ici

    def remove_callBack(self, IO_number):
        if GPIOlib != None:
            GPIOlib.remove_event_detect(IO_number)

    # TODO a supprimer
    """
    setmodeBOARD()
    print("GPIOlib MODE: " + str(getmode()))
    print("mode in:" + str(GPIOlib.IN))
    setupIO(12, GPIOlib.IN)
    print("get: " + str(getIO(12)))
    print("get mode: " + str(getsetupIO(12)))

    print("")
    print("mode out:" + str(GPIOlib.OUT))
    setupIO(12, GPIOlib.OUT)
    print("get: " + str(getIO(12)))
    print("get mode: " + str(getsetupIO(12)))

    cleanup()
    """
