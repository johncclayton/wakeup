Idea
====
To ensure that when I walk into the room that the monitor attached to the Raspberry Pi 4 automatically switches on. 

How
===
A movement/IR detector is attached to the Raspberry PI GPIO pins.  Python code monitors the GPIO signal and wakes the HDMI system.

A <TBD> task runs to keep a browser loaded at a specific page.  This page points to my Dashboard.  This web task is not
part of this project. 

Sleep / Screen Saver
====================
The OS is configured to enable the screen saver in a standard fashion. 

Quick Start
===========
I don't care about dev I just want to use it. 

Do this: 

    $ pip install wakeup

Development
===========
These instructions work well on a RPI4 installed with Buster (around August 2019)

    $ sudo apt install virtualenv virtualenvwrapper    
    $ mkvirtualenv -p /usr/bin/python3 stats
    $ workon stats
    $ pip install -r requirements.txt
    $ python setup.py develop

You'll want to open the firewall for prometheus metrics collection (9091) as well as the ZMQ publisher (8000). 

    $ sudo ufw allow 9091/tcp
    $ sudo ufw allow 9092/tcp
    $ sudo ufw allow 8000/tcp


Build
=====
To produce PyPi compatible package. 

Setup
-----
First ensure you have the latest tools 

    $ python -m pip install --upgrade setuptools wheel twine

Make packages
-------------

    $ python setup.py sdist bdist_wheel