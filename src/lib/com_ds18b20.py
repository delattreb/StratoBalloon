"""
com_ds18b20.py v1.0.2
Auteur: Bruno DELATTRE
Date : 02/10/2016
"""

from os import system

from lib import com_logger

# module GPIO 1-wire Port GPIO4
system('modprobe w1-gpio')
system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'


class DS18B20:
    def __init__(self):
        pass
    
    def read_file(self, file):
        f = open(file, 'r')
        lignes = f.readlines()
        f.close()
        return lignes
    
    def read(self, name, sensor, dal):
        logger = com_logger.Logger('DS18B20 ' + name)
        
        lines = self.read_file(sensor)
        
        """ Suppression en cas de dead lock
        while lines[0].strip()[-3:] != 'YES':  # lit les 3 derniers char de la ligne 0 et recommence si pas YES
            sleep(0.2)
            lines = self.read_file(sensor)
        """
        if lines[0].strip()[-3:] != 'YES':
            logger.debug('Connexion ERROR')
            return -999
        
        temp_raw = lines[1].split("=")[1]  # quand on a eu YES, on lit la temp apres le signe = sur la ligne 1
        temp = round(int(temp_raw) / 1000.0, 2)  # le 2 arrondi a 2 chiffres apres la virgule
        
        dal.set_ds18b20(name, str(temp))
        
        logger.debug('Temperature:' + str(temp))
        
        return temp
