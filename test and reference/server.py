import threading
import socket
import sys

# Get the host IP address
HOST = socket.gethostbyname(socket.gethostname())
# Alternatively, you can specify a specific IP address, e.g., '
# HOST = ''

# Function to find an available port
def find_available_port():
    # Create a socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to an available port in the range 49152 to 65535
    for port in range(49152, 65536):
        try:
            server.bind(('127.0.0.1', port))
            server.close()
            return port
        except OSError:
            pass

    # If no available port is found
    raise RuntimeError("No available ports in the range 49152 to 65535")

# Set the port number for the server
PORT = find_available_port()
# Create a server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(HOST, PORT)
clients = []
nicknames = []

# Broadcast message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle client connections and messages
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close
            nickname = nicknames[index]
            broadcast(f'{nickname} has left the game!'.encode('ascii'))
            nicknames.remove(nickname)
            break

# Function to gracefully close the server
def close_server():
    print("Closing server...")
    for client in clients:
        client.close()
    server.close()
    sys.exit(0)

# Receive connections from clients
def receive():
    try:
        while True:
            client, address = server.accept()
            print(f"Connected with {str(address)}")
            
            # How the Server Asks for Information (In this case nickname):
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            print(f'Nickname of the client is {nickname}!')
            broadcast(f'{nickname} joined the game!'.encode('ascii'))
            client.send('Connected to the server!'.encode('ascii'))
            
            if len(clients) == 2:
                for i in clients:
                    i.send('START'.encode('ascii'))
            
            # Start a new thread to handle client messages
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
    except KeyboardInterrupt:
        close_server()

# Example usage:
print(f"Found available port: {PORT}")
print("Server is listening! Press 'q' to exit...")
receive()
