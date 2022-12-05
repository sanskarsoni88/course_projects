
"""
The actual communication between the two processes is very straightforward. 

The client sends a simple greeting message including the message number, for example “PING 1 - hello world”) to the server using UDP. 
    Second message would be for example “PING 2 - hello world”, etc.

The server listens on the UDP port 12000 and responds back by simply replacing the greeting with "ditto" and then sends back the message. 
    For example, in response to the above message, it echoes back "PING 1 - ditto").

The client then calculates the Round Trip Time (RTT) and prints out the RTT result, and the received message itself (since it has the message number). 
    RTT is a common measure of the delay, which is the delay from the time the client sent the ping message to the time it received the echoed response message.

The client then repeats the above 4 more times (that is, we send 5 ping messages and calculate the corresponding 5 RTT values). 
•    To simulate the variability of the RTT delay, the server program must wait for some randomly chosen time between 5 to 50 ms before responding back. 
•    To simulate packet loss (that is, the messages that are lost for any reason along the way in an actual IPC communication over the Internet), the server must ignore a message (i.e. not responding back) randomly with a probability of 10%. If the client does not hear back within 1 sec for a sent message, it must print a ‘request timed out’ message. 
•    You may begin by using the code provided in the slides as a starting template for the programs.

To implement variable delay and loss and calculating the delay, use the methods in the random module (to create random variables) and time module (for timing related functionalities) in Python.
"""

import random, time

from socket import *
serverName = "hostname"    #replace with actual name
serverPort = 12000               #use an available port
clientSocket = socket(AF_INET,  SOCK_DGRAM)

message = input("Input lowercase sentence:")
clientSocket.sendto(message.encode(), (serverName, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print (modifiedMessage.decode())
clientSocket.close()