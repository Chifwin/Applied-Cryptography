import sys
import time
import socket
import threading

from AES_lib import *

# Choosing Nickname
nickname = input("Choose your nickname: ")

stop = False

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))


# Listening to Server and Sending Nickname
def receive():
    # while not stop:
    while not stop:
        try:
            # Receive Message From Server
            message = client.recv(1024)

            # If message is 'NICK', then  send Nickname
            if message.decode('utf-8') == 'NICK': 
                global key
                key = client.recv(1024).from_bytes()
                global aes
                aes = AES128(key)
                pre_message = len(nickname).to_bytes(64, 'little') + bytes(nickname, 'utf-8')
                client.send(aes.encrypt(pre_message))
            else:
                # Decoding  a message
                message = aes.decrypt(message[64:], int.from_bytes(message[:64], 'little')).decode()
                print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while not stop:
        message = '{}: {}'.format(nickname, input(''))
        pre_message = len(message).to_bytes(64, 'little') + bytes(message, 'utf-8')
        client.send(aes.encrypt(pre_message))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("quitting")
    stop = True
    sys.exit()
    


# int.from_bytes(g[:64], 'little')
# g = len(s).to_bytes(64, 'little') + bytes(s, 'utf-8')
# aes.decrypt(g[64:], int.from_bytes(g[:64], 'little'))

