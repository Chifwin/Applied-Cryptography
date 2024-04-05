def ROL64(a, n):
    return ((a >> (64 - (n % 64))) + (a << (n % 64))) % (1 << 64)

def keccak_f(state, rounds):
    R = 1
    for _ in range(rounds):
        # θ
        C = [state[x][0] ^ state[x][1] ^ state[x][2] ^ state[x][3] ^ state[x][4] for x in range(5)]
        D = [C[(x + 4) % 5] ^ ROL64(C[(x + 1) % 5], 1) for x in range(5)]
        state = [[state[x][y] ^ D[x] for y in range(5)] for x in range(5)]
        # ρ and π
        (x, y) = (1, 0)
        current = state[x][y]
        for t in range(24):
            (x, y) = (y, (2 * x + 3 * y) % 5)
            (current, state[x][y]) = (state[x][y], ROL64(current, (t + 1) * (t + 2) // 2))
        # χ
        for y in range(5):
            T = [state[x][y] for x in range(5)]
            for x in range(5):
                state[x][y] = T[x] ^ ((~T[(x + 1) % 5]) & T[(x + 2) % 5])
        # ι
        for j in range(7):
            R = ((R << 1) ^ ((R >> 7) * 0x71)) % 256
            if R & 2:
                state[0][0] ^= (1 << ((1 << j) - 1))
    return state

def keccak(rate, capacity, input_bytes, delimited_suffix, output_byte_len):
    output_bytes = bytearray()
    state = [[0] * 5 for _ in range(5)]  # Initialize state as a 5x5 matrix
    rate_in_bytes = rate // 8
    block_size = 0
    input_offset = 0
    # Absorb all the input blocks
    while input_offset < len(input_bytes):
        block_size = min(len(input_bytes) - input_offset, rate_in_bytes)
        for i in range(block_size):
            state[i % 5][(i // 8) % 5] ^= input_bytes[i + input_offset]
        input_offset += block_size
        if block_size == rate_in_bytes:
            state = keccak_f(state, 24)
            block_size = 0
    # Do the padding and switch to the squeezing phase
    state[block_size % 5][(block_size // 8) % 5] ^= delimited_suffix
    if (delimited_suffix & 0x80) != 0 and block_size == (rate_in_bytes - 1):
        state = keccak_f(state, 24)
    state[rate_in_bytes % 5][(rate_in_bytes // 8) % 5] ^= 0x80
    state = keccak_f(state, 24)
    # Squeeze out all the output blocks
    while output_byte_len > 0:
        block_size = min(output_byte_len, rate_in_bytes)
        for i in range(block_size):
            output_bytes.append(state[i % 5][(i // 8) % 5] & 0xFF)  # Truncate to fit byte range
        output_byte_len -= block_size
        if output_byte_len > 0:
            state = keccak_f(state, 24)
    return output_bytes

def shake_128(input_bytes, output_byte_len):
    return keccak(1344, 256, input_bytes, 0x1F, output_byte_len)

def shake_256(input_bytes, output_byte_len):
    return keccak(1088, 512, input_bytes, 0x1F, output_byte_len)

def sha3_224(input_bytes):
    return keccak(1152, 448, input_bytes, 0x06, 224 // 8)

def sha3_256(input_bytes):
    return keccak(1088, 512, input_bytes, 0x06, 256 // 8)

def sha3_384(input_bytes):
    return keccak(832, 768, input_bytes, 0x06, 384 // 8)

def sha3_512(input_bytes):
    return keccak(576, 1024, input_bytes, 0x06, 512 // 8)

def keccak_main():
    from_file = input("Choose file: ")
    with open(from_file, 'rb') as ff:
        fff = ff.read()
    return sha3_256(fff)


print(keccak_main())
print(hex(int.from_bytes(sha3_256(''.encode()), 'big')))
