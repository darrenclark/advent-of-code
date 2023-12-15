cmake_minimum_required(VERSION 3.28)

project(rocks VERSION 1.0 LANGUAGES OBJCXX)

add_executable(rocks main.mm)

set(CMAKE_OBJC_FLAGS "-fobjc-arc")
set(CMAKE_OBJCXX_FLAGS "-fobjc-arc")
set_property(TARGET rocks PROPERTY CXX_STANDARD 17)

target_link_libraries(rocks
    "-framework Foundation"
)
