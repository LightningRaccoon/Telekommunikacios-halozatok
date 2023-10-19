import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
  server_address = ('localhost', 10001)

  sock.sendto("Hello server!".encode(), server_address)
  data, _ = sock.recvfrom(200)
  print (f'received: {data.decode()}')
