cmake_minimum_required(VERSION 3.10)
project(zeromq_cpp_client)


find_package(cppzmq)
add_executable(cpp_client client.cpp)
target_link_libraries(cpp_client cppzmq)
