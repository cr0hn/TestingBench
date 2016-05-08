import zmq
import time

context = zmq.Context()
sock = context.socket(zmq.PUB)
sock.bind("tcp://127.0.0.1:5680")

while True:

    sock.send_string("a")
    time.sleep(1)
