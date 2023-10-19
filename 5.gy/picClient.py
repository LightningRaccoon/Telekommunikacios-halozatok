import socket


with open("img.png", "rb") as image:
    f = image.read()
    b = bytearray(f)
    print(b[0], len(b))

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    server_address = ('localhost', 10001)

    start = 0
    while start < len(b):
        data = b.slice(start, start+200)
        sock.sendto(data, server_address)