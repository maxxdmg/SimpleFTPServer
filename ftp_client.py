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
    #setup socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8000
    try:
       sock.connect((host, port))
    except:
       print("Connection Error")
       sys.exit()

    while True:
        print("Enter your command: QUIT to exit")
        #command to go to the server
        cmd = input()
        #process commands
        readcmd(cmd, sock)

def readcmd(rcmd, sock):
    cmd = rcmd #.upper()

    if cmd[0:5] == 'QUIT' or cmd[0:5] == 'quit':
        sock.sendall(cmd.encode("UTF-8")) #send quit to server
        time.sleep(1) #added because close operation timing issues
        sock.close() #close socket
        sys.exit() #exit 
            
    if cmd[0:8] == 'RETRIEVE' or cmd[0:8] == 'retrieve':
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

    return

if __name__ == "__main__":
   main()
