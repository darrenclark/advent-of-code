cmake_minimum_required(VERSION 3.28)

project(hot-springs VERSION 1.0 LANGUAGES OBJC)

add_executable(hot-springs main.m)

set(CMAKE_OBJC_FLAGS "-fobjc-arc")
set(CMAKE_OBJCXX_FLAGS "-fobjc-arc")

target_link_libraries(hot-springs
    "-framework Foundation"
)
