from socket import socket, AF_INET, SOCK_STREAM, timeout, SOL_SOCKET, SO_REUSEADDR
from select import select

tcp_server_addr = ('',)
udp_server_addr = ('',)

with socket(AF_INET, SOCK_STREAM) as proxyServer:
    proxyServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    proxyServer.bind(tcp_server_addr)
    proxyServer.listen(1)

    while True: