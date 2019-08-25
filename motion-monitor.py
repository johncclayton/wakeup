import zmq, time, sys, json

pub_port = 8000
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:{0}".format(pub_port))
socket.setsockopt(zmq.SUBSCRIBE, b"motion")

while True:
    (address, content) = socket.recv_multipart()
    msg = json.loads(content)
    if msg["type"] == "motion":
        state = msg["state"]
        if state == 1:
            print("It's ON")
        else:
            print("It's OFF")

socket.close()
context.term()
