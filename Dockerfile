FROM python:3.7.9

WORKDIR /dev

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r /requirements.txt

COPY . .