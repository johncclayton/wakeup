from gpiozero import MotionSensor
from signal import pause
# from prometheus_client import start_http_server, Counter
import time, zmq

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

MAX_VALUE = 60
counter = 0

while True:
    if sensor.motion_detected:
        print("Motion detected!")
        counter = MAX_VALUE

    counter = counter - 1
    if counter <= 0:
        counter = 0

    msg = {
        "type": "motion",
        "counter": counter
    }

    socket.send_json(msg)
    
    time.sleep(0.25)
