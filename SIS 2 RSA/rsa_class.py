import random, math, sympy

class RSA:
    def __init__(self):
        pass

    def generate_prime(self, min_values, max_values):
        prime1 = sympy.randprime(min_values, max_values)
        prime2 = sympy.randprime(min_values, max_values)
        while prime1 == prime2:
            prime2 = sympy.randprime(1000, 5000) # -
        return prime1, prime2

    def choose_e(self, p, q):
        phi_n = (p-1) * (q-1)
        e = random.randint(3, phi_n-1)
        while math.gcd(e, phi_n) != 1:
            e = random.randint(3, phi_n - 1)
        return e

    def mod_inverse(self, e, phi):
        for d in range(3, phi):
            if (d * e) % phi == 1:
                return d
        raise ValueError("mod_inverse does not exist") #algorithm evklida


    def generate_key(self):
        # print("Generating keys...")
        p, q = self.generate_prime(1000, 5000)
        n = p * q
        phi_n = (p-1) * (q-1)
        e = self.choose_e(p, q)
        d = self.mod_inverse(e, phi_n)
        # print("Done!")
        # save(e, n, d)

        return e, n, d
                    

    def encrypt(self, plaintext, e, n):
        message_encoded = [ch for ch in plaintext]
        ciphertext = [pow(ch, e, n) for ch in message_encoded]
        return ciphertext


    def decrypt(self, ciphertext, n, d):
        message_encoded = [pow(ch, d, n) for ch in ciphertext]
        message = bytes(message_encoded)
        return message


# Create an instance of the DSA class and call the main method
rsa = RSA()

def save(self, e, n, d):
    pubkey = str(e) + ", " + str(n)
    pubkey_f = open('public.key', 'w')
    pubkey_f.write(pubkey)
    pubkey_f.close()

    privkey = str(n) + ", " + str(d)
    privkey_f = open('private.key', 'w')
    privkey_f.write(privkey)
    privkey_f.close()

def main():
    choise = input("What do you want? (enc/dec/gen) ")
    if choise == "gen":
        print("...Generating...")
        
        e, n, d = rsa.generate_key() 
        save(e, n, d)
        # wtire here to save values
        print("Done!")

    elif choise == "enc":
        from_path = input("Enter the path to the file to encrypt: ")
        to_path = input("Enter the path to the file to save: ")
        try:
            fp = open(from_path, 'rb')
            plaintext = fp.read()
            fp.close()
        except:
            plaintext = from_path.encode()

        print("...Encrypting...")
        pubkey_f = open("public.key", 'r')
        pub = pubkey_f.read().split(", ")
        pubkey_f.close()

        e = int(pub[0])
        n = int(pub[1])
        ciphertext = rsa.encrypt(plaintext, e, n)
        # ciphertext = encrypt(plaintext, "public.key")

        tp = open(to_path, 'w')
        tp.write(str(ciphertext))
        tp.close()

        print("Done!")

    elif choise == "dec":
        from_path = input("Enter the path to encrypted file: ")
        to_path = input("Enter the path to the file to save: ")
        try:
            fp = open(from_path, 'r')
            ciphertext = [int(i) for i in fp.read()[1:-1].split(", ")]
            fp.close()
        except:
            ciphertext = [int(i) for i in from_path[1:-1].split(", ")]

        print("...Decrypting...")
        privkey_f = open("private.key", 'r')
        priv = privkey_f.read().split(", ")
        privkey_f.close()

        n = int(priv[0])
        d = int(priv[1])
        plaintext = rsa.decrypt(ciphertext, n, d)
        # plaintext = decrypt(ciphertext, "private.key")

        tp = open(to_path, 'wb')
        tp.write(plaintext)
        tp.close()

        print("Done!")

    else:
        print("!!!!Incorrect Input!!!!")

main()