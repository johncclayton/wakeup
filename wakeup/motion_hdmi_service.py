import zmq, time, sys, json, datetime
from prometheus_client import start_http_server, Gauge, Counter, Summary
from wakeup.configuration import get_pub_settings, get_sub_settings
from pkg_resources import resource_filename
import argparse
import os

(pub_sensor_pin, pub_bind_host, pub_bind_port, pub_prom_port, pub_time_delay_sec) = get_pub_settings()
(sub_connect_host, sub_connect_port) = get_sub_settings()

hdmi_prom_port = os.getenv("MOTION_HDMI_PROM_PORT", 9092)
script_path = resource_filename(__name__, "screen_on.sh")
listen_only = False
movement_count = 0

MOVEMENT_HDMI_REQUEST_TIME = Summary('movement_hdmi_request_seconds', 'The time taken to process incoming requests')
MOVEMENT_HDMI_DETECTION_EVENTS = Counter('movement_hdmi_is_moving', 'The total number of positive movement events detected')

def force_on():
    os.system(script_path)

@MOVEMENT_HDMI_REQUEST_TIME.time()
def process_request(msg):
    global movement_count
    
    if msg["type"] == "motion" and "state" in msg:
        if msg["state"] == 1:
            MOVEMENT_HDMI_DETECTION_EVENTS.inc()
            if listen_only:
                movement_count = movement_count + 1
                print("Movement detected - listen only mode, counter: {0}".format(movement_count))
            else:
                force_on()

def main_func():
    parser = argparse.ArgumentParser(description="HDMI monitor/controller, can also be used to listen to the ZMQ event stream")
    parser.add_argument("-l", "--listen", action="store_true", help='Listen only, print events to stdout - do not call the scripts to force HDMI on', default=False)
    args = parser.parse_args()

    global listen_only
    listen_only = args.listen
    if listen_only:
        print("Listening only, subscribing to {0}:{1}".format(sub_connect_host, sub_connect_port))

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://{0}:{1}".format(sub_connect_host, sub_connect_port))
    socket.setsockopt(zmq.SUBSCRIBE, b"motion")

    start_http_server(hdmi_prom_port)
    print("Motion HDMI service started - prometheus metrics are on port {0}".format(hdmi_prom_port))

    try:
        while True:
            [address, content] = socket.recv_multipart()
            process_request(json.loads(content))
    except KeyboardInterrupt:
        print("KeyboardInterrupt - graceful shutdown")
                    
    socket.close()
    context.term()
    
    return 0

if __name__ == "__main__":
    main_func()