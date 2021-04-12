#include <string>
#include <iostream>
#include <thread>
#include <stdlib.h>

#include <zmq.hpp>

struct Perf_Metrics
{
    unsigned short nodeNum;
    unsigned long sec;
    unsigned long align_frame;
    unsigned long sent_frame;
    unsigned long forward_packets;
    unsigned long consume_packets;
    unsigned long missing_packets;
    unsigned long drop_frames;
    unsigned long missing_frames;
    unsigned long consumer_speed;
    unsigned long recv_speed;
    unsigned short queue1_size;
    unsigned short queue2_size;
    unsigned short queue3_size;
};

void timer(int id)
{
    printf("ID: %d\n", id);
    // init perf_mertics
    Perf_Metrics metric;
    metric.nodeNum = id;
    metric.sec = 1;
    metric.align_frame = 2;
    metric.sent_frame = 3;
    metric.forward_packets = 4;
    metric.consume_packets = 5;
    metric.missing_packets = 6;
    metric.drop_frames = 7;
    metric.missing_frames = 8;
    metric.consumer_speed = 9;
    metric.recv_speed = 10;
    metric.queue1_size = 11;
    metric.queue2_size = 12;
    metric.queue3_size = 13;

    zmq::context_t context{1};
    zmq::socket_t socket{context, zmq::socket_type::req};
    socket.connect("tcp://localhost:"+std::to_string(5555+id));
    const std::string data{" Hello from client @ sec: "};
    int sec = 0;
    while (true)
    {
        // std::string tmp = "id"+std::to_string(id)+data+std::to_string(sec);
        std::string tmp = "nodeNum:" + std::to_string(metric.nodeNum) + "," +
                          "sec:" + std::to_string(metric.sec) + "," +
                          "align_frame:" + std::to_string(metric.align_frame) + "," +
                          "sent_frame:" + std::to_string(metric.sent_frame);
        // socket.send(zmq::buffer(&metric,sizeof(Perf_Metrics)), zmq::send_flags::none);
        socket.send(zmq::buffer(tmp), zmq::send_flags::none);

        // // wait for reply from server
        zmq::message_t reply{};
        socket.recv(reply, zmq::recv_flags::none);

        // std::cout << "Received " << reply.to_string();
        // std::cout << " (" << sec << ")";
        // std::cout << std::endl;
        printf("sec:%d\n", metric.sec);
        metric.sec += 1;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

int main()
{

    std::thread t1(timer, 0);
    std::thread t2(timer, 1);
    std::thread t3(timer, 2);
    // initialize the zmq context with a single IO thread

    // construct a REQ (request) socket and connect to interface

    // set up some static data to send
    t1.join();

    return 0;
}