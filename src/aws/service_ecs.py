import os
from threading import Thread


def aws_service_ecs_start(hpid:str, local_test=False):


    # for local docker testing
    if local_test:
        os.system(f"/usr/bin/docker start {hpid}")

    
def aws_service_ecs_stop(hpid:str, local_test=False):
    

    def stop():
        # for local docker testing
        if local_test:
            os.system(f"/usr/bin/docker stop hp_{hpid}")

    thread = Thread(target=stop)
    thread.start()

    
def aws_service_ecs_delete(hpid:str, local_test=False):

    def delete():
        # for local docker testing
        if local_test:
            os.system(f"/usr/bin/docker stop hp_{hpid}")
            os.system(f"/usr/bin/docker rm hp_{hpid}")

    thread = Thread(target=delete)
    thread.start()

    
def aws_service_ecs_create(hpid:str, local_test=False):

    def create():
        # for local docker testing
        if local_test:
            os.system(f"/usr/bin/docker run -d -it  --name \"hp_{hpid}\" --add-host \"maestro.intranet.kohana.cloud:172.16.65.136\" --env HPID={hpid} ecs-honeypot:latest")

        
    thread = Thread(target=create)
    thread.start()
    