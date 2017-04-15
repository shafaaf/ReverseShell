# 
# https://www.tutorialspoint.com/python/python_networking.htm

import socket
import sys

#------------------------------------------------------------------------------

# Setup socket (allows computers to connect)
def socketSetup():
	global host
	global port
	global s
	
	try:		
		s = socket.socket() # Create a socket object	
		host = socket.gethostname() # Get local machine name
		port = 8080
		print "socketSetup: host is: {} and port is: {}".format(host, port)

		s.bind((host, port)) # Bind to the port
		s.listen(5)  # 5 is bad connections it can take before refusing any new connections
		print "Server waiting for connections on port: {}...".format(port)
		
		# Accept incoming connections
		while True:
		   conn, address = s.accept()     # Blocking. Establish connection with client.
		   print 'Got a connection from', address
		   sendCommands(conn)
		   conn.close() # Close the connection

	except socket.error as message:
		print "socket error: {}".format(message)

#------------------------------------------------------------------------------

def sendCommands(conn):
	while True:
		print "Enter command: "
		cmd = raw_input()
		print "cmd entered in is: {}".format(cmd)
		if cmd == 'quit':
			print "Quitting connection ..."
			conn.close()
			s.close()
			sys.exit()

		if len(str.encode(cmd)) > 0: #only send if actually data there
			conn.send(str.encode(cmd))
			# Response in bytes, then convert for chartacter encodnig to see as normal string
			#1024 is buffer size
			#clientResponse = str(conn.recv(1024), "utf-8") 
			#print (clientResponse, end = "") # To resemble command line	
			#print clientResponse
			# Todo: the end thing here

#------------------------------------------------------------------------------

# Example program
if __name__ == "__main__":
	socketSetup()
	#print "host is: {} and port is: {}".format(host, port)
