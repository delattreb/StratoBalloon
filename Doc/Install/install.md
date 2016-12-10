# Installation/Configuration Raspberry Pi

## Raspberry Pi 3 disable the blutooth to get /dev/AMA0

file: /boot/config.txt
````
dtoverlay=pi3-disable-bt
reboot
````

File: /boot/cmdline.txt
remove: console=ttyAMA0,115200

````
dwc_otg.lpm_enable=0 console=tty1 elevator=deadline root=/dev/mmcblk0p2 rootfstype=ext4 rootwait
````

## Disk into RAM
File /etc/fstab:
```
tmpfs /tmp tmpfs defaults,noatime,nosuid,size=10m 0 0
tmpfs /var/tmp tmpfs defaults,noatime,nosuid,size=10m 0 0
```
Personnal directory into RAM
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

## Bash boot

**1st method :**
    copier le bash dans /etc/init.d
    chmod +x

**2nd method :** 
    sudo crontab -e
    @reboot /etc/init.d/bash.sh

**3th method :**
    cd /etc/init.d
    sudo update-rd.d bash.sh defaults

**Delete service on boot:**
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

Activate SPI et serial port

````
lsmod | grep i2c_ : Check install
lsmod | grep spi_ : Check install
````

````
sudo apt-get install python-rpi.gpio python3-rpi.gpio
pip3 install RPi.GPIOlib
````

Another method
I downloaded RPi.GPIO 5.3a from here: https://pypi.python.org/pypi/RPi.GPIO

````
sudo python setup.py install
````

## Pi GPIOd (pigpio)
````
apt-get install unzip

wget abyz.co.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make
make install
````

## Wifi Configuration

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

## DHT22

Install library

````
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
apt-get update
apt-get install build-essential python-dev
python setup.py install
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

Installation

````
sudo apt-get install ntfs-3g
sudo apt-get install usbmount
sudo apt-get install udisks-glue
sudo apt-get install exfat-fuse
sudo blkid
````

## Minibian

[Minibian link](https://sourceforge.net/projects/minibian/files/?source=navbar)

## GPSD

Installation

````
apt-get install gpsd gpsd-clients python-gps
````

Python install Lib
````
pip3 install gpsd-py3
````

/etc/default/gpsd
/dev/ttyAMA0 for Raspberry Pi 3
/dev/ttyS0 for Raspberry Pi Zero

````
# Default settings for the gpsd init script and the hotplug wrapper.

# Start the gpsd daemon automatically at boot time
START_DAEMON="true"

# Use USB hotplugging to add new USB devices automatically to the daemon
USBAUTO="true"

# Devices gpsd should collect to at boot time.
# They need to be read/writeable, either by user gpsd or the group dialout.
#DEVICES="/dev/ttyS0"
DEVICES="/dev/ttyAMA0"

# Other options you want to pass to gpsd
GPSD_OPTIONS="/var/run/gpsd.sock"
````
if Deamon not start automaticcaly

````
gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
````

**Warning: On Rasperry Pi Zero serial port is named: /dev/ttyS0**

## RPiclone

Installation

````
wget http://www.framboise314.fr/docs/rpi-clone/rpi-clone.sh
````


