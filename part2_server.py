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

from socket import *
from random import randint
from time import sleep
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

x=0
while x<5:
    message, clientAddress = serverSocket.recvfrom(2048)
    x += 1
    #random_delay = randint(5, 50)/1000
    sleep(randint(5, 50)/1000)
    random_probablity = randint(1,10)
    if random_probablity == 1:
        break
    else:
        modifiedMessage = f"Ping {x} - ditto"
        serverSocket.sendto(modifiedMessage.encode(),clientAddress) 
    