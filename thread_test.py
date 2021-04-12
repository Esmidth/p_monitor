import threading
import time
from typing import AbstractSet
import zmq

from flask import Flask, Response
from prometheus_client import Counter, Gauge,Histogram,Summary,generate_latest,CollectorRegistry, registry


app = Flask(__name__)
registry = CollectorRegistry()
# counter = Counter('my_counter','',['machine_ip'],registry=registry)
# gauge = Gauge('my_gauge','',['machine_ip'],registry=registry)
# buckets = (100,200,300,500,1000,3000,10000,float('inf'))
# histogram = Histogram('my_histogram','',['machine_ip'],registry=registry,buckets=buckets)
# summary = Summary('my_summary','an example ',['machine_ip'],registry=registry)

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
    # counter.labels('127.0.0.1').inc(1)
    # gauge.labels('127.0.0.1').set(2)
    # histogram.labels('127.0.0.1').observe(1001)
    # summary.labels('127.0.0.1').observe(1)
    global perf_metric_dict_list
    # return Response(str(perf_metric_dict_list),mimetype='text/plain')
    return Response(generate_latest(registry),mimetype='text/plain')


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
        self.perf_metric_dict = {}

    def getData(self, input_string):
        global perf_metric_dict_list
        self.perf_metric_dict = {}
        split_num = input_string.count(',')
        # print(split_num)
        split_res = input_string.split(',', split_num)
        for sub_string in split_res:
            sub_string_split = sub_string.split(':', 1)
            self.perf_metric_dict[sub_string_split[0]] = int(sub_string_split[1])
        

        id = self.perf_metric_dict['nodeNum']
        # print(id)
        if id >= len(perf_metric_dict_list):
            perf_metric_dict_list.append(self.perf_metric_dict)
        else:
            perf_metric_dict_list[id] = self.perf_metric_dict


    def register(self):
        self.para_dict = {}
        for item in self.perf_metric_dict:
            self.para_dict[item] = Gauge(item+str(self.threadID),'',['machine_ip'],registry=registry)
            # print(item)
        # print(self.para_dict)
        # print('------')

    def update_registry(self):
        for item in self.perf_metric_dict:
            self.para_dict[item].labels('127.0.0.1').set(self.perf_metric_dict[item])



        # self.perf_metric_dict = perf_metric_dict

    def run(self):
        global global_sec
        message = self.socket.recv().decode()
        self.getData(message)
        self.register()
        global_sec = 0
        self.socket.send_string('1')


        while True:
            message = self.socket.recv().decode()
            print(type(message))
            self.getData(message)
            self.update_registry()
            self.socket.send_string("123")
            # print("sec:{}, message: {}".format(global_sec, message))


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
    thread2 = DataCatcher(0,portID=5555)
    thread3 = DataCatcher(1,portID=5556)
    thread4 = DataCatcher(1,portID=5557)


    thread1.start()
    thread2.start()
    # thread3.start()
    # thread4.start()

    app.run(host="0.0.0.0", port=8888)
    thread1.join()
    thread2.join()
    print('Exit Main THread')
