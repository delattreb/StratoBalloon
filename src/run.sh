#!/bin/sh

cd /home/project/StratoBalloon/
pigpiod
python3.4 main.py
pkill pigpiod
