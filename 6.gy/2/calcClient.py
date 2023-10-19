from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
from time import sleep
import struct

packer = struct.Struct('15s i')

server_address = ('localhost', 11000)

with socket(AF_INET, SOCK_DGRAM) as client:
  client.sendto("GET".encode(), server_address)

  data, _ = client.recvfrom(packer.size)
  unpacked_data = packer.unpack(data)
  print(f"received: {unpacked_data}")
  server_addr = (unpacked_data[0].decode().strip("\0"), unpacked_data[1])

packer = struct.Struct('I I 1s')

with socket(AF_INET,SOCK_STREAM) as client:
  a = input("Enter a number:")
  b = input("Enter an operand:")
  c = input("Enter another number:")

  packed_data = packer.pack(int(a), int(c), b.encode())
  client.connect(server_addr)

  client.sendall(packed_data)
  data = client.recv(200)
  print(f"result: {data.decode()}")