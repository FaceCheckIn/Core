FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apt-get update && apt-get upgrade
# RUN apt-get update && apt-get install -y netcat
RUN apt-get update && apt-get install -y cmake
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /code

RUN pip install --upgrade pip

RUN export DOCKER_CLIENT_TIMEOUT=300
RUN export COMPOSE_HTTP_TIMEOUT=300

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000