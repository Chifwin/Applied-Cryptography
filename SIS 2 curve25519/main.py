import os

def clamp_scalar(scalar):
    scalar &= 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffffffffffff

def montgomery_multiply(a, b):
    c = 0
    for i in range(255):
        if b & 1:
            c ^= a
        a <<= 1
        if a & 0x10000000000000000000000000000000000000000000000000000000000000000:
            a ^= 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffed
        b >>= 1
    return c

def curve25519_scalarmult(n, p):
    clamp_scalar(n)

    x1 = 1
    x2 = p
    z2 = 0
    x3 = 1
    z3 = 0
    swap = 0

    for i in reversed(range(255)):
        n_bit = (n >> i) & 1
        swap ^= n_bit
        x2, x3 = x3 ^ (swap & (x2 ^ x3)), x2 ^ (swap & (x2 ^ x3))
        z2, z3 = z3 ^ (swap & (z2 ^ z3)), z2 ^ (swap & (z2 ^ z3))
        swap = n_bit

        a = x2 + z2
        aa = a * a
        b = x2 - z2
        bb = b * b
        e = aa - bb
        c = x3 + z3
        d = x3 - z3
        da = d * a
        cb = c * b
        x3 = (da + cb) ** 2
        x3 = montgomery_multiply(x3, 0x9d372c9cfc3d950d535b45c6b9ebf2b1a72250dfdac5a49c8f0d586e7b9b74f9)
        z3 = x1 * ((da - cb) ** 2)
        z3 = montgomery_multiply(z3, 0x56b4d47005f66bb04c6646e5c7c36b1f3475f2224a7f604a0c56697b960b33b8)
        x1 = (aa * bb) ** 2
        aa = montgomery_multiply(aa, bb)

        bb = e * (aa - 121665)
        aa = aa + bb
        x1 = montgomery_multiply(x1, aa)
        aa = x2 * z2
        bb = da - cb
        x2 = (aa + aa) ** 2
        x2 = montgomery_multiply(x2, 0x0ea0a73664f44deab8d56a62f15b6f7932774484d137a8780c44c5d527d60d5c)
        z2 = bb ** 2
        z2 = montgomery_multiply(z2, x1)
    
    result = x2 * z2
    result = montgomery_multiply(result, 0x99108cc9edd5e5eb88122e9eae7747942fa1777b7d5d1b14878ed1f0a4d3a418)
    return result

def curve25519_key_exchange(private_key, public_key):
    shared_secret = curve25519_scalarmult(private_key, public_key)
    return shared_secret.to_bytes(32, byteorder='little')

# Example usage:
alice_private_key = int.from_bytes(b'\x01' + os.urandom(31), byteorder='little')  # 32-byte random private key
alice_public_key = curve25519_scalarmult(alice_private_key, 9)  # Base point multiplication

bob_private_key = int.from_bytes(b'\x01' + os.urandom(31), byteorder='little')
bob_public_key = curve25519_scalarmult(bob_private_key, 9)

alice_shared_secret = curve25519_key_exchange(alice_private_key, bob_public_key)
bob_shared_secret = curve25519_key_exchange(bob_private_key, alice_public_key)

print("Alice shared secret:", alice_shared_secret.hex())
print("Bob shared secret:", bob_shared_secret.hex())
