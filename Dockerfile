# syntax=docker/dockerfile:1
FROM nvidia/cuda
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/