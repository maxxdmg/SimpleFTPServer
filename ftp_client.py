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

def main(host, port):
    # create TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    try:
        sock.connect((host, int(port)))
    except:
        print("Connection Error")
        sys.exit()

    while True:
        print("Enter your command: HELP to see options or QUIT to exit")
        cmd = input() #command to go to the server
        readcmd(cmd, sock) #process commands

def handle_quit(sock, cmd):
        sock.sendall(cmd.encode("UTF-8")) #send quit to server
        time.sleep(1) #added because close operation timing issues
        sock.close() #close socket
        sys.exit() #exit 
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

def readcmd(rcmd, sock):
    cmd = rcmd.lower() #.upper()

    # handle help
    if 'help' in cmd:
        handle_help()

    # handle quit
    if 'quit' in cmd:
        handle_quit(sock, cmd)
    
    # handle retrieve
    if 'retrieve' in cmd:
        handle_retrieve(sock, cmd) 

    # handle list
    if 'list' in cmd:
        data = sock.recv(1024)
        print(data)

    return

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 ftp_client.py ip_address port")
        exit()
    else:
    # get host and port from cmd line args
        host = sys.argv[1]
        port = sys.argv[2]

        main(host, port) # run main w/ supplied values
