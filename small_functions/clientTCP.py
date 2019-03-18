from socket import socket, AF_INET, SOCK_STREAM
import time
import json

server_ip = '192.168.10.167'
server_port = 4001
if __name__ == '__main__':
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((server_ip, server_port))
    print(str(client.recv(2048)))
    while True:
        data = [{
            'mac': '',
            'ts': int(time.time()),
            'loc_x': '',
            'loc_y': '',
            'remark': '',
        }]
        client.send(json.dumps(data).encode())
        # print(str(client.recv(2048)))
        # client.close()