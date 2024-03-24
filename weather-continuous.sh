#!/bin/bash
sleep 30  # wait for internet at reboot
cd /home/pi/inky-weather
python weather-continuous.py
