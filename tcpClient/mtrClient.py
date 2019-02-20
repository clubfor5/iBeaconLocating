from socket import socket, AF_INET, SOCK_STREAM
import time
import json


class mtrClient:
    def __init__(self, host = '192.168.2.11', port = 4001):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.addr = (self.host, self.port)
        self.socket.connect(self.addr)
        
    def sendData(self, data):
        #print(str(self.socket.recv(2048)))
        self.socket.send(json.dumps(data).encode())
        print(str(self.socket.recv(2048)))
       # self.socket.close()
 

