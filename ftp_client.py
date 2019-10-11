#Group members: Aaron, Camaal, Kelly, Max
#version 1.0 9-21-2019
#CS 457 Data Communications
#Prof. Bhuse
#Files: ftp_client
#Purpose: to have a client issue commands to a server until client terminates connection by sending 'QUIT'
#Tested with socket.txt file 7kb and file needs to be in the same directory as the server

import socket
import sys
import time
import os
from pathlib import Path


def main():
    sock = -1 # socket initialized as no connection
    print("Enter your command: HELP to see options or QUIT to exit")
    while True:
        cmd = input() #command to go to the server
        potential_socket = readcmd(cmd, sock) #read command and may return a socket
        if(potential_socket != 0):
            sock = potential_socket

def handle_connection(cmd):
    inputs = cmd.split() # splits command string into whitespace seperated text
    host = inputs[1]
    port = inputs[2]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # init socket
        # connect to server
    try:
        sock.connect((host, int(port)))
        print("Successfully connected")
    except:
        print("Connection Error, are you sure the server is running?")
        sys.exit()

    return sock


def handle_quit(sock, cmd):
    sock.sendall(cmd.encode("UTF-8")) #send quit to server
    time.sleep(1) #added because close operation timing issues
    sock.close() #close socket
    print("Connection terminated\n")


def handle_store(sock, cmd):
    
    sock.sendall(cmd.encode("UTF-8")) #send store to server
    file = cmd[6: ]
    
    #Size of data to send
    chunk_size = 1024
    #try to open the file
    try:
        rfile = open(file, 'rb') #open file passed
    
    except:
        print("File Not Found")
    
    #Get file size and send it to the server
    filesize = os.path.getsize(rfile.name)
    print('File size is: ', filesize)
    sock.send(bytes(str(filesize).encode()))
    time.sleep(1) #Added for thread timing

    #If file size is less than or equal to chunk_size we have all the data
    if int(filesize) <= chunk_size:
        s = rfile.read(chunk_size)
        sock.send(s)
        rfile.close()
        print('Successfully sent file')
        return
    
    #File is larger than chunk_size
    s = rfile.read(chunk_size)
    
    #While there is data to read in the file
    while s:
        sock.send(s) #send initial read
        print(s.decode()) #confirm data print to screen
        s = rfile.read(chunk_size) #continue to read
    rfile.close()
    print('Successfully sent file from client')


def handle_retrieve(sock, cmd):
    chunk_size = 1024 #arbitrary chunk size but needs to be sufficient for data transfers
    rfile = cmd[9:] #parse file name
    sock.sendall(cmd.encode('UTF-8')) #send file request to server
    filesize = sock.recv(16) #represents the size of file requested

    print('File size received is: ', filesize.decode())
    f = open('copy2-' + rfile, 'w') #Added to use file in same dir then run diff

    if filesize <= bytes(chunk_size):
        data = sock.recv(chunk_size)
        f.write(data.decode())
        f.flush()
        f.close()
        return

    while True:
        data = sock.recv(chunk_size)
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


def handle_help():
    print("connect address port: to connect to server\nquit: to quit\nretrieve: to retrieve files\nstore: to store files to server\nlist: to list the files on server\n")


def readcmd(rcmd, sock):
    cmd = rcmd.lower() #.upper()
    
    # handle connection
    if 'connect' in cmd:
        if sock != -1:
            print('Must be disconnected to connect to a server')
        else:
            return handle_connection(cmd) # returns socket to main

    # handle help
    elif 'help' in cmd:
        handle_help()
        return 0
    
    # handle exit
    elif 'exit' in cmd:
        if sock != -1:
            print('Must be disconnected before exiting program')
        else:
            print('Exiting...')
            exit()
  
    # handle quit
    elif 'quit' in cmd:
        # check that socket has been initialized
        if sock == -1:
            print('Must connect to server before issuing commands')
            print('Enter the help command for more details') 
        else:
            handle_quit(sock, cmd)
        return 0
    
    # handle retrieve
    elif 'retrieve' in cmd:
        # check that socket has been initialized
        if sock == -1:
            print('Must connect to server before issuing commands')
            print('Enter the help command for more details') 
        else:
            handle_retrieve(sock, cmd)
        return 0

    elif 'store' in cmd:
        # check that socket has been initialized
        if sock == -1:
            print('Must connect to server before issuing commands')
            print('Enter the help command for more details') 
        else:
            handle_store(sock, cmd)
        return 0

    # handle list
    if 'list' in cmd:
        # check that socket has been initialized
        if sock == -1:
            print('Must connect to server before issuing commands')
            print('Enter the help command for more details') 
        else:
            sock.sendall(cmd.encode("UTF-8"))
            data = sock.recv(1024).strip()
            print(data.decode())
        return 0
    
    else:
        print("Invalid command")
      
    return 0

if __name__ == "__main__":
    main()
