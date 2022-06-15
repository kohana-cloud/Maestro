FROM ubuntu:jammy
RUN apt-get update
RUN apt-get install python3 python3-pip -y

ENV AWS_DEFAULT_REGION=us-east-1
#TODO set AWS credentials

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
CMD [ "python3", "./maestro/maestro.py"]

EXPOSE 15001