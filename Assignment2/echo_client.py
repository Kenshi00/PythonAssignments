# -*- coding: utf-8 -*-
import socket

HOST = '172.16.166.107'
PORT = 12000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'hello, world')
    data = s.recv(1024)

print('received', repr(data))
