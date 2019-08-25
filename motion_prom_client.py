import zmq, time, sys, json
from prometheus_client import start_http_server, Counter
from configuration import get_pub_settings, get_sub_settings, get_prom_settings

(pub_sensor_pin, pub_bind_host, pub_bind_port, pub_time_delay_sec) = get_pub_settings()
(sub_connect_host, sub_connect_port) = get_sub_settings()

def main_func():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://{0}:{1}".format(sub_connect_host, sub_connect_port))
    socket.setsockopt(zmq.SUBSCRIBE, b"motion")

    MOVEMENT_DETECTION = Counter('movement_detected', 'Incremented by 1 when movement is detected')

    (prom_port,) = get_prom_settings()

    start_http_server(prom_port)
    print("Motion detection service started - on port {0}".format(prom_port))

    while True:
        [address, content] = socket.recv_multipart()
        
        msg = json.loads(content)
        if msg["type"] == "motion":
            state = msg["state"]
            if state == 1:
                MOVEMENT_DETECTION.inc(1)

    socket.close()
    context.term()
    
    return 0


if __name__ == "__main__":
    main_func()