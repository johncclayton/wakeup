Idea
====
To ensure that when I walk into the room that the monitor attached to the Raspberry Pi 4 automatically switches on. 

How
===
A movement/IR detector is attached to the Raspberry PI GPIO pins.  Python code monitors the GPIO signal and wakes the HDMI system.

The motion_pub_service command simply monitors the GPIO pin status and uses ZMQ to publish whatever it sees from the IR system as
a small JSON payload.  The ZMQ publish topic it's using is "motion". 

The motion_hdmi command subscribes to the "motion" topic and works out if it should force the screen on or not. 

Configuration
=============
Everything is via environment variables. 

TODO: list all the env vars

A <TBD> task runs to keep a browser loaded at a specific page.  This page points to my Dashboard.  This web task is not
part of this project. 

Sleep / Screen Saver
====================
This code doesn't turn off the screen - that's something the OS can do quite well on its own.

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

You'll want to open the firewall for prometheus metrics collection (9091, 9092) as well as the ZMQ publisher (8000). 

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