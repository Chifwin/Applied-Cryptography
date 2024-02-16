import socket
import threading

from AES_lib import *

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = {}
nicknames = []

def gen_key_for_client():
    return AES128(gen_key())

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        aes = AES128(clients[client])
        pre_message = len(message).to_bytes(64, 'little') + bytes(message, 'utf-8')
        client.send(aes.encrypt(pre_message))

# Handling Messages From encrypt
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            aes = AES128(clients[client])
            message = aes.decrypt(message[64:], int.from_bytes(message[:64], 'little')).decode()
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.keys().index(client)
            clients.pop(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname))
            nicknames.remove(nickname)
            break


# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        key_of_client = gen_key_for_client()
        client.send(key_of_client.to_bytes())

        #    !!!  check if there exists user with that name
        nickname = client.recv(1024)
        aes_client = AES128(key_of_client)
        nickname = aes_client.decrypt(nickname[64:], int.from_bytes(nickname[:64], 'little')).decode()

        nicknames.append(nickname)
        clients[client] = key_of_client

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname))
        pre_message = len('Connected to server!').to_bytes(64, 'little') + bytes('Connected to server!', 'utf-8')
        client.send(aes_client.encrypt(pre_message))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()