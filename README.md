# Reverse Shell

Way to connect to someone's computer from anywhere in the world

Why using this:
- Ip addresses are not public and dynamic and always changing
- Even if same network, and know ipaddress there are firewall, port forwarding issues etc
So cant ssh into someone's home computer like a web server all the time.

Can set up own server and make target connect to us.

In short, shell for any computer.

Hackers can use and make others click on it through cd, usb etc.

Note: Right now, scripts can be run in background without showing output message using "nohup whateverCommand". Do not run scripts using & as using trailing characters ".sh" as a lazy way to know its a script. Will later fix this maybe.

How to use:

## Server
Change host variable in server.py to server machine's private IP Address. Then run command on server:
``` python server.py ```

## Client
Change host variable in client.py to server machine's public IP Address. Then run command on target machine:
``` python client.py ```


Resources:

- Basic python socket programming: https://www.tutorialspoint.com/python/python_networking.htm

- Send and receive large messages:
http://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data

- Tutorial help: https://www.youtube.com/playlist?list=PL6gx4Cwl9DGCbpkBEMiCaiu_3OL-_Bz_8

- Make standalone exeutables: http://www.pyinstaller.org/