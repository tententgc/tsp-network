import socket
import os

city_number = os.getenv('CITY_NUMBER')
port = os.getenv('PORT')

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# bind to the port
serversocket.bind(('0.0.0.0', int(port)))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket, addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))

    # Receive data from client
    data = clientsocket.recv(1024).decode('utf-8')
    print('Received ', data, ' from the client')

    # Process and send data back to client
    new_data = str(data) + str(city_number)
    print('Sending ', new_data, ' to the client')
    clientsocket.send(new_data.encode('utf-8'))

    clientsocket.close()
