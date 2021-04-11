import time
import zmq


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://*:5555')

i = 0
while True:
    message = socket.recv()
    print(f"Received request: {message}")

    # time.sleep(1)

    res = 'World ' + str(i)
    i += 1

    socket.send_string(res)
