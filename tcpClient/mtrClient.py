from socket import  *
import time
import json


class mtrClient:
    def __init__(self, host = '192.168.2.167', port = 4000):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)
       # self.socket.timeout = 3
        self.addr = (self.host, self.port)
       # self.socket.connect(self.addr)
     
        
    def sendData(self, data):
        #print(str(self.socket.recv(2048)))
        self.socket.sendto(json.dumps(data).encode(),self.addr)
       # print(str(self.socket.recv(2048)))
       # self.socket.close()
 

if __name__ == '__main__':
	mtr = mtrClient()
	mtr.sendData('hello')
