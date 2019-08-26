import zmq, time, sys, json, datetime
from prometheus_client import start_http_server, Gauge, Counter
from wakeup.configuration import get_pub_settings, get_sub_settings
from pkg_resources import resource_filename
import os

(pub_sensor_pin, pub_bind_host, pub_bind_port, pub_prom_port, pub_time_delay_sec) = get_pub_settings()
(sub_connect_host, sub_connect_port) = get_sub_settings()

hdmi_prom_port = os.getenv("MOTION_HDMI_PROM_PORT", 9092)

MOVEMENT_HDMI_STATE = Gauge('movement_hdmi_state', 'The state of the HDMI controller')
MOVEMENT_HDMI_COUNTER = Gauge('movement_hdmi_detected_received_count', 'The number of movement detected messages received over ZMQ')

def main_func():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://{0}:{1}".format(sub_connect_host, sub_connect_port))
    socket.setsockopt(zmq.SUBSCRIBE, b"motion")

    start_http_server(hdmi_prom_port)
    print("Motion HDMI service started - on port {0}".format(hdmi_prom_port))

    DELAY_VALUE = 20
    counter = 0
    last_screen_on = None

    try:
        while True:
            [address, content] = socket.recv_multipart()
            msg = json.loads(content)
            if msg["type"] == "motion":
                state = msg["state"]
                if state == 1:
                    counter = DELAY_VALUE
                    print("Somebody moved!")
                    MOVEMENT_HDMI_COUNTER.inc(1)

            now = datetime.datetime.now()
            counter = counter - 1

            if counter <= 0:
                # ok, time to switch off the screen!
                print("Boy it's boring in here... somebody move!")
                MOVEMENT_HDMI_STATE.set(0)
            else:
                if last_screen_on is None or (now - last_screen_on).seconds > 60:
                    last_screen_on = now

                    MOVEMENT_HDMI_STATE.set(2)

                    # ok, it's time to FORCE the screen on
                    script_path = resource_filename(__name__, "screen_on.sh")
                    print("Forcing the screen on using: {0}".format(script_path))
                    os.system(script_path)
                else:
                    print("Counter is at: {0} - ignoring events for 60 seconds...".format(counter))
                    MOVEMENT_HDMI_STATE.set(1)
    except KeyboardInterrupt:
        print("KeyboardInterrupt - graceful shutdown")
                    
    socket.close()
    context.term()
    
    return 0

if __name__ == "__main__":
    main_func()