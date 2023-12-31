FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=$PYTHONPATH:/app

RUN apt-get update
RUN apt-get install nano

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt