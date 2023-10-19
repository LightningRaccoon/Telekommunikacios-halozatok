import random
import struct
from socket import socket, AF_INET, SOCK_STREAM
import time
import sys

hostname = sys.argv[1]
port = sys.argv[2]
server_addr = (hostname, int(port))

client = socket(AF_INET, SOCK_STREAM)
client.connect(server_addr)

min = 1
max = 100
mid = round(min + max / 2)
op = random.randint(1, 2)
prevStep = mid

if op == 1:
    startSymbol = '>'
else:
    startSymbol = '<'

packer = struct.Struct('c I')
end = False

while not end:
    #time.sleep(1)
    #print(f"MinMax: {min} - {max} - {mid}")
    packed = packer.pack(startSymbol.encode(), mid)
    client.sendall(packed)

    data = client.recv(16)

    unpdata = packer.unpack(data)
    #print(unpdata)

    if unpdata[0].decode() == "V":
        #print(mid)
        end = True
    elif unpdata[0].decode() == "K":
        #print(mid)
        end = True
    elif unpdata[0].decode() == "Y":
        #print(mid)
        end = True
    elif unpdata[0].decode() == "I":
        #print("I lépés")
        #print(f"perv: {prevStep}, {mid}, {min}, {max}")

        if max-min == 2:
            startSymbol = '='
        else:
            if startSymbol == '>':
                min = mid
            else:
                max = mid
            mid = round((min + max) / 2)

        #print(f"after: {prevStep}, {mid}, {min}, {max}")
    elif unpdata[0].decode() == "N":
        #print("N lépés")
        #print(f"perv: {prevStep}, {mid}, {min}, {max}")
        if max - min == 2:
            startSymbol = '='
        else:
            if prevStep != mid:
                if startSymbol == '>':
                    max = mid
                    min = prevStep
                else:
                    min = mid
                    max = prevStep
            else:
                if startSymbol == '>':
                    max = mid
                else:
                    min = mid

        mid = round((min + max) / 2)
        #print(f"after: {prevStep}, {mid}, {min}, {max}")
    #print("\n")

    prevStep = mid
client.close()
