from gpiozero import MotionSensor
from signal import pause
from prometheus_client import start_http_server, Counter
from wakeup.configuration import get_pub_settings
import time, zmq, json, os

(   pub_sensor_pin, 
    pub_bind_host, 
    pub_bind_port, 
    pub_prom_port,
    pub_time_delay_sec) = get_pub_settings()

MOVEMENT_DETECTION = Counter('movement_pub_detected_total', 'Incremented by 1 when movement is detected')
MOVEMENT_MSG_SENT = Counter('movement_pub_sent_total', 'Counter of the number of messages sent over ZMQ')

def main_func():
    sensor = MotionSensor(pub_sensor_pin)

    start_http_server(pub_prom_port)
    print("Motion detection service started - on port {0}".format(pub_prom_port))

    try:
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://{0}:{1}".format(pub_bind_host, pub_bind_port))

        while True:
            state = 0
            if sensor.motion_detected:
                state = 1
                MOVEMENT_DETECTION.inc()

            msg = {
                "type": "motion",
                "state": state
            }

            socket.send_multipart([b"motion", json.dumps(msg).encode("UTF-8")])
            MOVEMENT_MSG_SENT.inc(1)
            
            time.sleep(pub_time_delay_sec)

    except KeyboardInterrupt:
        print("KeyboardInterrupt - graceful shutdown")

    socket.close()
    context.term()

    return 0

if __name__ == "__main__":
    main_func()