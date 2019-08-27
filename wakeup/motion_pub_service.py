from gpiozero import MotionSensor
from signal import pause
from prometheus_client import start_http_server, Counter
from wakeup.configuration import get_pub_settings
import time, zmq, json, os, datetime

(   pub_sensor_pin, 
    pub_bind_host, 
    pub_bind_port, 
    pub_prom_port,
    pub_time_delay_sec) = get_pub_settings()

MOVEMENT_DETECTION = Counter('movement_pub_detected_total', 'Incremented by 1 when movement is detected')
MOVEMENT_MSG_SENT = Counter('movement_pub_sent_total', 'Counter of the number of messages sent over ZMQ')

last_state_change_time = datetime.datetime.now()
send_motion_event = True
have_sent_motion_event = False

# def motion_detected(sensor):
#     event_time = datetime.datetime.now()
#     seconds_diff = (event_time - last_state_change_time).seconds

#     # if sensor.motion_detected and not have_sent_motion_event:
#     #     send_motion_event = True
#     # elif not sensor.motion_detected and have_sent_motion_event:
#     #     send_motion_event = False
#     print("seconds: {0}, movement: {1}".format(seconds_diff, sensor.motion_detected))

def main_func():
    start_http_server(pub_prom_port)
    print("Motion detection service started - on port {0}".format(pub_prom_port))

    try:
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://{0}:{1}".format(pub_bind_host, pub_bind_port))

        sensor = MotionSensor(pub_sensor_pin)
        # sensor.when_motion = motion_detected

        while True:
            sensor.wait_for_motion(1)
            
            state = sensor.motion_detected
            if state == 1:
                MOVEMENT_DETECTION.inc()

            msg = {
                "type": "motion",
                "state": state
            }

            socket.send_multipart([b"motion", json.dumps(msg).encode("UTF-8")])
            MOVEMENT_MSG_SENT.inc(1)

            if state == 1:
                sensor.wait_for_inactive(1)

    except KeyboardInterrupt:
        print("KeyboardInterrupt - graceful shutdown")

    socket.close()
    context.term()

    return 0

if __name__ == "__main__":
    main_func()