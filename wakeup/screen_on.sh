#!/bin/bash

export DISPLAY=:0
# /usr/bin/tvservice --preferred

sleep 1
/usr/bin/xdotool mousemove_relative 0 10
sleep 1
/usr/bin/xdotool mousemove_relative 10 0

sudo XAUTHORITY=/home/pi/.Xauthority DISPLAY=:0.0 xset dpms force on
