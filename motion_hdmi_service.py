import zmq, time, sys, json, datetime
from prometheus_client import start_http_server, Counter
from configuration import get_pub_settings, get_sub_settings, get_prom_settings
import os

(pub_sensor_pin, pub_bind_host, pub_bind_port, pub_time_delay_sec) = get_pub_settings()
(sub_connect_host, sub_connect_port) = get_sub_settings()

def main_func():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://{0}:{1}".format(sub_connect_host, sub_connect_port))
    socket.setsockopt(zmq.SUBSCRIBE, b"motion")

    DELAY_VALUE = 20
    counter = 0
    last_screen_on = None

    while True:
        [address, content] = socket.recv_multipart()
        msg = json.loads(content)
        if msg["type"] == "motion":
            state = msg["state"]
            if state == 1:
                counter = DELAY_VALUE

        now = datetime.datetime.now()
        counter = counter - 1

        if counter <= 0:
            # ok, time to switch off the screen!
            print("Boy it's boring in here... somebody move!")
        else:
            if last_screen_on is None or (now - last_screen_on).seconds > 60:
                last_screen_on = now

                print("Forcing the screen on")

                # ok, it's time to FORCE the screen on
                os.system("./screen_on.sh")
            else:
                print("Counter is at: {0} - ignoring events for 60 seconds...".format(counter))
                    
    socket.close()
    context.term()
    
    return 0

if __name__ == "__main__":
    main_func()