#!/usr/bin/env python
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 2137))
s.sendall('Hello Python!'.encode('utf-8'))
data = s.recv(1024)
s.close()

print("received data:", data.decode())