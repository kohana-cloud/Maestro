FROM ubuntu:jammy
RUN apt-get update
RUN apt-get -y install python3 python3-pip

#TODO set AWS credentials
#ENV AWS_DEFAULT_REGION=us-east-1

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# Start the orchestrator
CMD [ "python3", "./maestro/maestro.py"]
