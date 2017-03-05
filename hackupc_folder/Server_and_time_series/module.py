#!/usr/bin/env python

import socket
from time import sleep

#TCP_IP = socket.gethostbyname('ec2-34-249-135-120.eu-west-1.compute.amazonaws.com')
TCP_IP = "10.4.180.103"
TCP_PORT = 12345
BUFFER_SIZE = 1024

print(TCP_IP)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

print("Connected!")

s.send(bytearray("module", "utf-8"))
sleep(5)
s.send(bytearray("on", "utf-8"))

while 1:
	data = s.recv(BUFFER_SIZE)
	if not data:
		break
	print(data.decode("utf-8"))
s.close()