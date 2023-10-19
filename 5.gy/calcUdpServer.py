from socket import socket,AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
import struct

server_address = ('localhost', 10001)
unpacker = struct.Struct('I I 1s')

with socket(AF_INET, SOCK_DGRAM) as server:
  server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
  server.bind(server_address)

  while True:
    data, client = server.recvfrom(unpacker.size)
    unp_data = unpacker.unpack(data)

    print(f"received: {unp_data} from {client}")

    x = eval(str(unp_data[0])+unp_data[2].decode()+str(unp_data[1]))

    server.sendto(str(x).encode(), client)