import struct
from socket import socket, AF_INET, SOCK_STREAM

server_addr = ('localhost', 10000)

packer = struct.Struct('I I 1s')

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect(server_addr)
    szam1 = input("Enter a number:")
    op = input("Enter an operand:")
    szam2 = input("Enter another number:")

    values = (int(szam1), int(szam2), op.encode())
    packed_data = packer.pack(*values)
    # packed_data = packer.pack(int(szam1), int(szam2), op.encode())

    client.sendall(packed_data)
    data = client.recv(16).decode()

    print("Result:", data)

