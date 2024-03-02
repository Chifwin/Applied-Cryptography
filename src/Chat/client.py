from AES_lib import *
from RSA import RSA

RSA_KEY_LEN = 512

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
        '''
            Recieve public key, encrypt AES key and send it
        '''
        n = int.from_bytes(self.sock.recv(RSA_KEY_LEN), "big")
        e = int.from_bytes(self.sock.recv(RSA_KEY_LEN), "big")
        byte_key = bytes(i for i in self.key)
        self.sock.send(RSA(n, e=e).encrypt(byte_key))

    @staticmethod
    def get_key(sock):
        '''
            Send public key, recieve encrypted AES key and decrypt it
        '''
        n, e, d = RSA.generate_key(RSA_KEY_LEN)
        sock.send(n.to_bytes(RSA_KEY_LEN, "big"))
        sock.send(e.to_bytes(RSA_KEY_LEN, "big"))
        key = RSA(n, e=e, d=d).decrypt(sock.recv(AES_KEY_LEN * RSA_KEY_LEN))
        return gen_key([*key])