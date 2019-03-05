from socket import *
import time
import json


class mtrClient:
    def __init__(self, host = '143.89.50.151', port = 4004):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET, SOCK_DGRAM)
        #self.socket.timeout = 3
        self.addr = (self.host, self.port)
       # self.socket.connect(self.addr)
     
        
    def send(self, data):
        #print(str(self.socket.recv(2048)))
        self.socket.sendto(json.dumps(data).encode(), self.addr)
        #print(str(self.socket.recv(2048)))
       # self.socket.close()

if __name__ == '__main__':
        myt = mtrClient()
        while True:
                data = {
                'Type': 'loc',
                'mac': 'testMac',
                }
                myt.send(data)
               # print ("hello!")
                time.sleep(0.2)
 

