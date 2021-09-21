#!/usr/bin/python3

import socket
import threading
from string import *

class Handler(threading.Thread):
    def __init__(self,local_host,local_port):
        threading.Thread.__init__(self,name="messenger_receiver")
        self.host = local_host
        self.port = local_port
        self.dataRecived = ""

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host,self.port))
        sock.listen(16)
        while True:
            connection, client_address = sock.accept()
            try:
                message = ""
                while True:
                    character = connection.recv(1)
                    message +=character.decode("utf-8")
                    print(message)
            except Exception as e:
                print("Error:" + e)
    def run(self):
        self.listen()
        
class Sender(threading.Thread):
    def __init__(self,remote_host,remote_port):
        threading.Thread.__init__(self,name="messenger_sender")
        self.host = remote_host
        self.port = remote_port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Waiting for peer...")

        connected = False
        while not connected:
            try:
                s.connect((self.host,self.port))
                connected = True
            except:
                ""

        while True:
            try:
                message = str(input("Digite sua mensagem:"))
                s.send(message.encode("utf-8")) 
            except Exception as e:                    
                s.shutdown(2)
                s.close()    
    
def execute(localIp, localPort, remoteIp, remotePort):
    receiver = Handler(localIp, localPort)
    sender = Sender(remoteIp, remotePort)
    treads = [sender.start(),receiver.start()]

def main():
    localIp = input("Local Ip:")
    localPort = int(input("Local Port:"))
    remoteIp = input("Remote Ip:")
    remotePort = int(input("Remote Port:"))
    execute(localIp, localPort, remoteIp, remotePort)

if __name__ == "__main__":
    main()