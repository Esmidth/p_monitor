import threading
import time
from typing import AbstractSet
import zmq

from flask import Flask, Response
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

exitFlag = 0


global_sec = 0


# class Running_Metrics:
    # def __init__(self):
# class Perf_Metric:
#     nodeNum:int
#     sec:int
#     align_frame:int
#     sent_frame:int
#     forward_packets:int
#     consume_packets:int
#     missing_packets:int
#     drop_frames:int
#     missing_frames:int
#     consumer_speed:int
#     recv_speed:int
#     queue1_size:int
#     queue2_size:int
#     queue3_size:int

perf_metric_dict_list = []

# sec = Counter


@app.route('/metrics')
def hello():
    global perf_metric_dict_list
    return Response(str(perf_metric_dict_list),mimetype='text/plain')


# class ChannelCatcher(threading.Thread):
#     def __init__(self,ChannelID):
#         threading.Thread.__init__(self)
#         self.ChannelID = ChannelID
#         self.Timer = Timer()


class DataCatcher(threading.Thread):
    def __init__(self, threadID,portID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.counter = 0

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind('tcp://*:'+str(portID))
        # self.perf_metric_dict = {}

    def getData(self, input_string):
        global perf_metric_dict_list
        perf_metric_dict = {}
        split_num = input_string.count(',')
        # print(split_num)
        split_res = input_string.split(',', split_num)
        for sub_string in split_res:
            sub_string_split = sub_string.split(':', 1)
            perf_metric_dict[sub_string_split[0]] = int(sub_string_split[1])
        id = perf_metric_dict['nodeNum']
        # print(id)
        if id >= len(perf_metric_dict_list):
            perf_metric_dict_list.append(perf_metric_dict)
        else:
            perf_metric_dict_list[id] = perf_metric_dict


        # self.perf_metric_dict = perf_metric_dict

    def run(self):
        global global_sec
        message = self.socket.recv()
        global_sec = 0
        self.socket.send_string('1')

        while True:
            message = self.socket.recv().decode()
            # print(type(message))
            self.getData(message)
            # print("sec:{}, message: {}".format(global_sec, message))
            self.socket.send_string("123")


class Timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # self.sec = 0

    def run(self):
        global global_sec
        global perf_metric_dict
        while True:
            global_sec += 1
            time.sleep(1)
            print("sec:{}\t{}".format(global_sec, perf_metric_dict_list))
            # self.sec += 1


if __name__ == "__main__":
    thread1 = Timer()
    thread2 = DataCatcher(1,portID=5555)
    thread3 = DataCatcher(1,portID=5556)
    thread4 = DataCatcher(1,portID=5557)


    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    app.run(host="0.0.0.0", port=8888)
    thread1.join()
    thread2.join()
    print('Exit Main THread')
