import socket
import json


class mtrClient:
    def __init__(self, host = '143.89.144.200', port = 4000):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = (self.host, self.port)
        #self.socket.connect(self.addr)
        
    def sendData(self, data):
        #print(str(self.socket.recv(2048)))
        try: 
      	    self.socket.sendto(json.dumps(data).encode(),self.addr)
        except:
	        print("no network")
       #  print(str(self.socket.recv(2048)))
       #  self.socket.close()
 

