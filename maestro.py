from concurrent import futures
import uuid
import proto.query_pb2_grpc as rpc
import proto.query_pb2 as query
import grpc
from datetime import datetime
#from src.aws_session import AWS_Session
import json, time
import random
import os, signal
from os.path import exists
from src.configuration import Configuration
from threading import Thread

SERVER_PORT = {'unary': 15001, 'bidirectional':15002}
HEALTH_CHECK_INTERVAL_SECONDS = 3

#honeypots = ingest_honeypots("data/honeypots.yaml")
honeypots = {
    '859a277c-f3ff-11ec-a661-000c2970a8e4': {
        'type': 'EC2',
        'owner': 12345,
        'updated': 1652508781,
        'health': 1,
        'last_heartbeat': 0
    },
    '92c75190-f3ff-11ec-a661-000c2970a8e4': {
        'type': 'LAMBDA',
        'owner': 12345,
        'updated': 1652508781,
        'health': 1,
        'last_heartbeat': 0
    }
}


class QueryServer(rpc.QueryServer):
    def __init__(self): pass

    def GetHoneypots(self, request, context):
        print(f"[{datetime.now()}] QueryServer received gRPC call -- retrieve honeypots")
        return query.Honeypots(HoneypotsAsJSON = json.dumps(honeypots), count = len(honeypots))

    def NewHoneypot(self, request, context):
        print(f"[{datetime.now()}] QueryServer received gRPC call -- creating new honeypot, type:{request.type}")

        honeypots[str(uuid.uuid1())] = {
                'type': request.type.upper(),
                'owner': 12345,
                'updated': int(time.time()),
                'health': 1,
                'last_heartbeat': 0
                }
        
        return query.ReturnCode()


class HoneypotManagementServer(rpc.HoneypotManagementServer):
    def __init__(self): self.chats = []

    def ChatStream(self, request_iterator, context):
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while True: pass

        #commands to be implemented here, but currently NA

    def SendEvent(self, request: query.Event, context):
        # Called when a client sends an event to the server.

        # Log to server
        print(f"[{datetime.now()}] {request.type} - {request.message}")

        if request.type == "connection":
            if request.message.split(':')[0] == "connect":
                #live attacker present in machine
                honeypots[request.message.split(':')[1]]['health'] = 3
                honeypots[request.message.split(':')[1]]['updated'] = int(time.time())
            elif request.message.split(':')[0] == "disconnect":
                #live attacker no longer present in machine
                honeypots[request.message.split(':')[1]]['health'] = 2
                honeypots[request.message.split(':')[1]]['updated'] = int(time.time())

        if request.type == "status":
            if request.message.split(':')[0] == "heartbeat":
                honeypots[request.message.split(':')[1]]['last_heartbeat'] = int(time.time())
                
                # Set healthy if currently degraded and recieves a heartbeat
                if (honeypots[request.message.split(':')[1]]['health'] == 1): 
                    honeypots[request.message.split(':')[1]]['health'] = 0
                    honeypots[request.message.split(':')[1]]['updated'] = int(time.time())
        
        # Return something to the client honeypot
        return query.Empty()



def degrade_unresponsive_honeypots():
    while True:
        current_time = int(time.time())
        for honeypot in honeypots:
            # check if the hp hasn't been updated in a bit
            if (honeypots[honeypot]['last_heartbeat'] < (time.time() - 3)) and (honeypots[honeypot]['health'] == 0):
                honeypots[honeypot]['health'] = 1
                honeypots[honeypot]['updated'] = int(time.time())
                
        time.sleep(HEALTH_CHECK_INTERVAL_SECONDS)



def start_server(configuration:object):
    unary_server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    rpc.add_QueryServerServicer_to_server(QueryServer(), unary_server)

    bidirectional_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1000))
    rpc.add_HoneypotManagementServerServicer_to_server(HoneypotManagementServer(), bidirectional_server)  # register the server to gRPC

    if configuration.tls_enabled:        
        server_credentials = grpc.ssl_server_credentials(((configuration.private_key, certificate_chain)))

        unary_server.add_secure_port(f"0.0.0.0:{SERVER_PORT['unary']}", server_credentials)
        bidirectional_server.add_secure_port(f"0.0.0.0:{SERVER_PORT['bidirectional']}", server_credentials)

    else:
        unary_server.add_insecure_port(f"0.0.0.0:{SERVER_PORT['unary']}")
        bidirectional_server.add_insecure_port(f"0.0.0.0:{SERVER_PORT['bidirectional']}")

    unary_server.start()
    print(f"[{datetime.now()}] started unary gRPC server")

    bidirectional_server.start()
    print(f"[{datetime.now()}] started bidirectional gRPC server")

    health_monitor_thread = Thread(target=degrade_unresponsive_honeypots)
    health_monitor_thread.start()
    

    unary_server.wait_for_termination()
    bidirectional_server.wait_for_termination()
    health_monitor_thread.join()
    



if __name__ == '__main__':
    #aws_internal_session = AWS_Session()
    #aws_internal_session.get_all_services()

    configuration = Configuration('configuration.yaml')
    configuration.read_keys()

    try:
        # Create a process group to capture child processes
        os.setpgrp()

        # Start server with provided configuration
        start_server(configuration)

    except KeyboardInterrupt:
        print('\r[KeyboardInterrupt] Terminating Server')

        # Ensure all children are dead
        os.killpg(0, signal.SIGKILL)