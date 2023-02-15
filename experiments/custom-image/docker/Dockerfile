FROM public.ecr.aws/lambda/python:3.8

ARG CMAKE_VER=3.21.3
RUN curl -sSL https://github.com/Kitware/CMake/releases/download/v${CMAKE_VER}/cmake-${CMAKE_VER}-linux-x86_64.tar.gz -o /cmake.tar.gz
RUN mkdir -p /opt/cmake && tar -xf /cmake.tar.gz -C /opt/cmake --strip-components 1


curl -sSL https://github.com/Kitware/CMake/releases/download/v3.21.3/cmake-3.21.3-linux-x86_64.tar.gz -o /cmake.tar.gz
## cmake will be installed under /opt/cmake/bin/cmake
ENV PATH="/opt/cmake/bin/:${PATH}"