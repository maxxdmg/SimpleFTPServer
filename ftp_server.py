#Group members: Aaron, Camaal, Kelly, Max
#version 1.0 9-21-2019
#CS 457 Data Communications
#Prof. Bhuse
#Files: ftp_server
#Purpose: to have a multi-threaded server receive and process commands from clients with further details below.
#On receiving a command, the server should parse the command and perform the appropriate action. The format of the commands is such as follows:

#1.	CONNECT <server name/IP address> <server port>: This command allows a client to connect to a server.
# The arguments are the IP address of the server and the port number on which the server is listening for connections.

#2.	LIST: When this command is sent to the server, the server returns a list of the files in the current directory on which it is executing.
# The client should get the list and display it on the screen.

#3.	RETRIEVE <filename>: This command allows a client to get a file specified by its filename from the server.

#4.	STORE <filename>: This command allows a client to send a file specified by its filename to the server.

#5.	QUIT: This command allows a client to terminate the control connection.
# On receiving this command, the client should send it to the server and terminate the connection.
# When the ftp_server receives the quit command it should close its end of the connection.


import socket
import os
import sys
from _thread import *

#Host and port needs to be the same for ftp_client
host = '127.0.0.1'
port = 8000

#create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Socket Created") #Status update

#Attempt to bind socket to IP and port, error otherwise.
try:
	s.bind((host, port))
except socket.error:
	print("Binding failed");
	sys.exit();
	
print("socket bound") # Status update

s.listen();

print("listening") #Status update

#Function to handle all client connections and their respective commands
def clientthread(conn):

	while True:
		data = conn.recv(1024)
		reply = "ACK " + data.decode()
		rdata = data.decode()
		if not data:
			break;
		print(reply)
	#Retrieve function
		if rdata[0:8] == 'RETRIEVE':
			rfile = rdata[9:] #parse file name
			print(rfile) #confirms file name
			#try to open requested file error if not found
			try:
				file = open(rfile, 'rb') #open file to read bytes
			except:
				print("File Not Found.")
				traceback.print_exc()
				
			s = file.read(1024)
			
			while(s):
				conn.send(s) #send initial read
				print('Sent ', repr(s)) #confirm data print to screen
				s = file.read(1024) #continue to read
			file.close() #close file after sending all

			print(rfile + " sent") #print file name that's sent
    #End RETRIEVE function

	#conn.close() #

while 1:
	conn, addr = s.accept() #continuously accept client connections

    #Print IP address and port# of connected client
	print("Connected with " + addr[0] + ":" + str(addr[1]))

    #Start new thread for client each connection
	start_new_thread(clientthread, (conn,))

#Close socket
s.close()