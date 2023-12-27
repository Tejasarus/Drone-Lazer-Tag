import threading
import socket
# Get the host IP address
HOST = socket.gethostbyname(socket.gethostname())
# Alternatively, you can specify a specific IP address, e.g., '
# HOST = ''

# Set the port number for the server
PORT = 55555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(HOST,PORT)
clients = []
nicknames = []

def broadcast(message):
    for client in clients:
     client.send(message)

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

def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        
        #How the Server Asks for Information(In this case nickname):
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the game!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("Server is listening!...")
recieve()