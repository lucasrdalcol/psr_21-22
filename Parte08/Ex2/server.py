#!/usr/bin/env python
# --------------------------------------------------
# Miguel Riem Oliveira.
# PARI, September 2020.
# Adapted from https://stackabuse.com/basic-socket-programming-in-python/
# --------------------------------------------------
import socket
import dog_lib

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create TCP/IP socket
local_hostname = socket.gethostname()  # retrieve local hostname
local_fqdn = socket.getfqdn()  # get fully qualified hostname
ip_address = socket.gethostbyname(local_hostname)  # get the according IP address

# output hostname, domain name and IP address
print ("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))
server_address = (ip_address, 23457)  # bind the socket to the port 23456

print ('starting up on %s port %s' % server_address)
sock.bind(server_address)

# listen for incoming connections (server mode) with one connection at a time
sock.listen(1)

while True:
    print ('waiting for a connection')
    connection, client_address = sock.accept()  # wait for a connection

    try:  # show who connected to us
        print ('connection from', client_address)

        while True:  # receive the data in small chunks (64 bytes) and print it
            data = connection.recv(64)

            if data:
                print ("Data: %s" % data) # output received data
                # Deserialization
                print('data = ' + data)
                data_list = data.split(',')
                print('data_list = ' + str(data_list))

                name = data_list[0]
                age = data_list[1]
                color = data_list[2]

                # create an instance of class dog
                dog = dog_lib.Dog(name=name, age=age, color=color)

                # add brothers
                for element in data_list[3:]:
                    print('Adding brother ' + str(element))
                    dog.addBrother(element)

                print("Received a dog: " + str(dog))

            else:
                print ("no more data.") # no more data -- quit the loop
                break
    finally:
        # Clean up the connection
        connection.close()