import random, math, sympy


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


def generate_keys(min_value, max_value):
    """
    Using the prime numbers compute and store 
    the public and private keys in two separate 
    files.
    """

    # choose two random prime numbers 
    prime1, prime2 = sympy.randprime(min_value, max_value), sympy.randprime(min_value, max_value)
    while prime1 == prime2:
        prime2 = sympy.randprime(min_value, max_value)

    # compute n, totient, e
    n = prime1 * prime2
    totient = (prime1 * prime2) // math.gcd(prime1, prime2)
    e = chooseE(totient)

    # compute d, 1 < d < totient such that e*d = 1 (mod totient)
    # e and d are inverses (mod totient)
    gcd, x, y = compute_d(e, totient)

    # make sure d is positive
    if (x < 0):
        d = x + totient
    else:
        d = x

    return(e, n, d)

