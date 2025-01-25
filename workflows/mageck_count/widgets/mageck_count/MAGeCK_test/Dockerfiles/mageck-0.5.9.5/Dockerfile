FROM python:3.8.6

RUN apt-get update  

RUN pip install numpy scipy

COPY . /app

WORKDIR /app

RUN python setup.py install

ENTRYPOINT echo "Welcome to MAGeCK Docker" & mageck --version & /bin/bash 

