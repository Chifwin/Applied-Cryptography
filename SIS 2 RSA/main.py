from rsa import encrypt, decrypt
from generate_keys import generate_keys

choise = input("What do you want? (enc/dec/gen) ")
if choise == "gen":
    print("...Generating...")
    e, n, d = generate_keys(512, 1024)
    # write the public keys n and e to a file
    pubkey = str(e) + ", " + str(n)
    pubkey_f = open('public.key', 'w')
    pubkey_f.write(pubkey)
    pubkey_f.close()

    privkey = str(n) + ", " + str(d)
    privkey_f = open('private.key', 'w')
    privkey_f.write(privkey)
    privkey_f.close()   
    print("Done!")
elif choise == "enc":
    from_path = input("Enter the path to the file to encrypt: ")
    pubkey_path = input("Enter the path to key file: ")
    to_path = input("Enter the path to the file to save: ")
    print("...Encrypting...")
    encrypt(from_path, pubkey_path, to_path)
    print("Done!")
elif choise == "dec":
    from_path = input("Enter the path to encrypted file: ")
    privkey_path = input("Enter the path to key file: ")
    to_path = input("Enter the path to the file to save: ")
    print("...Decrypting...")
    decrypt(from_path, privkey_path, to_path)
    print("Done!")
else:
    print("!!!!Incorrect Input!!!!")

