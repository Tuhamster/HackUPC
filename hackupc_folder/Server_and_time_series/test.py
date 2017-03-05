#!/usr/bin/env python

import socket
import sys

TCP_PORT = 12345
TCP_IP = socket.gethostbyname("ec2-34-249-135-120.eu-west-1.compute.amazonaws.com")

print(type(TCP_IP))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
