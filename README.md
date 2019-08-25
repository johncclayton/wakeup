Idea
====
To ensure that when I walk into the room that the monitor attached to the Raspberry Pi 4 automatically switches on. 

How
===
A movement/IR detector is attached to the GPIO.  This drives a monitor process that wakes the HDMI system.  

Sleep
=====
The OS is configured to enable the screen saver in a standard fashion. 

Runtime
=======
Simply by installing a standard systemctl based control job to run the code. 

Development
===========
These instructions work well on a RPI4 installed with Buster (around August 2019)

    $ sudo apt install virtualenv virtualenvwrapper    
    $ mkvirtualenv -p /usr/bin/python3 stats
    $ workon stats
    $ pip install -r requirements.txt


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