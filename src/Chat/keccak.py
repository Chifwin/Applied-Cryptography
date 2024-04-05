def ROL(a, n, width):
    return ((a << n) | (a >> (width - n))) % (1 << width)

def keccak_p(state, rounds):
    state_size = len(state)
    width = state_size * 8
    lane_size = width // 25
    for rnd in range(rounds):
        # θ
        C = [state[x] ^ state[x + 5] ^ state[x + 10] ^ state[x + 15] ^ state[x + 20] for x in range(5)]
        D = [C[(x + 4) % 5] ^ ROL(C[(x + 1) % 5], 1, lane_size) for x in range(5)]
        state = [state[x] ^ D[x] for x in range(25)]
        # ρ and π
        (x, y) = (1, 0)
        current = state[x + 5 * y]
        for t in range(24):
            (x, y) = (y, (2 * x + 3 * y) % 5)
            index = x + 5 * y
            (current, state[index]) = (state[index], ROL(current, (t + 1) * (t + 2) // 2, lane_size))
        # χ
        for y in range(5):
            T = [state[x + 5 * y] for x in range(5)]
            for x in range(5):
                index = x + 5 * y
                state[index] = T[x] ^ ((~T[(x + 1) % 5]) & T[(x + 2) % 5])
        # ι
        RC = [1]
        for j in range(1, 24):
            RC.append((RC[j - 1] << 1) ^ ((RC[j - 1] >> 7) * 0x71))
        for i in range(7):
            state[0] ^= RC[i] << (i * 8)
    return state

def keccak_f(state, capacity):
    rate = len(state) * 8 - capacity
    rounds = 12 + 2 * (rate // 32)
    return keccak_p(state, rounds)

def keccak(rate, capacity, input_bytes, delimited_suffix, output_byte_len):
    output_bytes = bytearray()
    state = bytearray([0] * (rate // 8))
    block_size = 0
    rate_in_bytes = rate // 8
    if (rate + capacity) != len(state) * 8 or (rate % 8) != 0:
        return
    input_offset = 0
    # Absorb all the input blocks
    while input_offset < len(input_bytes):
        block_size = min(len(input_bytes) - input_offset, rate_in_bytes)
        for i in range(block_size):
            state[i] ^= input_bytes[i + input_offset]
        input_offset += block_size
        if block_size == rate_in_bytes:
            state = keccak_f(state, capacity)
            block_size = 0
    # Do the padding and switch to the squeezing phase
    state[block_size] ^= delimited_suffix
    if (delimited_suffix & 0x80) != 0 and block_size == (rate_in_bytes - 1):
        state = keccak_f(state, capacity)
    state[rate_in_bytes - 1] ^= 0x80
    state = keccak_f(state, capacity)
    # Squeeze out all the output blocks
    while output_byte_len > 0:
        block_size = min(output_byte_len, rate_in_bytes)
        output_bytes.extend(state[:block_size])
        output_byte_len -= block_size
        if output_byte_len > 0:
            state = keccak_f(state, capacity)
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
