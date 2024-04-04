def ROL64(a, n):
    return ((a >> (64 - (n % 64))) + (a << (n % 64))) % (1 << 64)

def keccak_f_1600_on_lanes(lanes):
    R = 1
    for _ in range(24):
        # θ
        C = [lanes[x][0] ^ lanes[x][1] ^ lanes[x][2] ^ lanes[x][3] ^ lanes[x][4] for x in range(5)]
        D = [C[(x + 4) % 5] ^ ROL64(C[(x + 1) % 5], 1) for x in range(5)]
        lanes = [[lanes[x][y] ^ D[x] for y in range(5)] for x in range(5)]
        # ρ and π
        (x, y) = (1, 0)
        current = lanes[x][y]
        for t in range(24):
            (x, y) = (y, (2 * x + 3 * y) % 5)
            (current, lanes[x][y]) = (lanes[x][y], ROL64(current, (t + 1) * (t + 2) // 2))
        # χ
        for y in range(5):
            T = [lanes[x][y] for x in range(5)]
            for x in range(5):
                lanes[x][y] = T[x] ^ ((~T[(x + 1) % 5]) & T[(x + 2) % 5])
        # ι
        for j in range(7):
            R = ((R << 1) ^ ((R >> 7) * 0x71)) % 256
            if R & 2:
                lanes[0][0] ^= (1 << ((1 << j) - 1))
    return lanes

def keccak_f_1600(state):
    lanes = [[int.from_bytes(state[8 * (x + 5 * y):8 * (x + 5 * y) + 8], 'little') for y in range(5)] for x in range(5)]
    lanes = keccak_f_1600_on_lanes(lanes)
    state = bytearray(200)
    for x in range(5):
        for y in range(5):
            state[8 * (x + 5 * y):8 * (x + 5 * y) + 8] = int.to_bytes(lanes[x][y], 8, 'little')
    return state

def keccak(rate, capacity, input_bytes, delimited_suffix, output_byte_len):
    output_bytes = bytearray()
    state = bytearray([0] * 200)
    rate_in_bytes = rate // 8
    block_size = 0
    if (rate + capacity) != 1600 or (rate % 8) != 0:
        return
    input_offset = 0
    # Absorb all the input blocks
    while input_offset < len(input_bytes):
        block_size = min(len(input_bytes) - input_offset, rate_in_bytes)
        for i in range(block_size):
            state[i] ^= input_bytes[i + input_offset]
        input_offset += block_size
        if block_size == rate_in_bytes:
            state = keccak_f_1600(state)
            block_size = 0
    # Do the padding and switch to the squeezing phase
    state[block_size] ^= delimited_suffix
    if (delimited_suffix & 0x80) != 0 and block_size == (rate_in_bytes - 1):
        state = keccak_f_1600(state)
    state[rate_in_bytes - 1] ^= 0x80
    state = keccak_f_1600(state)
    # Squeeze out all the output blocks
    while output_byte_len > 0:
        block_size = min(output_byte_len, rate_in_bytes)
        output_bytes.extend(state[:block_size])
        output_byte_len -= block_size
        if output_byte_len > 0:
            state = keccak_f_1600(state)
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
    ff = open(from_file, 'rb')
    fff = ff.read()
    return sha3_256(fff)
