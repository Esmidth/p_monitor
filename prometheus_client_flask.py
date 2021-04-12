from flask import Flask, Response
from prometheus_client import Counter, generate_latest
import zmq


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")




app = Flask(__name__)


counter = Counter("my_counter",'an example showed how to use counter')





@app.route('/metrics')
def hello():
    counter.inc(1)

    return Response(generate_latest(counter),mimetype='text/plain')


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8888)

