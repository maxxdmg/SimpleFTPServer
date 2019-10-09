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
    # connection status
    connected = False
    
    # create placeholder for socket
    sock = None


    while True:
        print("Enter your command: HELP to see options or EXIT to exit\n")
        cmd = input() #command to go to the server
        # Handle the special case of connecting to the server separately
        if 'connect' in cmd and connected == False:
            sock = connect_server(cmd)
            if sock is not None:
                connected = True
        elif 'connect' in cmd and connected == True:
            print("Must disconnect first\n")
        else:
            connected = readcmd(cmd, sock, connected) #process other commands

def connect_server(cmd):
    # retrieve host and port number from the command
    host = cmd.split()[1]
    port = cmd.split()[2]
    
    # create TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # connect to the server
    try:
        sock.connect((host, int(port)))
        print("Connected")
        return sock
    except:
        print("Connection Error")
        return None
    
def handle_quit(sock, cmd):
        sock.sendall(cmd.encode("UTF-8")) #send quit to server
        time.sleep(1) #added because close operation timing issues
        sock.close() #close socket
        print("Connection terminated\n")
        #sys.exit() #exit 
'''
def handle_retrieve(sock, cmd):
    rfile = cmd[9:] #parse file name
    sock.sendall(cmd.encode("UTF-8"))
    try:
        f = open(rfile, "w")
    except:
        print("error opening file")
        return 0

    while True:
        data = sock.recv(128)

        # handle empty file
        if data.decode() == "$nil$":
            break

        print(data)

        f.write(data.decode())
        f.flush()

        #if less than 1024 nothing more to receive
        if len(data) < 128:
            break
    f.close()
    print('Successfully received the file')
'''

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
        print('data=%s', (data.decode()))
        f.write(data.decode())
        f.flush()

        #Indicates last of data was received
        if len(data) < chunk_size:
            f.close()
            break

    f.close()
    print('Successfully received the file')



def handle_help():
    print("QUIT: to quit\nRETRIEVE: to retrieve files\n")

def readcmd(rcmd, sock, connected):
    cmd = rcmd.lower() #.upper()

    # handle help - connection independent
    if 'help' in cmd:
        handle_help()
    
    # handle exit - must be disconnected
    elif 'exit' in cmd:
        if connected:
            print("Must be disconnected\n")
        else:
            print("Exiting...")
            exit()
    
    # handle quit - must be connected
    elif 'quit' in cmd:
        if not connected:
            print("Must be connected\n")
        else:
            handle_quit(sock, cmd)
            return False
    
    # handle retrieve - must be connected
    elif 'retrieve' in cmd:
        if not connected:
            print("Must be connected\n")
        else:
            handle_retrieve(sock, cmd)

    # handle store - must be connected
    elif 'store' in cmd:
        if not connected:
            print("Must be connected\n")
        else:
            handle_store(sock, cmd)

    # handle list - must be connected
    elif 'list' in cmd:
        if not connected:
            print("Must be connected\n")
        else:
            sock.sendall(cmd.encode("UTF-8"))
            data = sock.recv(1024)
            print(data)

    else:
        print("invalid command\n")
        
    return connected

if __name__ == "__main__":
    main()
    '''
    if len(sys.argv) != 3:
        print("Usage: python3 ftp_client.py ip_address port")
        exit()
    else:
    # get host and port from cmd line args
        host = sys.argv[1]
        port = sys.argv[2]

        main(host, port) # run main w/ supplied values
    '''
