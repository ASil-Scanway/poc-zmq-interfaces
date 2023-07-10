FROM python:3.11
LABEL authors="olek1"

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN apt-get update && apt-get install -y \
    nano ffmpeg libsm6 libxext6 libgl1

RUN pip3 install poetry

RUN poetry config virtualenvs.create false
