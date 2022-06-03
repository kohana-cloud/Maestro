
import proto.query_pb2_grpc as rpc
import proto.query_pb2 as query

from datetime import datetime
from time import perf_counter
import grpc
import json

SERVER_HOST = "localhost"
SERVER_PORT = 15001

class QueryClient(object):
    def __init__(self, tls:bool=False):
        if tls:
            with open('cert/server.crt', 'rb') as fio:
                tls_secret = grpc.ssl_channel_credentials(fio.read())
            self.channel = grpc.secure_channel(f"{SERVER_HOST}:{SERVER_PORT}", tls_secret)
        else:
            self.channel = grpc.insecure_channel(f"{SERVER_HOST}:{SERVER_PORT}")

        self.stub = rpc.QueryServerStub(self.channel)
    
    def get_honeypots(self):
        return self.stub.GetHoneypots(query.Empty())
    
    def new_honeypot(self):
        return self.stub.NewHoneypot(query.Honeypot())

if __name__ == "__main__":
    client = QueryClient(tls=False)
    client.new_honeypot()
    
    """
    print(f"[{datetime.now()}] Sending gRPC message")

    t1_start = perf_counter()
    honeypots = client.get_honeypots().HoneypotsAsJSON
    honeypots = json.loads(honeypots)
    print(type(honeypots))
    print(honeypots)

    print(f"[{datetime.now()}] Received gRPC response")
    t1_stop = perf_counter()
    print(f"\tround trip (fractional seconds): {t1_stop-t1_start}")"""






"""
{'1Cbas2ZWQ8Kq': {'type': 'VPS', 'os': 'Ubuntu 20.04', 'owner': 12345, 'updated': 1652508781, 'health': 0}, 'w8w5t32JFMzT': {'type': 'VPS', 'os': 'Ubuntu 20.04', 'owner': 12345, 'updated': 1653760662, 'health': 1}, 'hFc8c7Hhr8wj': {'type': 'Database', 'os': 'Ubuntu 20.04', 'owner': 12345, 'updated': 1651953237, 'health': 3}, '0ooQzs78Aizu': {'type': 'Database', 'db-engine': 'mysql', 'owner': 12345, 'updated': 1651993737, 'health': 0}, '0SK8zO8VB8Wj': {'type': 'NAS', 'owner': 12345, 'updated': 1651123437, 'health': 3}, 'qVAUYY6C67tv': {'type': 'Database', 'db-engine': 'mysql', 'owner': 12345, 'updated': 1651933123, 'health': 2}, 'yCdPU4EtIk33': {'type': 'NAS', 'owner': 12345, 'updated': 1652507693, 'health': 0}}
"""