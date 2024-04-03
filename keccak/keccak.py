# -*- coding: utf-8 -*-
# Implementation by Gilles Van Assche, hereby denoted as "the implementer".
#
# For more information, feedback or questions, please refer to our website:
# https://keccak.team/
#
# To the extent possible under law, the implementer has waived all copyright
# and related or neighboring rights to the source code in this file.
# http://creativecommons.org/publicdomain/zero/1.0/

def ROL64(a, n):
    return ((a >> (64-(n%64))) + (a << (n%64))) % (1 << 64)

def KeccakF1600onLanes(lanes):
    R = 1
    for round in range(24):
        # θ
        C = [lanes[x][0] ^ lanes[x][1] ^ lanes[x][2] ^ lanes[x][3] ^ lanes[x][4] for x in range(5)]
        D = [C[(x+4)%5] ^ ROL64(C[(x+1)%5], 1) for x in range(5)]
        lanes = [[lanes[x][y]^D[x] for y in range(5)] for x in range(5)]
        # ρ and π
        (x, y) = (1, 0)
        current = lanes[x][y]
        for t in range(24):
            (x, y) = (y, (2*x+3*y)%5)
            (current, lanes[x][y]) = (lanes[x][y], ROL64(current, (t+1)*(t+2)//2))
        # χ
        for y in range(5):
            T = [lanes[x][y] for x in range(5)]
            for x in range(5):
                lanes[x][y] = T[x] ^((~T[(x+1)%5]) & T[(x+2)%5])
        # ι
        for j in range(7):
            R = ((R << 1) ^ ((R >> 7)*0x71)) % 256
            if (R & 2):
                lanes[0][0] = lanes[0][0] ^ (1 << ((1<<j)-1))
    return lanes

def load64(b):
    return sum((b[i] << (8*i)) for i in range(8))

def store64(a):
    return list((a >> (8*i)) % 256 for i in range(8))

def KeccakF(state, stateSizeBits):
    rate = stateSizeBits // 25
    capacity = stateSizeBits - 2 * rate
    lanes = [state[i*8:i*8+8] for i in range(len(state)//8)]  # Разбиваем состояние на линии
    lanes = KeccakF1600onLanes(lanes)
    state = bytearray(stateSizeBits // 8)
    for x in range(5):
        for y in range(5):
            state[x*8+y*40:x*8+y*40+8] = store64(lanes[x][y])
    return state

def Keccak(rate, capacity, inputBytes, delimitedSuffix, outputByteLen):
    outputBytes = bytearray()
    state = bytearray([0 for i in range((rate + capacity) // 8)])  # Инициализируем состояние с учетом размера rate и capacity
    blockSize = 0
    if (((rate + capacity) % 8) != 0):
        return
    inputOffset = 0
    # === Absorb all the input blocks ===
    while(inputOffset < len(inputBytes)):
        blockSize = min(len(inputBytes)-inputOffset, rate//8)
        for i in range(blockSize):
            state[i] = state[i] ^ inputBytes[i+inputOffset]
        inputOffset = inputOffset + blockSize
        if (blockSize == rate//8):
            state = KeccakF(state, rate + capacity)  # Используем общую функцию KeccakF
            blockSize = 0
    # === Do the padding and switch to the squeezing phase ===
    state[blockSize] = state[blockSize] ^ delimitedSuffix
    if (((delimitedSuffix & 0x80) != 0) and (blockSize == (rate//8-1))):
        state = KeccakF(state, rate + capacity)  # Используем общую функцию KeccakF
    state[rate//8-1] = state[rate//8-1] ^ 0x80
    state = KeccakF(state, rate + capacity)  # Используем общую функцию KeccakF
    # === Squeeze out all the output blocks ===
    while(outputByteLen > 0):
        blockSize = min(outputByteLen, rate//8)
        outputBytes.extend(state[:blockSize])  # Используем метод extend для добавления элементов в выходной буфер
        outputByteLen = outputByteLen - blockSize
        if (outputByteLen > 0):
            state = KeccakF(state, rate + capacity)  # Используем общую функцию KeccakF
    return outputBytes

def SHAKE128(inputBytes, outputByteLen):
    return Keccak(1344, 256, inputBytes, 0x1F, outputByteLen)

def SHAKE256(inputBytes, outputByteLen):
    return Keccak(1088, 512, inputBytes, 0x1F, outputByteLen)

def SHA3_224(inputBytes):
    return Keccak(1152, 448, inputBytes, 0x06, 224//8)

def SHA3_256(inputBytes):
    return Keccak(1088, 512, inputBytes, 0x06, 256//8)

def SHA3_384(inputBytes):
    return Keccak(832, 768, inputBytes, 0x06, 384//8)

def SHA3_512(inputBytes):
    return Keccak(576, 1024, inputBytes, 0x06, 512//8)
