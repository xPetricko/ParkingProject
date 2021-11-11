# syntax=docker/dockerfile:1
FROM nvidia/cuda:11.3.0-devel-ubuntu20.04
WORKDIR /code
COPY requirements.txt /code/

RUN apt-get update && \
  apt-get install -y --no-install-recommends git wget unzip bzip2 sudo build-essential && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN apt update

RUN apt-get install -y python3.8 python3-pip

RUN  pip install --upgrade pip && \
  rm -rf ~/.cache/pip


RUN pip install -r requirements.txt
RUN pip3 install torch==1.10.0+cu113 torchvision==0.11.1+cu113 torchaudio==0.10.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html --no-cache-dir

COPY . /code/