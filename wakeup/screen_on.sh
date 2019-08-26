#!/bin/bash
export DISPLAY=:0
/usr/bin/tvservice --preferred
sleep 1
/usr/bin/xdotool mousemove_relative 0 1
sleep 1
/usr/bin/xdotool mousemove_relative 0 1
