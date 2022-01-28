# syntax=docker/dockerfile:1

FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev default-libmysqlclient-dev build-essential

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
RUN pip3 install mysqlclient

EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD [ "run.py" ]