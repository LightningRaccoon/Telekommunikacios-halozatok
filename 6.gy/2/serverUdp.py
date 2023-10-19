from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
import struct

server_address = ('localhost', 11000)

packer = struct.Struct('15s i')

with socket(AF_INET, SOCK_DGRAM) as server:
  server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
  server.bind(server_address)

  data, client_addr = server.recvfrom(200)
  print(f"received: {data.decode()} from: {client_addr}")

  d = packer.pack("127.0.0.1".encode(), 11000)
  server.sendto(d, client_addr)