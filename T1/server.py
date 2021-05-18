#!/usr/bin/env python3

import socket 

# Assign port value
PORT = 5923

# Create a TCP server socket
SOCKET = socket(AF_INET, SOCK_STREAM)

# Bind the socket to server address and server port
SOCKET.bind(("", PORT))

# Listen to at most 1 connection at a time
SOCKET.listen(1)

print("Ready to serve . . .")

while True:
    connectionSocket, addr = SOCKET.accept()
    print("Request accepted from (address, port): %s" % (addr,))

    try:
        # Receives the request message from the client
        message =  connectionSocket.recv(1024)
        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        filename = message.split()[1]
        # Because the extracted path of the HTTP request includes 
        # a character '\', we read the path from the second character 
        f = open(filename[1:])
        # Store the entire contenet of the requested file in a temporary buffer
        outputdata = f.read()
        print("Requested file found. Sending response.")
        # Send the HTTP response header line to the connection socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n")

        # Send the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):  
            connectionSocket.send(outputdata[i])
        connectionSocket.send("\r\n")

        # Close the client connection socket
        connectionSocket.close()

    except IOError:
        # Send HTTP response message for file not found
        print("ERROR 404: Requested file not found.")
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n")
        # Close the client connection socket
        connectionSocket.close()

    SOCKET.close()