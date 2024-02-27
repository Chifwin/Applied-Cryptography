
def encrypt(from_path, pubkey_path, to_path):
    fp = open(from_path, 'rb')
    plaintext = fp.read()
    fp.close()

    pubkey_f = open(pubkey_path, 'r')
    pub = pubkey_f.read().split(", ")
    pubkey_f.close()

    e = int(pub[0])
    n = int(pub[1])
    message_encoded = [ch for ch in plaintext]
    ciphertext = [pow(ch, e, n) for ch in message_encoded]

    tp = open(to_path, 'w')
    tp.write(str(ciphertext))
    tp.close()
    return ciphertext

def decrypt(from_path, privkey_path, to_path):
    fp = open(from_path, 'r')
    ciphertext = [eval(i) for i in fp.read()[1:-1].split(", ")]
    fp.close()

    privkey_f = open(privkey_path, 'r')
    priv = privkey_f.read().split(", ")
    privkey_f.close()

    n = int(priv[0])
    d = int(priv[1])
    message_encoded = [pow(ch, d, n) for ch in ciphertext]
    message = bytes(message_encoded)
    #message ="".join(chr(ch) for ch in message_encoded)
    tp = open(to_path, 'wb')
    tp.write(message)
    tp.close()
    return message

