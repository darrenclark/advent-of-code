cmake_minimum_required(VERSION 3.28)

project(galaxies VERSION 1.0 LANGUAGES CXX)

add_executable(galaxies main.cpp)

set_property(TARGET galaxies PROPERTY CXX_STANDARD 17)
