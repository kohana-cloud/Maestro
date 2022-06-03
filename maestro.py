from concurrent import futures
import proto.query_pb2_grpc as rpc
import proto.query_pb2 as query
import grpc
from datetime import datetime

SERVER_PORT = 15001

class QueryServer(rpc.QueryServer):
    def __init__(self): pass

    def GetHoneypots(self, request, context):
        print(f"[{datetime.now()}] QueryServer received gRPC call")
    
        return query.Honeypots(
                HoneypotsAsJSON = "{key:value}",
                count = 1
            )

def server(tls=True):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_QueryServerServicer_to_server(QueryServer(), server)

    if tls:
        with open('cert/server.key', 'rb') as f:
            private_key = f.read()
        with open('cert/server.crt', 'rb') as f:
            certificate_chain = f.read()
        server_credentials = grpc.ssl_server_credentials(
            ((private_key, certificate_chain),))
            
        server.add_secure_port(f"[::]:{SERVER_PORT}", server_credentials)
    else:
        server.add_insecure_port(f"[::]:{SERVER_PORT}")

    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    server(tls=False)