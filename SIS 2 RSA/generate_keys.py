import random, math, sympy


def generate_prime(min_values, max_values):
    prime = random.randint(min_values, max_values)
    while not sympy.isprime(prime):
        prime = random.randint(min_values, max_values)
    return prime


def compute_d(a, b):
    """
    Performs the extended Euclidean algorithm
    Returns the gcd, coefficient of a, and coefficient of b
    """
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = compute_d(b % a, a)
        return gcd, y - (b // a) * x, x


def chooseE(totient):
    """
    Chooses a random number, 1 < e < totient, and checks whether or not it is 
    coprime with the totient, that is, gcd(e, totient) = 1
    """
    while (True):
        e = random.randrange(2, totient)

        if (math.gcd(e, totient) == 1):
            return e


def generate_keys():
    """
    Using the prime numbers compute and store 
    the public and private keys in two separate 
    files.
    """

    # choose two random prime numbers 
    prime1, prime2 = generate_prime(1000, 5000), generate_prime(1000, 5000)
    while prime1 == prime2:
        prime2 = generate_prime(1000, 5000)

    # compute n, totient, e
    n = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    e = chooseE(totient)

    # compute d, 1 < d < totient such that e*d = 1 (mod totient)
    # e and d are inverses (mod totient)
    gcd, x, y = compute_d(e, totient)

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