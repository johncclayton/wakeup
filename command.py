from gpiozero import MotionSensor
from signal import pause
import time

Sensor_Pin = 4
sensor = MotionSensor(Sensor_Pin)

while True:
    if sensor.motion_detected:
        print("There is movement!")
    else:
        print("Nothing happenin...")
    time.sleep(1)
