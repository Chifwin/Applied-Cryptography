import random, math, sympy

class RSA:
    def __init__(self):
        pass

    def generate_prime(self, min_values, max_values):
        prime = random.randint(min_values, max_values)
        while not sympy.isprime(prime):
            prime = random.randint(min_values, max_values)
        return prime


    def compute_d(self, a, b):
        """
        Performs the extended Euclidean algorithm
        Returns the gcd, coefficient of a, and coefficient of b
        """
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.compute_d(b % a, a)
            return gcd, y - (b // a) * x, x


    def chooseE(self, totient):
        """
        Chooses a random number, 1 < e < totient, and checks whether or not it is 
        coprime with the totient, that is, gcd(e, totient) = 1
        """
        while (True):
            e = random.randrange(2, totient)

            if (math.gcd(e, totient) == 1):
                return e


    def generate_keys(self):
        """
        Using the prime numbers compute and store 
        the public and private keys in two separate 
        files.
        """
        # choose two random prime numbers 
        prime1, prime2 = self.generate_prime(1000, 5000), self.generate_prime(1000, 5000)
        while prime1 == prime2:
            prime2 = self.generate_prime(1000, 5000)

        # compute n, totient, e
        n = prime1 * prime2
        totient = (prime1 - 1) * (prime2 - 1)
        e = self.chooseE(totient)

        # compute d, 1 < d < totient such that e*d = 1 (mod totient)
        # e and d are inverses (mod totient)
        gcd, x, y = self.compute_d(e, totient)

        # make sure d is positive
        if (x < 0):
            d = x + totient
        else:
            d = x

        # write the public keys n and e to a file
        pubkey = str(e) + ", " + str(n)
        pubkey_f = open('public.key', 'w')
        pubkey_f.write(pubkey)
        pubkey_f.close()

        privkey = str(n) + ", " + str(d)
        privkey_f = open('private.key', 'w')
        privkey_f.write(privkey)
        privkey_f.close()    

        
    def encrypt(self, from_path, pubkey_path, to_path):
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

    def decrypt(self, from_path, privkey_path, to_path):
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

    def main(self):
        choise = input("What do you want? (enc/dec/gen) ")
        if choise == "gen":
            print("...Generating...")
            self.generate_keys()
            print("Done!")
        elif choise == "enc":
            from_path = input("Enter the path to the file to encrypt: ")
            pubkey_path = input("Enter the path to key file: ")
            to_path = input("Enter the path to the file to save: ")
            print("...Encrypting...")
            self.encrypt(from_path, pubkey_path, to_path)
            print("Done!")
        elif choise == "dec":
            from_path = input("Enter the path to encrypted file: ")
            privkey_path = input("Enter the path to key file: ")
            to_path = input("Enter the path to the file to save: ")
            print("...Decrypting...")
            self.decrypt(from_path, privkey_path, to_path)
            print("Done!")
        else:
            print("!!!!Incorrect Input!!!!")

# Create an instance of the DSA class and call the main method
dsa_instance = RSA()
dsa_instance.main()
