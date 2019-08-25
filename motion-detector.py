from gpiozero import MotionSensor
from signal import pause
import time, zmq, json

Sensor_Pin = 4
sensor = MotionSensor(Sensor_Pin)


pub_port = 8000

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:{0}".format(pub_port))

while True:
    state = 0
    if sensor.motion_detected:
        state = 1

    msg = {
        "type": "motion",
        "state": state
    }

    socket.send_multipart([b"motion", json.dumps(msg).encode("UTF-8")])
    
    time.sleep(1)

