# syntax=docker/dockerfile:1
FROM nvidia/cuda
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update
RUN apt-get install -y python3.7
RUN apt-get install -y pip
RUN pip install -r requirements.txt
COPY . /code/