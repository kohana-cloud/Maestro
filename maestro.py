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
    '1Cbas2ZWQ8Kq': {
        'type': 'VPS',
        'os': 'Ubuntu 20.04',
        'owner': 12345,
        'updated': 1652508781,
        'health': 0
    },
    'w8w5t32JFMzT': {
        'type': 'VPS',
        'os': 'Ubuntu 20.04',
        'owner': 12345,
        'updated': 1653760662,
        'health': 1
    },
    'hFc8c7Hhr8wj': {
        'type': 'Database',
        'os': 'Ubuntu 20.04',
        'owner': 12345,
        'updated': 1651953237,
        'health': 3
    },
    '0ooQzs78Aizu': {
        'type': 'Database',
        'db-engine': 'mysql',
        'owner': 12345,
        'updated': 1651993737,
        'health': 0
    },
    '0SK8zO8VB8Wj': {
        'type': 'NAS',
        'owner': 12345,
        'updated': 1651123437,
        'health': 3
    },
    'qVAUYY6C67tv': {
        'type': 'Database',
        'db-engine': 'mysql',
        'owner': 12345,
        'updated': 1651933123,
        'health': 2
    }
}


class QueryServer(rpc.QueryServer):
    def __init__(self): pass

    def GetHoneypots(self, request, context):
        print(f"[{datetime.now()}] QueryServer received gRPC call -- Retrieve Honeypots")
        return query.Honeypots(HoneypotsAsJSON = json.dumps(honeypots), count = len(honeypots))

    def NewHoneypot(self, request, context):
        print(f"[{datetime.now()}] QueryServer received gRPC call -- New Honeypot")
        new_uuid = str(uuid.uuid1())[:12]

        honeypots[new_uuid] = {
                'type': 'NAS',
                'owner': 12345,
                'updated': int(time.time()),
                'health': 0
                }
        
        return query.ReturnCode()


def start_server(tls=True):
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


if __name__ == '__main__':
    aws_internal_session = AWS_Session()
    #aws_internal_session.get_all_services()
    start_server()