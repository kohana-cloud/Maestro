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

SERVER_PORT = {'unary': 15001, 'bidirectional':15002}

#honeypots = ingest_honeypots("data/honeypots.yaml")
honeypots = {
    '1a463804ea': {
        'type': 'EC2',
        'owner': 12345,
        'updated': 1652508781,
        'health': 0
    },
    '65bf0194ea': {
        'type': 'LAMBDA',
        'owner': 12345,
        'updated': 1652508781,
        'health': 1
    },
    '6b5b0b7aea': {
        'type': 'ECS',
        'owner': 12345,
        'updated': 1652508781,
        'health': 2
    },
    '714c39aaea': {
        'type': 'EC2',
        'owner': 12345,
        'updated': 1652508781,
        'health': 3
    }
}


class QueryServer(rpc.QueryServer):
    def __init__(self): pass

    def GetHoneypots(self, request, context):
        print(f"[{datetime.now()}] QueryServer received gRPC call -- retrieve honeypots")
        return query.Honeypots(HoneypotsAsJSON = json.dumps(honeypots), count = len(honeypots))

    def NewHoneypot(self, request, context):
        print(f"[{datetime.now()}] QueryServer received gRPC call -- creating new honeypot, type:{request.type}")
        tempid = str(uuid.uuid1()).replace('-','')
        new_uuid = tempid[:10]

        honeypots[new_uuid] = {
                'type': request.type.upper(),
                'owner': 12345,
                'updated': int(time.time()),
                'health': 0
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
        
        # Return something to the client honeypot
        return query.Empty()



def start_server(tls=True):
    unary_server = grpc.server(futures.ThreadPoolExecutor(max_workers=100))
    rpc.add_QueryServerServicer_to_server(QueryServer(), unary_server)

    bidirectional_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1000))
    rpc.add_HoneypotManagementServerServicer_to_server(HoneypotManagementServer(), bidirectional_server)  # register the server to gRPC

    if tls:
        with open('cert/server.key', 'rb') as fio: private_key = fio.read()
        with open('cert/server.crt', 'rb') as fio: certificate_chain = fio.read()
        
        server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain),))

        unary_server.add_secure_port(f"[::]:{SERVER_PORT['unary']}", server_credentials)
        bidirectional_server.add_secure_port(f"[::]:{SERVER_PORT['bidirectional']}", server_credentials)

    else:
        unary_server.add_insecure_port(f"[::]:{SERVER_PORT['unary']}")
        bidirectional_server.add_insecure_port(f"[::]:{SERVER_PORT['bidirectional']}")

    unary_server.start()
    print(f"[{datetime.now()}] Started unary gRPC server")

    bidirectional_server.start()
    print(f"[{datetime.now()}] Started bidirectional gRPC server")

    unary_server.wait_for_termination()
    bidirectional_server.wait_for_termination()
    



if __name__ == '__main__':
    #aws_internal_session = AWS_Session()
    #aws_internal_session.get_all_services()
    try:
        # Create a process group to capture child processes
        os.setpgrp()
        start_server()

    except KeyboardInterrupt:
        print('\r[KeyboardInterrupt] Terminating Server')

        # Ensure all children are dead
        os.killpg(0, signal.SIGKILL)