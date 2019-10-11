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
import time
import os
import sys
import select
from _thread import *

# intialize and run everything


def main():
    print("To begin listening, enter: CONNECT address port")
    s = -1
    host = -1
    port = -1
    while(1):
        cmd = input()
        inputs = cmd.split()
        
        if len(inputs) < 3 or inputs[0] != "CONNECT":
            print("Incorrect input, enter: CONNECT address port")
            continue

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create socket
        host = inputs[1]
        port = inputs[2]
        print("Socket Created")  # Status update
        break

    # Attempt to bind socket to IP and port, error otherwise.
    try:
        s.bind((host, int(port)))
    except socket.error:
        print("Binding failed")
        sys.exit()
    print("socket bound")  # Status update

    s.listen()
    print("listening")  # Status update

    # driver loop
    while 1:
        try:
            conn, addr = s.accept()  # continuously accept client connections
            # Print IP address and port# of connected client
            print("Connected with " + addr[0] + ":" + str(addr[1]))
            # Start new thread for client each connection
            start_new_thread(clientthread, (conn, addr,)) #,s
        except socket.error:
            continue
        except KeyboardInterrupt:
            print("\nQuiting server...")
            break
    s.close()  # Close socket

'''
def retrieve(file, conn):
    filesize = 0;
    sizeread = 0;

    f = open(file, 'rb')  # open file to read bytes
    filesize = os.path.getsize(f.name)
    print(os.listdir())

    if int(filesize) == 0:
        conn.send(b'$nil$');
        f.close();
        return;       
    elif int(filesize) <= 1024:
        s = f.read(filesize);
        conn.send(s);
        f.close();
        print('Sent ' + file + '\n')  # confirm data print to screen
        return;


    while(sizeread < 1024):
        s = f.read(1024)  # continue to read
        sizeread += 1024;
        conn.send(s)  # send initial read
        print('Sending ' + file + '\n')  # confirm data print to screen
        if filesize - sizeread < 1024:
            conn.send(f.read(filesize - sizeread))
            break;
    f.close()  # close file after sending all
    return 1
'''
def store(file, conn):
    chunk_size = 1024 #arbitrary chunk size but needs to be sufficient for data transfers
    rfile = file #parse file name
    filesize = conn.recv(16) #represents the size of file requested
    
    print('File size received is: ', filesize.decode())
    f = open('copy of' + rfile, 'w') #Added to use file in same dir then run diff
    
    if filesize <= bytes(chunk_size):
        data = conn.recv(chunk_size)
        f.write(data.decode())
        f.flush()
        f.close()
        return
    
    while True:
        data = conn.recv(chunk_size)
        if not data: break
        #print('data=%s', (data.decode()))
        f.write(data.decode())
        f.flush()
        
        #Indicates last of data was received
        if len(data) < chunk_size:
            f.close()
            break

    f.close()
    print('Successfully received the file')


def retrieve(file, conn):
    #Size of data to send
    chunk_size = 1024
    #try to open the file
    try:
        rfile = open(file, 'rb') #open file passed

    except:
        print("File Not Found")

    #Get file size and send it to the client
    filesize = os.path.getsize(file)
    print('File size is: ', filesize)
    conn.send(bytes(str(filesize).encode()))
    time.sleep(1) #Added for thread timing

    #If file size is less than or equal to chunk_size we have all the data
    if int(filesize) <= chunk_size:
        s = rfile.read(chunk_size)
        conn.send(s)
        rfile.close()
        print('Successfully sent file')
        return

    #File is larger than chunk_size
    s = rfile.read(chunk_size)

    #While there is data to read in the file
    while s:
        conn.send(s) #send initial read
        print(s.decode()) #confirm data print to screen
        s = rfile.read(chunk_size) #continue to read
    rfile.close()
    print('Successfully sent file')


# Function to handle all client connections and their respective commands
def clientthread(conn, addr):
    while True:
        #print(conn)
        data = conn.recv(1024)
        reply = "ACK " + data.decode()
        rdata = data.decode()
        rdata = rdata.lower()
        #print(rdata)
        if not data:
            break
        #print(reply)

        # Retrieve function
        if 'retrieve' in rdata:
            rfile = rdata[9:]  # parse file name
            print(rfile)  # confirms file name
            retrieve(rfile, conn)

        # List function
        if 'list' in rdata:
            results = os.popen('ls').read().encode() #socket sends bytes needs to be encoded
            while (results):
                conn.send(results)  # send initial read
                if len(results) < 1024:
                    break
        # end LIST function
    
        #store function
        if 'store' in rdata:
            sfile = rdata[6: ] #find file name
            print("reading " + sfile)
            store(sfile, conn)

        # QUIT function
        if 'quit' in rdata:
            # print close mesaage
            print("Connection with " + addr[0] + ":" + str(addr[1]) + " closed")
            conn.close()
            break
        # End RETRIEVE function


main()