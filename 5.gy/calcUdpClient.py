from socket import socket,AF_INET, SOCK_DGRAM, timeout, SOL_SOCKET, SO_REUSEADDR
import struct

server_address = ('localhost', 10001)

packer = struct.Struct('I I 1s')

with socket(AF_INET, SOCK_DGRAM) as client:
  num1 = input("Enter a number:")
  op = input("Enter an operand:")
  num2 = input("Enter another number:")

  values = (int(num1),int(num2), op.encode())
  packed_data = packer.pack(*values)

  print (f"Sending: {values}")
  client.sendto(packed_data, server_address)
  data, sock = client.recvfrom(16)
  print (f"Result: {data.decode()} from {sock}")