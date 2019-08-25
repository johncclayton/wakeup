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
