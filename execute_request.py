
import proto.query_pb2_grpc as rpc
import proto.query_pb2 as query

from datetime import datetime
from time import perf_counter
import grpc

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

if __name__ == "__main__":
    client = QueryClient(tls=False)

    print(f"[{datetime.now()}] Sending gRPC message")
    t1_start = perf_counter()
    result = client.get_honeypots()
    print(f"[{datetime.now()}] Received gRPC response")
    t1_stop = perf_counter()
    print(f"\tround trip (fractional seconds): {t1_stop-t1_start}")

