import os
import socket
import time
from threading import Thread

# Assuming we have 4 cities with their 2D coordinates
CITIES = {
    '1': (1, 1),
    '2': (2, 2),
    '3': (3, 3),
    '4': (4, 4),
}

def compute_distance(city1, city2):
    return ((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)**0.5

def server_program(city_id):
    host = socket.gethostname()
    port = 5000 + int(city_id)  # Assign a unique port to each city based on its id

    server_socket = socket.socket()
    server_socket.bind((host, port))

    # Configure socket to accept connections
    server_socket.listen(2)
    conn, address = server_socket.accept()

    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        # Compute the distance to the received city and send it back
        received_city_id = data.strip()
        distance = compute_distance(CITIES[city_id], CITIES[received_city_id])
        conn.send(str(distance).encode())

    conn.close()


def client_program(city_id, target_city_id):
    host = socket.gethostname()
    port = 5000 + int(target_city_id)  # Use the target city's unique port

    client_socket = socket.socket()

    # Keep trying to connect until it succeeds
    while True:
        try:
            client_socket.connect((host, port))
            break
        except ConnectionRefusedError:
            print('Connection refused, retrying in 1 second...')
            time.sleep(1)

    # Send our city id to the target city
    client_socket.send(city_id.encode())

    # Receive the distance data from the target city
    data = client_socket.recv(1024).decode()
    print('Received data: ' + data)

    client_socket.close()

if __name__ == "__main__":
    my_city_id = os.getenv('CITY_ID')  # Fetch the city ID from environment variable

    # Start the server in a separate thread to listen for connections
    Thread(target=server_program, args=(my_city_id,)).start()

    # Connect to all other cities
    for other_city_id in CITIES:
        if other_city_id != my_city_id:
            client_program(my_city_id, other_city_id)
