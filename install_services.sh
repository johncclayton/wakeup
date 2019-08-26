#!/bin/sh
sudo cp wakeup_hdmi.service /etc/systemd/system/wakeup_hdmi.service
sudo cp wakeup_pub.service /etc/systemd/system/wakeup_pub.service

sudo systemctl start wakeup_pub.service
sudo systemctl start wakeup_hdmi.service

sudo systemctl enable wakeup_pub.service
sudo systemctl enable wakeup_hdmi.service
