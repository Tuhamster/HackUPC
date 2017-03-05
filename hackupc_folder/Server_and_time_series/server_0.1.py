#!/usr/bin/env python

from threading import Thread
from threading import Timer
from time import sleep
import socket
import sys
import errno
import scipy.io

import datetime

import time
import numpy as np
import time
from operator import itemgetter
from itertools import groupby

import urllib.parse
import urllib.request
import zlib
from io import StringIO
import pandas as pd

import subprocess

TCP_IP = '172.31.42.119'
#TCP_IP = '10.4.180.103'
TCP_PORT = 12345
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

global eix_temporal

eix_temporal = [0]*48

app_conn = None

global app_addr
app_addr = None

global module_conn
module_conn = None

global module_addr
module_addr = None

module_state = "KO"

def consecutive(data, stepsize=1):
	return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)
'''
eix_temporal[2] = 1
eix_temporal[3] = -1
eix_temporal[4] = 1
eix_temporal[5] = -1
eix_temporal[6] = 1

eix_temporal[35] = -1
eix_temporal[36] = 1
eix_temporal[37] = -1
eix_temporal[38] = 1
eix_temporal[39] = -1
eix_temporal[40] = 1
'''
# mode -> modo schedule (0) o modo eco (1)
# t1 -> tiempo de start if mode 0 o tiempo de carga if mode 
# t2 -> tiempo de fin if mode 0 o deadline if mode 1


def exec_get_data():
	yesterday = datetime.date.today() - datetime.timedelta(days=1)
	yesterday = yesterday.strftime('%Y%m%d')

	url = 'http://www.ree.es/sites/default/files/simel/demd/DEMD_'+yesterday+'.gz'

	print("Calling the script...")
	subprocess.call(['./get_data.sh' + " " + url], shell=True)

	subprocess.call ("./timeseries.r")

def process_petition(mode, t1, t2):

	global eix_temporal
	params = [t1, t2, mode]

	t_time = time.gmtime().tm_hour + 1
	if(params[2]) == 0:

		t_start = t1
		if t2 == 0:
			t_end = 24
		else:
			t_end = t2

		if(t_start<t_time):
			t_start = t_start+24
		if(t_start>t_end):
			t_end=t_end+24
		print("Time processed: now: ", t_time , " start: ", t_start, " end: ", t_end)
		eix_temporal[t_start-t_time] = 1
		eix_temporal[t_end-t_time] = -1


	if(params[2]) == 1:
		charge_time = params[0]
		charge_time_limit = params[1]
		if(charge_time_limit<t_time):
			charge_time_limit = charge_time_limit + 24
		if(charge_time_limit<t_time+charge_time):
			charge_time_limit = charge_time_limit 
		charge_time_limit = charge_time_limit-t_time
		print("Charging before", charge_time_limit, "hours")

		serie = np.loadtxt("forecast.txt")
		serie = serie[t_time:t_time+48]

		serie2 = serie[:charge_time_limit]
		print(serie2)
		charge_time_limit = charge_time_limit -t_time
		serie_sorted_indexes = np.argsort(serie2, axis=0)
		index_bons = serie_sorted_indexes[:charge_time]
		index_bons = np.sort(index_bons)
		ilist = index_bons.tolist()
		index_bons_grouped = consecutive(ilist)

		for aux in index_bons_grouped:
			eix_temporal[aux[0]] = 1
			eix_temporal[aux[-1]+1] = -1
	print(eix_temporal)

def timeout():
    global eix_temporal
    #print("Timeout executed")
    if(eix_temporal[0]==1):
        print("CHARGER ON")
        module_conn.send(bytearray("on", "utf8"))

    if(eix_temporal[0]==-1):
        print("CHARGER OFF")
        module_conn.send(bytearray("off", "utf8"))

    eix_temporal = np.roll(eix_temporal,-1)
    eix_temporal[-1] = 0
    print(eix_temporal)
    t = Timer(3, timeout)
    t.start()

def listening_server(arg):
	global module_conn
	global module_state
	global module_timer
	global app_conn

	while 1: 
		print("Listening in server")
		conn, addr = s.accept()
		print('Connection address:', addr)

		data = conn.recv(BUFFER_SIZE)
		data_string = data.decode("utf-8")
		print(data_string)

		if len(data_string.split("/")) > 1:
			
			app_conn = conn

			app_t = Thread(target = app_thread, args = (data_string, ))
			app_t.start()

		else:
			
			module_timer = Timer(1, timeout)
			module_timer.start()

			module_conn = conn

			module_state = data.decode("utf-8")

			print("Current state of the module:", data.decode("utf-8"))

			module_t = Thread(target = module_thread, args = (conn, ))
			module_t.start()

def app_thread(arg):
	print("**************   The client is connected		**************")

	print("Received from app:", str(arg))
	tokens = arg.split("/")

	global module_conn
	global module_state
	global app_conn

	if tokens[0] == "switch":

		print(tokens[1])

		if tokens[1] == "on" and module_state != "KO":
			print("Switching module on")
			module_conn.send(bytearray("on", "utf8"))
			module_state = 'on'

		elif tokens[1] == "off" and module_state != "KO":
			module_conn.send(bytearray("off", "utf8"))
			print("Switching module off")
			module_state = 'off'

		app_conn.send(bytearray("ACK\n", "utf8"))

	elif tokens[0] == "command":

		print(tokens[1])
		
		if tokens[1] == "sched":
			process_petition(0, int(tokens[2]), int(tokens[3]))

		elif tokens[1] == "eco":
			process_petition(1, int(tokens[2]), int(tokens[3]))

		app_conn.send(bytearray("ACK\n", "utf8"))
		
	elif tokens[0] == "init":
		print("Initial configuration sending state")
		app_conn.send(bytearray(module_state + "\n", "utf8"))
	
	else:
		print("Rubish data from app")


def module_thread(arg):
	print("**************   The module is connected		**************")
	try:
		while 1:
			sleep(5)
			module_conn.send(bytearray("keppalive", "utf8"))
	
	except socket.error as e:
		print("Module disconnected")
		module_state = 'KO'

#Connections

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

thread = Thread(target = listening_server, args = (s, ))
thread.start()


while 1:
	time.sleep(60*30)
	time_now = datetime.datetime.now().hour + 1
	print("Current hour:", time_now)

	# a la una de la mañana se tiene que descargar los datos y hacer unos calculos
	if time_now == 1:
		exec_get_data()

