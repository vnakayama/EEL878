#!/usr/bin/env python3

import socket
import sys

if len(sys.argv) !=3:
    print("Error: wrong number of arguments. Requires 3: client.py <hostname> <filename>")

PORT = 5923

HOST = sys.argv[1]

FILENAME = sys.argv[2]

SOCKET = socket(AF_INET, SOCK_STREAM)

# Connect to server 
try:
    SOCKET.connect((HOST, PORT))
    print("Connected.")
except:
    print("Couldn't establish connection with server. Try again in a moment.")
    SOCKET.close()

# Send the HTTP request
REQUEST = "GET /" + filename + " HTTP/1.1\r\n\r\n"
try: 
    SOCKET.send(REQUEST.encode())
    print("Request message sent.")
except:
    print("Couldn't send request. Try again in a moment.")

# Recieve server HTTP response
RESPONSE = ""
while True:
    SOCKET.settimeout(5)
    RESPONSE += SOCKET.recv(1024).decode()
    if (len(SOCKET.recv(1024).decode()) == 0):
        break

print("Server HTTP Response:\r\n\n" + RESPONSE)

# Close connection to server
print("Closing connection. Bye!")
SOCKET.close()

