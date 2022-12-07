# Group#: G12
# Student Names: Cullen Jamieson, Sanskar Soni

from socket import *
from random import randint
from time import sleep

serverPort = 12000                            #or 'localhost'
serverSocket = socket(AF_INET, SOCK_DGRAM)    #create server socket
serverSocket.bind(('', serverPort))           #bind server socket to 12000 port to communicate with client

x = 0         #x represents the number of messages revieved

while x < 5:  #total 5 messages to be recieved
    message, clientAddress = serverSocket.recvfrom(2048)      #recieve the message from client
    x += 1                                                    #increment x to represent which number message has recently been recieved

    sleep(randint(5, 50)/1000)                 #generate a random integer between 5 and 50 (both included). Divide that by 1000 and delay by that number (corresponds to 5 ms to 50 ms of delay)

    if randint(1,10) == 1:                     #generate a random integer between 1 to 10 (both included). 
        pass                                   #If this number is 1 (10% probablity), send no message.
    else:
        modifiedMessage = f"Ping {x} - ditto"  #else, this is the message to be sent to the client
        serverSocket.sendto(modifiedMessage.encode(),clientAddress)   #function to send the message to the client
    