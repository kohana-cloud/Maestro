import proto.chat_pb2_grpc as rpc
import proto.chat_pb2 as chat
import threading
import grpc
import uuid
import time

class Client:
    def __init__(self, username):
        self.chat_list = []
        self.username = username

        # create a gRPC channel + stub
        channel = grpc.insecure_channel('localhost:11912')
        self.connection = rpc.ChatServerStub(channel)

        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen_for_messages, daemon=True).start()

    def __listen_for_messages(self):
        """
        Must run in a separate thread from main/ui as it the message stream is blocking
        """
        for note in self.connection.ChatStream(chat.Empty()):  # this line will wait for new messages from the server!
            print(f"R[{note.name}] {note.message}")  # debugging statement
            #self.chat_list.append(f"[{note.name}] {note.message}\n")  # add the message to the UI

    def send_message(self):
        message = "received a message"
        n = chat.Note()  # create protobug message (called Note)
        n.name = self.username  # set the username
        n.message = message  # set the actual message of the note
        #print(f"\nS[{n.name}] {n.message}")  # debugging statement
        self.connection.SendNote(n)  # send the Note to the server

if __name__ == '__main__':
    username = str(uuid.uuid1()).encode('utf8')
    
    # start a client (distinct thread) which keeps connection to server open
    c = Client(username)

    while True:
        input("Press [enter] to send message.")
        c.send_message()