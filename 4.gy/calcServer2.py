from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import struct
from select import select

server_addr = ('', 10000)
# int, int, char[1]
unpacker = struct.Struct('I I 1s')
with socket(AF_INET, SOCK_STREAM) as server:
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(server_addr)
    server.listen(1)

    sockets = [server]

    while True:
        r, w, e = select(sockets, [], [], 1)

        if not (r or w or e):
            continue

        for s in r:
            if s is server:
                # kliens csatlakozik
                client, client_addr = s.accept()
                sockets.append(client)
                print("Connected", client_addr)
            else:
                data = s.recv(16)
                # ha 0 byte akkor kilepett a kliens
                if not data:
                    sockets.remove(s)
                    s.close()
                    print("Disconnected")
                else:
                    unp_data = unpacker.unpack(data)
                    print("Unpacked: ", unp_data)
                    x = eval(str(unp_data[0]) + unp_data[2].decode() + str(unp_data[1]))
                    s.sendall(str(x).encode())