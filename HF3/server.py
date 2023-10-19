import random
import struct
import sys
import time
from select import select
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

hostname = sys.argv[1]
port = sys.argv[2]
server_addr = (hostname, int(port))

#print("Received hostname and port:" + hostname + " - " + port)

# int, int, char[1]
packer = struct.Struct('c I')
#t_end = time.time() + 60 * 1


def handleGuess(op, num):
    if op == '=' and num == guess:
        return (True, "eq")
    elif op == ">" and guess > num:
        return (True, "big")
    elif op == "<" and guess < num:
        return (True, "sma")
    if op == '=' and num != guess:
        return (False, "eq")
    else:
        return (False, "N")


def checkInputChar(c):
    possibleChars = ["<", ">", "="]
    if c in possibleChars:
        return True
    else:
        return False


#print("Setting up server...")
guess = random.randint(1, 100)
#print(f"Guess: {guess}\n")

with socket(AF_INET, SOCK_STREAM) as server:
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(server_addr)
    server.listen(1)

    sockets = [server]
    end = False
    gameEnd = False

    while True:
        r, w, e = select(sockets, [], [], 1)

        if not (r or w or e):
            continue

        for s in r:
            if s is server:
                # kliens csatlakozik
                client, client_addr = s.accept()
                sockets.append(client)
                #print("Connected", client_addr)
            else:
                data = s.recv(16)
                # ha 0 byte akkor kilepett a kliens
                if not data:
                    sockets.remove(s)
                    s.close()
                    # print("Disconnected")
                elif not gameEnd:
                    if not end:
                        unp_data = packer.unpack(data)
                        # print("Unpacked: ", unp_data)
                        if checkInputChar(unp_data[0].decode()):
                            eq_bool = handleGuess(unp_data[0].decode(), unp_data[1])
                            #print(eq_bool)
                            if eq_bool[0] and eq_bool[1] == 'sma' or eq_bool[1] == 'big':
                                answer = packer.pack('I'.encode(), 0)
                                s.sendall(answer)
                            elif eq_bool[0] and eq_bool[1] == 'eq':
                                answer = packer.pack('Y'.encode(), 0)
                                s.sendall(answer)
                                end = True
                            elif not eq_bool[0] and eq_bool[1] == 'eq':
                                answer = packer.pack('K'.encode(), 0)
                                s.sendall(answer)
                            else:
                                answer = packer.pack('N'.encode(), 0)
                                s.sendall(answer)
                    else:
                        answer = packer.pack('K'.encode(), 0)
                        s.sendall(answer)
                        gameEnd = True
                else:
                    answer = packer.pack('V'.encode(), 0)
                    s.sendall(answer)

    #print("Shutting down server...")
