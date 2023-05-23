import socket
import itertools

# Variables for each city and the distances between them
cities = ['1', '2', '3', '4']
distances = {
    ('1', '2'): 10,
    ('1', '3'): 15,
    ('1', '4'): 20,
    ('2', '1'): 5,
    ('2', '3'): 10,
    ('2', '4'): 15,
    ('3', '1'): 20,
    ('3', '2'): 15,
    ('3', '4'): 10,
    ('4', '1'): 25,
    ('4', '2'): 20,
    ('4', '3'): 15,
}

# Function to calculate the total distance of a path
def calculate_distance(path):
    return sum(distances[(path[i-1], path[i])] for i in range(1, len(path)))

# Breadth-first search to solve TSP
def solve_tsp():
    # All possible paths (permutations of cities)
    paths = list(itertools.permutations(cities))

    # Find the path with the shortest distance
    shortest_path = min(paths, key=calculate_distance)

    return shortest_path, calculate_distance(shortest_path)

# Function to send message to another city
def send_message(city, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((city, 12345))  # Assuming all cities are listening on port 12345
        s.sendall(message.encode())

# Function to receive message from another city
def receive_message():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 12345))  # Bind to port 12345
        s.listen(1)  # Start listening for incoming connections

        conn, addr = s.accept()
        with conn:
            return conn.recv(1024).decode()

# Main function
def main():
    # Solve TSP
    path, distance = solve_tsp()

    # Send the result to all other cities
    for city in cities:
        send_message(city, f"Shortest path: {path}, total distance: {distance}")

    # Receive results from all other cities
    for city in cities:
        print(receive_message())

if __name__ == "__main__":
    main()
