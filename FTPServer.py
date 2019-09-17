import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #initialize socket
port = 1010 #set port
s.bind((''), port) #bind port
s.listen(5) #socket begins listening

while 1:
	c, addr = s.accept(); #establish connection w/ client
	print 'Connection from ', addr
	
	c.send('Connection successful!') #send stuff to client
	c.close() #close connection