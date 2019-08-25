from gpiozero import MotionSensor
from signal import pause
import time, zmq, json
# from prometheus_client import start_http_server, Counter

Sensor_Pin = 4
sensor = MotionSensor(Sensor_Pin)

# MOVEMENT_DETECTION = Counter('movement_detected', 'Incremented by 1 when movement is detected')

# prom_port = 9091
# start_http_server(prom_port)
# print("Motion detection service started - on port {0}".format(prom_port))

pub_port = 8000

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:{0}".format(pub_port))

while True:
    state = 0
    if sensor.motion_detected:
        print("Motion detected!")
        state = 1

    msg = {
        "type": "motion",
        "state": state
    }

    socket.send_multipart([b"motion", json.dumps(msg).encode("UTF-8")])
    
    time.sleep(1)

