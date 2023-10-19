from socket import socket, AF_INET, SOCK_STREAM
import time

server_addr = ('localhost', 10000)

client = socket(AF_INET, SOCK_STREAM)
client.connect(server_addr)

time.sleep(5)

client.sendall('Hello Server'.encode())
data = client.recv(16)
print(f'received: {data.decode()}')

client.close()

