#Program 2 - client.py
# This implements the client of a simple chat room
# Author: Arata Katayama

import socket
import sys
import threading

#class to listen for keyboard input
class keyboardThread ( threading.Thread ):
    def __init__(self, connection): # define the constructor with appropriate parameters
        threading.Thread.__init__( self )
        # initilize instance fields
        self.connection = connection

    def run( self ):
        while True:
            try:
                # get message from user using input
                message = input()
                # if first character is ".", add a second "." to the beginning
                if message[0] == ".":
                    message = "." + message
                # send the message to the server
                self.connection.sendall(message.encode())

            except:
                # ^d entered, so exit loop
                break

        # send a message consisting of "." to server
        self.connection.sendall(".".encode())

#class to listen for chat messages from the server
class chatThread ( threading.Thread ):
    def __init__(self, connection): #define the constructor with appropriate parameters
        threading.Thread.__init__( self )
         # initialize instance fields
        self.connection = connection

    def run( self ):
        while True:
            # get message from server
            data = self.connection.recv(2048)

            # if the message has at least one byte of data, print it out
            if len(data) >= 1:
                print ("{}".format(data.decode()))
            else:
                break

#main
if __name__ == "__main__":
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get command line arguments
    argc = len(sys.argv)
    if argc != 4:
        print ("usage: python3 client.py serverAddress serverPort userHandle")
        sys.exit()
    serverName = sys.argv[1]
    port = int(sys.argv[2])
    userHandle = sys.argv[3]

    # Connect the socket to the port where the server is listening
    server_address = (serverName,port)
    print ('connecting to {} port {}'.format(server_address[0], server_address[1]) )
    sock.connect(server_address)

    # send the user's handle to the server
    sock.sendall(userHandle.encode())

    #start threads to handle the communication
    kb = keyboardThread(sock) #pass parameters defined in the constructor
    kb.start()
    chat = chatThread (sock) # pass parameters defined in the constructor
    chat.start ()

    #wait for the threads to end, which indicates that the user has left the room
    kb.join()
    chat.join()

    # close the TCP connection
    sock.close()
