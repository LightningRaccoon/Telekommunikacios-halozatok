from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from select import select
import struct

packer = struct.Struct('I I 1s')

proxy_addr = ('localhost', 10000)
server_addr = ('localhost', 10001)

with socket(AF_INET, SOCK_STREAM) as server, socket(AF_INET, SOCK_DGRAM) as proxy_client:
  server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
  server.bind(proxy_addr)
  server.listen(1)

  inputs = [server]

  while True:
    r, w, e = select(inputs,inputs,inputs)
    if not (r or w or e):
      continue

    for s in r:
      if s is server:
        client, client_addr = s.accept()
        inputs.append(client)
        print(f"connected: {client_addr}")
      else:
        data = s.recv(packer.size)
        if not data:
          print(f"disconnected: {s.getpeername()}")
          inputs.remove(s)
          s.close()
        else:
          proxy_client.sendto(data, server_addr)
          res, _ = proxy_client.recvfrom(200)
          s.sendall(res)