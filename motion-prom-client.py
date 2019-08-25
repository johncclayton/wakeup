import zmq, time, sys, json
from prometheus_client import start_http_server, Counter

pub_port = 8000
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:{0}".format(pub_port))
socket.setsockopt(zmq.SUBSCRIBE, b"motion")

MOVEMENT_DETECTION = Counter('movement_detected', 'Incremented by 1 when movement is detected')

prom_port = 9091
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
