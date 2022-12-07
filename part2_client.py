# Group#: G12
# Student Names: Cullen Jamieson, Sanskar Soni

import time
from socket import *

serverName = '127.0.0.1'                     #or 'localhost'
serverPort = 12000                           #use an available port
clientSocket = socket(AF_INET, SOCK_DGRAM)   #create client socket

for i in range(5):     #5 messages in total

    message = f"PING {i} - hello world"
    clientSocket.sendto(message.encode(), (serverName, serverPort))   #send message to server

    sendTime = time.time()     #sendTime is the time at which message is sent to server
    clientSocket.settimeout(1) # Set the maximum delay to be 1 second

    try:      #try recieving the message from the server in under a second
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)  #message from server recieved
        receiveTime = time.time()                                     #time at which message is recieved recorded

        RTT = 1000 * round(receiveTime - sendTime, 3)     #calculate round trip time in seconds (round to 3 decimals) and convert to ms finally
        print(f'{RTT} ms')                                #print RTT in ms
        print(modifiedMessage.decode())                   #print message recieved from server

    except timeout:     #message was not recieved from server in under a second
        print('request timed out')
            
clientSocket.close()     #close the client socket