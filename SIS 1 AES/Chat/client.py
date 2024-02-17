from AES_lib import *

class Client:
    def __init__(self, key, sock):
        '''
            Create key and save socket for connection
        '''
        self.key = key
        self.aes = AES128(key)
        self.sock = sock
    
    def set_nickname(self, name):
        self.nick = name

    def encrypt(self, text: str):
        '''
            Encrypt string, using key of client. Lenght of the message is placed before chifertext
        '''
        sb = bytes(text, 'utf-8')
        return self.aes.encrypt(sb)
    
    def decrypt(self, sb: bytes):
        '''
            Decrypt bytes, using key of client, and getting lenght from start of the message
        '''
        return str(self.aes.decrypt(sb), 'utf-8')
    
    def send(self, text):
        '''
            Send to socket encypted message
        '''
        self.sock.send(self.encrypt(text))

    def recv(self):
        '''
            Wait for message from socket and decrypt it
        '''
        return self.decrypt(self.sock.recv(1024))
   
    def close(self):
        self.sock.close()

    def key_exchange(self):
        self.sock.send(bytes(i for i in self.key))

    @staticmethod
    def get_key(sock):
        '''
            Return key from recieved bytes
        '''
        key = sock.recv(1024)
        return gen_key([*key])