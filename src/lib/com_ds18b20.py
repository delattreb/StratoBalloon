"""
com_ds18b20.py v1.0.2
Auteur: Bruno DELATTRE
Date : 02/10/2016
"""

"""
Doc:
https://jahislove314.wordpress.com/2014/07/16/installation-dun-capteur-de-temperature-1-wire-ds18b20-sur-raspberry-partie-1/
https://jahislove314.wordpress.com/2014/07/16/afficher-la-temperature-dune-sonde-ds18b20-en-python-sur-le-raspberry-partie-2/


Lecture du capteur sur le 1-wire
Mettre le tout en classe
"""

from os import system
from time import sleep

## module GPIO 1-wire et capteur de temperature #####
system('modprobe w1-port')
system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'

## Remplacez les repertoires 28-xxxxxxxxxxx par vos propres repertoires
sonde1 = "/sys/bus/w1/devices/w1_bus_master1/28-000005f2424d/w1_slave"
sonde2 = "/sys/bus/w1/devices/w1_bus_master1/28-000005f2764e/w1_slave"
sonde3 = "/sys/bus/w1/devices/w1_bus_master1/28-000005f396a0/w1_slave"
## et ajuster aussi les 2 lignes ci dessous #########
sensors = [sonde1, sonde2, sonde3]
sensor_value = [0, 0, 0]


class DS18B20:
    def __init__(self):
        pass

    def read_file(self, file):
        f = open(file, 'r')
        lignes = f.readlines()
        f.close()
        return lignes

    def read_good(self, sensor):
        lines = self.read_file(sensor)
        while lines[0].strip()[-3:] != 'YES':  # lit les 3 derniers char de la ligne 0 et recommence si pas YES
            sleep(0.2)
            lines = self.read_file(sensor)

        temp_raw = lines[1].split("=")[1]  # quand on a eu YES, on lit la temp apres le signe = sur la ligne 1
        return round(int(temp_raw) / 1000.0, 2)  # le 2 arrondi a 2 chiffres apres la virgule

    def read(self, sensor):
        for (i, sensor) in enumerate(sensors):
            lines = self.read_file(sensor)
            while lines[0].strip()[-3:] != 'YES':  # lit les 3 derniers char de la ligne 0 et recommence si pas YES
                sleep(0.2)
                lines = self.read_file(sensor)

            temp_raw = lines[1].split("=")[1]  # quand on a eu YES, on lit la temp apres le signe = sur la ligne 1
            sensor_value[i] = round(int(temp_raw) / 1000.0, 2)  # le 2 arrondi a 2 chiffres apres la virgule

            return sensor_value[i]
