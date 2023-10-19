from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import struct

server_addr = ('localhost', 10000)
# int, int, char[1]
unpacker = struct.Struct('I I 1s')
with socket(AF_INET, SOCK_STREAM) as server:
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(server_addr)
    server.listen(1)

    while True:
        client, client_addr = server.accept()
        print("Connected: ", client_addr)

        data = client.recv(unpacker.size)
        print("Received:", data)

        unp_data = unpacker.unpack(data)
        print("Unpacked:", unp_data)

        x = eval(str(unp_data[0]) + unp_data[2].decode() + str(unp_data[1]))

        client.sendall(str(x).encode())