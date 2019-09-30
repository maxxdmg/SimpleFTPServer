# Group members: Aaron, Camaal, Kelly, Max
# version 1.0 9-21-2019
# CS 457 Data Communications
#Prof. Bhuse
#Files: ftp_server
# Purpose: to have a multi-threaded server receive and process commands from clients with further details below.
# On receiving a command, the server should parse the command and perform the appropriate action. The format of the commands is such as follows:

# 1.	CONNECT <server name/IP address> <server port>: This command allows a client to connect to a server.
# The arguments are the IP address of the server and the port number on which the server is listening for connections.

# 2.	LIST: When this command is sent to the server, the server returns a list of the files in the current directory on which it is executing.
# The client should get the list and display it on the screen.

# 3.	RETRIEVE <filename>: This command allows a client to get a file specified by its filename from the server.

# 4.	STORE <filename>: This command allows a client to send a file specified by its filename to the server.

# 5.	QUIT: This command allows a client to terminate the control connection.
# On receiving this command, the client should send it to the server and terminate the connection.
# When the ftp_server receives the quit command it should close its end of the connection.


import socket
import os
import sys
import select
from _thread import *

# intialize and run everything


def main(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
    print("Socket Created")  # Status update

    # Attempt to bind socket to IP and port, error otherwise.
    try:
        s.bind((host, int(port)))
    except socket.error:
        print("Binding failed")
        sys.exit()
    print("socket bound")  # Status update

    s.setblocking(0)  # for exiting server on windows
    s.listen()
    print("listening")  # Status update

    # driver loop
    while 1:
        # see if kill process occured
        try:
            # handle windows kill command, ctrl+c
            ready = select.select((s,), (), (), 0.5)
        except KeyboardInterrupt:
            # kill process message
            print("Keyboard interrupt occured, closing...")
            break

        # no process kill occurred
        if (ready[0]):
            try:
                conn, addr = s.accept()  # continuously accept client connections
                # Print IP address and port# of connected client
                print("Connected with " + addr[0] + ":" + str(addr[1]))
                # Start new thread for client each connection
                start_new_thread(clientthread, (conn,))
            except socket.error:
                print("ignoring socket error")
                continue
            if conn:
                s.close()
                break  # after every connection, reset ready so that the process can be killed
    s.close()  # Close socket


def retrieve(filename):
    print(filename)

    try:
        file = open(filename, 'rb')  # open file to read bytes
        s = file.read(1024)
    except:
        print("error opening file")
        return

    while(s):
        conn.send(s)  # send initial read
        print('Sent ', repr(s))  # confirm data print to screen
        s = file.read(1024)  # continue to read
    file.close()  # close file after sending all

    print(filename + " sent")  # print file name that's sent


# Function to handle all client connections and their respective commands
def clientthread(conn):
    while True:
        data = conn.recv(1024)
        reply = "ACK " + data.decode()
        rdata = data.decode()
        rdata = rdata.lower()
        if not data:
            break
        print(reply)

        # Retrieve function
        if 'retrieve' in rdata:
            rfile = rdata[9:]  # parse file name
            print(rfile)  # confirms file name
            retrieve(rfile)

    # List function
    if rdata[0:4] == 'LIST' or rdata[0:4] == 'list':
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            print(f)
    # end LIST function

    # QUIT function
    if rdata[0:4] == 'QUIT' or rdata[0:4] == 'quit':
        conn.close()
    # End RETRIEVE function


    #conn.close() #


if len(sys.argv) != 3:
    print("Usage: python3 ftp_server.py ip_address port")
    exit()
else:
    # get host and port from cmd line args
    host = sys.argv[1]
    port = sys.argv[2]

    main(host, port) # run main w/ supplied values
