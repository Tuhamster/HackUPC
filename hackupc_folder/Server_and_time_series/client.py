#!/usr/bin/env python

import socket


TCP_IP = socket.gethostbyname('ec2-34-249-135-120.eu-west-1.compute.amazonaws.com')
#TCP_IP = "10.4.180.103"
TCP_PORT = 12345
BUFFER_SIZE = 1024

print(TCP_IP)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

print("Connected!")
s.send(bytearray("switch/on", "utf-8"))

data = s.recv(BUFFER_SIZE)
print("Status:", data.decode("utf-8"))


s.close()


'''
while 1:
	data = input("Enter data: ")
	s.send(bytearray(data, "utf-8"))

	data = s.recv(BUFFER_SIZE)
	print(data.decode("utf-8"))

s.close()
'''

'''
		while 1:
			global module_conn
			global module_state
			app_data = app_conn.recv(BUFFER_SIZE)
			print(app_data.decode("utf-8"))
			app_conn.send(bytearray("ACK", "utf8"))

			if app_data.decode("utf-8") == "on" and module_state != "KO":
				print("Sending", app_data.decode("utf-8"), "to module")
				module_conn.send(bytearray("on", "utf8"))
				module_state = 'on'

			elif app_data.decode("utf-8") == "off" and module_state != "KO":
				module_conn.send(bytearray("off", "utf8"))
				print("Sending", app_data.decode("utf-8"), "to module")
				module_state = 'off'

			elif app_data.decode("utf-8") == "cosas de config":
				print("Cosas de config")
				# aqui hacer el procesado de los datos!!
			else:
				print("Rubish data from app")
				break

'''