#!/usr/bin/env python3

from socket import *

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
    CONNECTION, addr = SOCKET.accept()
    print("Request accepted from (address, port): %s" % (addr,))

    try:
        # Receives the request message from the client
        MESSAGE =  CONNECTION.recv(4096)
        # Extract the path of the requested object from the message
        FILENAME = MESSAGE.split()[1]
        f = open(FILENAME[1:])
        # Store the entire content of the requested file
        RESPONSE = f.read()
        print("Requested file found. Sending response.")
        # Send the HTTP response header line to the connection socket
        CONNECTION.sendall("HTTP/1.1 200 OK\r\n\r\n".encode('utf-8'))

        # Send the content of the requested file to the connection socket
        for i in range(0, len(RESPONSE)):  
            CONNECTION.sendall(RESPONSE[i].encode('utf-8'))
        CONNECTION.sendall("\r\n".encode('utf-8'))

        # Close the client connection socket
        CONNECTION.close()
        SOCKET.close()
        break

    except IOError:
        # Send HTTP response message for file not found
        print("ERROR 404: Requested file not found.")
        CONNECTION.sendall("HTTP/1.1 404 Not Found\r\n\r\n".encode('utf-8'))
        CONNECTION.sendall("<html><head></head><body><h1> \
        404 Not Found</h1></body></html>\r\n".encode('utf-8'))
        # Close the client connection socket
        CONNECTION.close()
        SOCKET.close()
        break

