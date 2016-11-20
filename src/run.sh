#!/bin/sh

cd /home/project/StratoBalloon/src/
pigpiod
python3.4 main.py
pkill pigpiod
