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
	print "will get current directory now"
	currentClientPath = conn.recv(1024)
	print "currentClientPath is: {}".format(currentClientPath)
	
	# Will send commands from this point on.
	print "Enter commands from now on: "
	while True:
		print currentClientPath + ":",
		cmd = raw_input()
		print "cmd entered in is: {}".format(cmd)
		if cmd == 'quit':
			print "Quitting connection ..."
			conn.close()
			s.close()
			sys.exit()

		if len(cmd) > 0: #only send if actually data there
			conn.send(cmd)
		else:
			print "No command entered."

#------------------------------------------------------------------------------

# Example program
if __name__ == "__main__":
	socketSetup()
	#print "host is: {} and port is: {}".format(host, port)
