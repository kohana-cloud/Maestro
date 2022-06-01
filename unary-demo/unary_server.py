import grpc
from concurrent import futures
from datetime import datetime
import unary_pb2_grpc as pb2_grpc
import unary_pb2 as pb2


class UnaryService(pb2_grpc.UnaryServicer):
    """
    Server for receiving a sample gRPC message
    """

    def __init__(self, *args, **kwargs): pass

    def GetServerResponse(self, request, context):
        # Send receipt to stdout
        print(f"[{datetime.now()}]: {str(request).encode('utf-8')}")

        # Print out the received arguments
        hpType = request.hpType
        ownerId = request.ownerId
        startAfterBuild = request.startAfterBuild
        targetIp = request.targetIp
        targetSubnet = request.targetSubnet
        resourceAllocation = request.resourceAllocation
        
        # Define response
        response = { "success": True, "errorCode": 0 }

        # Serialize and return response
        return pb2.StartHoneypotResponse(**response)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_UnaryServicer_to_server(UnaryService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()