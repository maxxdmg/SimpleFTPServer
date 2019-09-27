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

def main():
    #Create TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #host = "127.0.0.1"
    #port = 8000
    #try:
    #   sock.connect((host, port))
    #except:
    #   print("Connection Error")
    #   sys.exit()

    while True:
        print("Enter your command: HELP to see options or QUIT to exit")
        cmd = input() #command to go to the server
        readcmd(cmd, sock) #process commands

def handle_quit():
        sock.sendall(cmd.encode("UTF-8")) #send quit to server
        time.sleep(1) #added because close operation timing issues
        sock.close() #close socket
        sys.exit() #exit 

def handle_retrieve():
    rfile = cmd[9:] #parse file name
    sock.sendall(cmd.encode("UTF-8"))
    data = sock.recv(1024)
    f = open(rfile, "w")
    f.write(data.decode())
    f.flush()
    while True:
        data = sock.recv(1024)
        if not data: break
        print('data=%s', (data))
        f.write(data.decode())
        f.flush()

        #if less than 1024 nothing more to receive
        if len(data) < 1024:
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
        handle_quit()
    
    # handle retrieve
    if 'retreieve' in cmd:
        handle_retrieve() 

    # handle connection
    if 'connection' in cmd:
        cmdlist = cmd.split(" ", 3)
        ip = cmdlist[1]
        port = cmdlist[2]

        try:
            sock.connect((ip, int(port)))
        except:
            print("Connection Error")
            sys.exit()
        finally:
            print("Connection established\n")

        #f.close()
        #print('Successfully received the file')

    return

if __name__ == "__main__":
   main()
