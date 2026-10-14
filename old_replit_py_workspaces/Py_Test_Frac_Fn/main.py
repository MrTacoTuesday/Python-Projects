
## Provided input
a = [
    0b01, 0b10, 0b01, 0b11, 0b00, 0b00, 0b00, # integer part
    0b00, 0b00, 0b00, 0b00, 0b00, 0b00, 0b00, ... # fractional part
]

## Expected Q values per iteration
b = [0b1, 0b010, 0b1001, 0b00011, 0b001100, 0b0110000, 0b11000000, # integer part completed
    0b010000000, ... # fractional part completed
]

## Expected X values per iteration
c = [0b1, 0b101, 0b1001, 0b10101, 0b101001, 0b1010001, 0b10100001, # integer part completed
    0b101000101, ... # fractional part completed
] 

## Expected answer
d = [0b1, 0b0, 0b1, 0b0, 0b0, 0b0, 0b1, # integer part
    0b0, 0b1, 0b1, 0b1, 0b0, 0b1, 0b1, ... # fractional part
]


#b[n] = ((b[n-1] - c[n-1]) if d[n-1] else b[n-1])<<2 + a[n]
#c[n] = to_int(d[:n])<<2 + 0b01
#d[n] = b[n] >= c[n]

from functools import reduce

def to_int(bits: list[int], group_size: int = 1) -> int:
    return reduce(lambda x, y: x << group_size | y, bits)

def to_bits(n: int, group_size: int = 1) -> list[bytearray]:
    evened_bits = (n.bit_length()//group_size)*group_size
    bits: list[int] = [(n >> i & 1) for i in range(evened_bits-1, -1, -1)]
    #print(bits)
    #for i in range(0, len(bits), group_size):
    #    print(bits[i:i+group_size], to_int(bits[i:i+group_size]))
    grouped = [
        bits[i:i+group_size]
        for i in range(0, len(bits), group_size)
    ]
    return grouped

def int_to_bytes(x: int)->bytearray:
    return bytearray(x.to_bytes(16, 'big'))

k = bytearray((15864834).to_bytes(8, 'big'))
print(k)
for i in k:
    print(i)
