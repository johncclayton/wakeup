from gpiozero import MotionSensor
from signal import pause
from configuration import get_pub_settings
import time, zmq, json, os

(pub_sensor_pin, pub_bind_host, pub_bind_port, pub_time_delay_sec) = get_pub_settings()

def main_func():
    sensor = MotionSensor(pub_sensor_pin)

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://{0}:{1}".format(pub_bind_host, pub_bind_port))

    while True:
        state = 0
        if sensor.motion_detected:
            state = 1

        msg = {
            "type": "motion",
            "state": state
        }

        socket.send_multipart([b"motion", json.dumps(msg).encode("UTF-8")])
        
        time.sleep(pub_time_delay_sec)
        
    return 0

if __name__ == "__main__":
    main_func()