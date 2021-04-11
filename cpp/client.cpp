#include <string>
#include <iostream>
#include <thread>
#include <stdlib.h>

#include <zmq.hpp>

void timer(int id)
{
    printf("ID: %d\n",id);
    zmq::context_t context{1};
    zmq::socket_t socket{context, zmq::socket_type::req};
    socket.connect("tcp://localhost:5555");
    const std::string data{" Hello from client @ sec: "};
    int sec = 0;
    while (true)
    {
        std::string tmp = "id"+std::to_string(id)+data+std::to_string(sec);
        socket.send(zmq::buffer(tmp), zmq::send_flags::none);

        // wait for reply from server
        zmq::message_t reply{};
        socket.recv(reply, zmq::recv_flags::none);

        std::cout << "Received " << reply.to_string();
        std::cout << " (" << sec << ")";
        std::cout << std::endl;
        printf("sec:%d\n", sec);
        sec++;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

int main()
{

    std::thread t1(timer,1);
    std::thread t2(timer,2);
    // initialize the zmq context with a single IO thread

    // construct a REQ (request) socket and connect to interface

    // set up some static data to send
    t1.join();

    return 0;
}