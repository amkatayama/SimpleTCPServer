#Program 2 - server.py
# This implements the server of a simple chat room
# Author: Arata Katayama
#
import socket
import sys
import threading

# global variable containing a list of established connections
clientList = []

#class to service one client
class serverThread ( threading.Thread ):
    def __init__(self, connection, clientAddress, userHandle, clientList): # define a constructor with appropriate parameters
        threading.Thread.__init__( self )
        # initialize other appropriate instance fields
        self.connection = connection
        self.clientAddress = clientAddress
        self.userHandle = userHandle
        self.clientList = clientList

    def run( self ):
        # send message to everyone letting them know that we're in the room
        print('connection from {}'.format(self.clientAddress))

        for s in self.clientList:
            if s != self.connection:
                s.sendall("{} has entered the chat room".format(self.userHandle).encode())

        while True:
            # read a message from the client
            data = self.connection.recv(2048)
            message = data.decode()

            if message == ".":
                # close the connection
                break
            if message[0] == ".":
                # remove the first character
                message = message[1:]
            # add the user's handle to the front of the message
            message = "{}: ".format(self.userHandle) + message
            # send this message to all other clients
            for s in self.clientList:
                if s != self.connection:
                    s.sendall(message.encode())

        # send message to all other clients letting them know this user is leaving the chat room
        for s in self.clientList:
            if s != self.connection:
                leftMessage = "{} has left the chat room".format(self.userHandle)
                s.sendall(leftMessage.encode())

        self.clientList.remove(self.connection)

        # close the TCP connection
        self.connection.close()


# main
if __name__ == "__main__":
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get command line arguments
    argc = len(sys.argv)
    if argc != 2:
        print ("usage: python3 server.py serverPort")
        sys.exit()
    port = int(sys.argv[1])

    # Bind the socket to the port
    serverAddress = ("", port)

    print ('starting up on {} port {}'.format(serverAddress[0], serverAddress[1]))
    sock.bind(serverAddress)

    # Listen for incoming connections
    sock.listen()

    #initialize any data structures

    while True:
        # Wait for a connection
        print("waiting for connection")
        connection, client_address = sock.accept()

        # read the first message from the client, which will be the user's handle
        userHandle = connection.recv(2048).decode()

        # add this client to any data structures
        clientList.append(connection)

        # create a thread to handle this client and start that thread
        thread = serverThread(connection, client_address, userHandle, clientList) # You'll have to pass whatever parameters you defined in your constructor
        thread.start()
