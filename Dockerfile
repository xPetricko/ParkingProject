# syntax=docker/dockerfile:1
FROM nvidia/cuda:11.6.0-base-ubuntu20.04
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update \
    && apt-get -y install libpq-dev gcc 
RUN apt-get install -y python3
RUN apt-get install -y pip
RUN pip3 install -r requirements.txt
COPY . /code/