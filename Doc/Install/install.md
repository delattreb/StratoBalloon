# Installation/Configuration Raspberry

## Disque en RAM
Fichier /etc/fstab:
```
tmpfs /tmp tmpfs defaults,noatime,nosuid,size=10m 0 0
tmpfs /var/tmp tmpfs defaults,noatime,nosuid,size=10m 0 0
```
Répertoire personnel en RAM
````
tmpfs /home/pi/images tmpfs defaults,noatime,nosuid,size=50m 0 0
````

## I2C Bus speed
sudo nano /boot/config.txt
````
dtparam=i2c_baudrate=50000
````

## UART speed
/boot/cmdline.txt 
````
dwc_otg.lpm_enable=0 console=ttyAMA0,115200 kgdboc=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 rootwait
````

/etc/inittab 
````
respawn:/sbin/getty -L ttyAMA0 115200 vt100
````

## Bash au boot

**1er méthode :**
    copier le bash dans /etc/init.d
    chmod +x

**2eme méthode :** 
    sudo crontab -e
    @reboot /etc/init.d/bash.sh

**3eme méthode :**
    cd /etc/init.d
    sudo update-rd.d bash.sh defaults

**Pour supprimer le service au démarrage:**
    sudo update-rc bash.sh remove


## WiringPi GPIO

http://wiringpi.com/pins/
````
sudo apt-get install git-core
sudo apt-get update
sudo apt-get upgrade
git clone git://git.drogon.net/wiringPi
cd wiringPi
git pull origin
./build
````

## GPIO

````
sudo raspi-config Activer:I2C
sudo reboot
lsmod | grep i2c_ : Vérifier l'installation
sudo raspi-config
````

Activer le spi

sudo reboot
````
lsmod | grep spi_ : Vérifier l'installation
````

sudo raspi-config
activer serial
sudo reboot
````
sudo apt-get install python-rpi.gpio python3-rpi.gpio
pip3 install RPi.GPIOlib
````

Sinon
I downloaded RPi.GPIO 5.3a from here: https://pypi.python.org/pypi/RPi.GPIO
sudo python setup.py install

## Configuration Wifi

````
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
network={
    ssid="SFR_0950"
    psk="Your_wifi_password"
}


 /etc/network/interfaces

allow-hotplug wlan0
iface wlan0 inet static
address 192.168.0.150
netmask 255.255.255.0
gateway 192.168.0.1
wpa-ssid "mon SSID"
wpa-psk "mon mot de passe"
````

## Apache PHP

http://raspbian-france.fr/installer-serveur-web-raspberry/

```
sudo chown -R www-data:pi /var/www/html/
sudo chmod -R 770 /var/www/html/

Installation Python3
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install python3-picamera
sudo pip3 install bs4
sudo pip3 install psutil
sudo apt-get install python3-pil
sudo apt-get install python3-smbus
sudo apt-get install php5-sqlite

sudo apt-get install libjpeg-dev
sudo  apt-get install zlib1g-dev
sudo pip3 install Pillow
```

## USB

````
sudo apt-get install ntfs-3g
sudo apt-get install usbmount
sudo apt-get install udisks-glue
sudo apt-get install exfat-fuse
sudo blkid
````

## Wifi pour Minibian

http://www.htpcguides.com/upgrade-minibian-raspberry-pi-3-image/

## GPSD

/etc/default/gpsd
-> DEVICES="/dev/ttyAMA0"

**Attention: Sur Rasperry Pi Zero le port serie est: /dev/ttyS0**



