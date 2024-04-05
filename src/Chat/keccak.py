def ROL(a, n, bit_length):
    return ((a >> (bit_length - (n % bit_length))) + (a << (n % bit_length))) % (1 << bit_length)

def keccak_f_on_lanes(lanes, bit_length, rounds):
    lane_count = len(lanes)
    for _ in range(rounds):
        # θ
        C = [lanes[x][0] ^ lanes[x][1] ^ lanes[x][2] ^ lanes[x][3] ^ lanes[x][4] for x in range(lane_count)]
        D = [C[(x + 4) % lane_count] ^ ROL(C[(x + 1) % lane_count], 1, bit_length) for x in range(lane_count)]
        lanes = [[lanes[x][y] ^ D[x] for y in range(lane_count)] for x in range(lane_count)]
        # ρ and π
        (x, y) = (1, 0)
        current = lanes[x][y]
        for t in range(24):
            (x, y) = (y, (2 * x + 3 * y) % lane_count)
            (current, lanes[x][y]) = (lanes[x][y], ROL(current, (t + 1) * (t + 2) // 2, bit_length))
        # χ
        for y in range(lane_count):
            T = [lanes[x][y] for x in range(lane_count)]
            for x in range(lane_count):
                lanes[x][y] = T[x] ^ ((~T[(x + 1) % lane_count]) & T[(x + 2) % lane_count])
        # ι
        R = 1
        for j in range(7):
            R = ((R << 1) ^ ((R >> (bit_length - 1)) * 0x71)) % (1 << bit_length)
            if R & 2:
                lanes[0][0] ^= (1 << ((1 << j) - 1))
    return lanes

def keccak_f(state, bit_length, rounds):
    lane_count = len(state) * 8 // bit_length
    lanes = [[int.from_bytes(state[bit_length // 8 * (x + lane_count * y):bit_length // 8 * (x + lane_count * y) + bit_length // 8], 'little') for y in range(lane_count)] for x in range(lane_count)]
    lanes = keccak_f_on_lanes(lanes, bit_length, rounds)
    state = bytearray(lane_count * lane_count * bit_length // 8)
    for x in range(lane_count):
        for y in range(lane_count):
            state[bit_length // 8 * (x + lane_count * y):bit_length // 8 * (x + lane_count * y) + bit_length // 8] = int.to_bytes(lanes[x][y], bit_length // 8, 'little')
    return state

def keccak(rate, capacity, input_bytes, delimited_suffix, output_byte_len, bit_length=1600, rounds=24):
    output_bytes = bytearray()
    state = bytearray([0] * (bit_length // 8))
    rate_in_bytes = rate // 8
    block_size = 0
    if (rate + capacity) != bit_length or (rate % 8) != 0:
        return
    input_offset = 0
    # Absorb all the input blocks
    while input_offset < len(input_bytes):
        block_size = min(len(input_bytes) - input_offset, rate_in_bytes)
        for i in range(block_size):
            state[i] ^= input_bytes[i + input_offset]
        input_offset += block_size
        if block_size == rate_in_bytes:
            state = keccak_f(state, bit_length, rounds)
            block_size = 0
    # Do the padding and switch to the squeezing phase
    state[block_size] ^= delimited_suffix
    if (delimited_suffix & 0x80) != 0 and block_size == (rate_in_bytes - 1):
        state = keccak_f(state, bit_length, rounds)
    state[rate_in_bytes - 1] ^= 0x80
    state = keccak_f(state, bit_length, rounds)
    # Squeeze out all the output blocks
    while output_byte_len > 0:
        block_size = min(output_byte_len, rate_in_bytes)
        output_bytes.extend(state[:block_size])
        output_byte_len -= block_size
        if output_byte_len > 0:
            state = keccak_f(state, bit_length, rounds)
    return output_bytes

def shake_128(input_bytes, output_byte_len):
    return keccak(1344, 256, input_bytes, 0x1F, output_byte_len, bit_length=1600, rounds=24)

def shake_256(input_bytes, output_byte_len):
    return keccak(1088, 512, input_bytes, 0x1F, output_byte_len, bit_length=1600, rounds=24)

def sha3_224(input_bytes):
    return keccak(1152, 448, input_bytes, 0x06, 224 // 8, bit_length=1600, rounds=24)

def sha3_256(input_bytes):
    return keccak(1088, 512, input_bytes, 0x06, 256 // 8, bit_length=1600, rounds=24)

def sha3_384(input_bytes):
    return keccak(832, 768, input_bytes, 0x06, 384 // 8, bit_length=1600, rounds=24)

def sha3_512(input_bytes):
    return keccak(576, 1024, input_bytes, 0x06, 512 // 8, bit_length=1600, rounds=24)

def keccak_main():
    from_file = input("Choose file: ")
    ff = open(from_file, 'rb')
    fff = ff.read()
    return sha3_256(fff)

