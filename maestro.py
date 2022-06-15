from concurrent import futures
import uuid
import proto.query_pb2_grpc as rpc
import proto.query_pb2 as query
import grpc
from datetime import datetime
from src.Honeypots import ingest_honeypots
from src.aws_session import AWS_Session
import json, time

SERVER_PORT = 15001

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


def start_server(tls=True):
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1000))
        rpc.add_QueryServerServicer_to_server(QueryServer(), server)

        if tls:
            with open('cert/server.key', 'rb') as fio: private_key = fio.read()
            with open('cert/server.crt', 'rb') as fio: certificate_chain = fio.read()
            
            server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain),))   
            server.add_secure_port(f"[::]:{SERVER_PORT}", server_credentials)

        else:
            server.add_insecure_port(f"[::]:{SERVER_PORT}")

        server.start()
        server.wait_for_termination()
    except KeyboardInterrupt:
        print('\rTerminating Server')
        exit()


if __name__ == '__main__':
    #aws_internal_session = AWS_Session()
    #aws_internal_session.get_all_services()
    start_server()