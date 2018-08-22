# StratoBalloon

See installation documentation:
https://github.com/delattreb/StratoBalloon/blob/master/Doc/Install/install.md

This project manage a strato spherical balloon.
Acquisition picture by two camera, temperature interior and exterior, GPS.
GPIO gasture on Raspberry Pi.

## Sensor gesture:
- DHT 11 (Humidity and temperature)
- DHT 22 x2 (Humidity and temperature)
- DS18B20 x2 (Temperature)
- SR04 (Ultra Sound)
- GPS (GPS)
- Camera x2
- LCD Screen (Type OLED 0.96" 128x64 pixel)

All sensor are read by a multi threading system, and write into a SQLite Database.

## Hardware:
This program run on 2 Raspberry Pi Zero.

## Software
Python programming


