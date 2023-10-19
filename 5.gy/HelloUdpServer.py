import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  server_address = ('localhost', 10001)
  sock.bind(server_address)

  while True:
    data, client = sock.recvfrom(200)
    print (f'received: {data.decode()}')
    sock.sendto("Hello client!".encode(), client)