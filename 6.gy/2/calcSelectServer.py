from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct
from select import select

server_addr = ('localhost', 11000)
unpacker = struct.Struct('I I 1s')  # int, int, char[1]

with socket(AF_INET, SOCK_STREAM) as server:
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(server_addr)
    server.listen(1)

    socketek = [server]

    while True:
        r, w, e = select(socketek, [], [], 1)

        if not (r or w or e):
            continue

        for s in r:
            if s is server:
                # kliens csatlakozik
                client, client_addr = s.accept()
                socketek.append(client)
                print("Connected", client_addr)
            else:
                data = s.recv(unpacker.size)
                # ha 0 byte akkor kilepett a kliens
                if not data:
                    socketek.remove(s)
                    s.close()
                    print("Disconnected")
                else:
                    unp_data = unpacker.unpack(data)
                    print("Unpacked:", unp_data)
                    x = eval(str(unp_data[0]) + unp_data[2].decode() + str(unp_data[1]))
                    s.sendall(str(x).encode())