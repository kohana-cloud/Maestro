import unary_pb2_grpc as pb2_grpc
import unary_pb2 as pb2
import grpc

class UnaryClient(object):
    """
    Client for sending a sample gRPC message
    """

    def __init__(self):
        self.host = 'localhost'
        self.port = 50051

        # instantiate a channel
        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")

        # bind the client and the server
        self.stub = pb2_grpc.UnaryStub(self.channel)

    def start_honeypot(self):
        """
        Client function to call the rpc for StartHoneypot
        """
        message = pb2.StartHoneypot(
            hpType = 1,
            ownerId = 987654321,
            startAfterBuild = True,
            targetIp = 2923507574,
            targetSubnet = 4294934528,
            resourceAllocation = 2
        )
        
        with open('unary.data','bw') as fio:
            fio.write(message.SerializeToString())

        with open('rest.data','tw') as fio:
            fio.write("{hpType: 1, ownerId: 9876543120, startAfterBuild: True, targetIp: 192.168.1.1, subnetMask: 255.255.128.0, resourceAllocation: medium}")
        
        print(f"Sending: {message}")
        return self.stub.GetServerResponse(message)


if __name__ == "__main__":
    client = UnaryClient()
    result = client.start_honeypot()
    print(f"Received: {result}")
