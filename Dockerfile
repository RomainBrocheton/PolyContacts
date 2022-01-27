# syntax=docker/dockerfile:1

FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

# ENTRYPOINT [ "python" ]
CMD [ "python", "run.py" ]