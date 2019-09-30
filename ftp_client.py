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

def handle_retrieve(sock, cmd):
    rfile = cmd[9:] #parse file name
    sock.sendall(cmd.encode("UTF-8"))
    data = sock.recv(1024)
    try:
        f = open(rfile, "w")
    except:
        print("error opening file")
        return 0
    f.write(data.decode())
    f.flush()
    while True:
        data = sock.recv(1024)
        f.write(data.decode())
        f.flush()

        #if less than 1024 nothing more to receive
        if len(data) < 1024:
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
        while True:
            data = sock.recv(1024)
            print(data)
            if len(data) < 1024:
                break

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
