# Checks for site/topics/12-bit-manipulation.html
# Every function and every operator example on the page is tested here.

# --- Lesson operator examples (verbatim) ---
n = 1 & 1
assert n == 1, n
n = 1 | 0
assert n == 1, n
n = 0 ^ 1
assert n == 1, n
n = ~n
assert n == -2, n            # ~1 == -1 - 1 == -2 in Python
n = 1
n = n << 1
assert n == 2, n
n = n >> 1
assert n == 1, n

# --- Full truth tables ---
assert [a & b for a in (0, 1) for b in (0, 1)] == [0, 0, 0, 1]
assert [a | b for a in (0, 1) for b in (0, 1)] == [0, 1, 1, 1]
assert [a ^ b for a in (0, 1) for b in (0, 1)] == [0, 1, 1, 0]
assert 1 ^ 1 == 0

# --- Left shift of 001 three times, in a 3-bit register ---
MASK3 = 0b111
x = 0b001
steps = []
for _ in range(3):
    x = (x << 1) & MASK3        # keep only 3 bits so the 1 "falls off"
    steps.append(x)
assert steps == [0b010, 0b100, 0b000], steps
# In plain Python nothing falls off: ints grow.
assert (1 << 3) == 8

# --- Shifts are multiply / divide by 2 ---
assert 5 << 1 == 10
assert 22 >> 1 == 11
assert 0b10110 == 22 and 0b01011 == 11
assert 23 >> 1 == 11 == 23 // 2
assert 7 << 2 == 28 == 7 * 4

# --- Binary <-> decimal ---
assert 0b10111 == 23
assert 1 * 16 + 0 * 8 + 1 * 4 + 1 * 2 + 1 * 1 == 23
assert bin(23) == "0b10111"
assert bin(23)[2:] == "10111"
assert format(23, "08b") == "00010111"
assert f"{23:b}" == "10111"
assert int("10111", 2) == 23
assert int("00010111", 2) == 23


# --- Counting Bits (NeetCode version) ---
def countBits(n):
    count = 0
    while n > 0:
        if n & 1 == 1:
            count += 1
        n = n >> 1  # same as n // 2
    return count


assert countBits(23) == 4
assert countBits(0) == 0
assert countBits(1) == 1
assert countBits(255) == 8
assert countBits(1024) == 1


def countBitsTrace(n):
    """Return the rows of the trace table: (n_bits, n&1, count, n>>1)."""
    rows = []
    count = 0
    while n > 0:
        low = n & 1
        if low == 1:
            count += 1
        n = n >> 1
        rows.append((low, count, n))
    return rows


trace = countBitsTrace(23)
assert trace == [
    (1, 1, 0b01011),
    (1, 2, 0b00101),
    (1, 3, 0b00010),
    (0, 3, 0b00001),
    (1, 4, 0b00000),
], trace


# --- Kernighan: n & (n - 1) clears the lowest set bit ---
def countBitsKernighan(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


assert 0b10110 & (0b10110 - 1) == 0b10100
assert 22 & 21 == 20
assert 0b10111 & 0b10110 == 0b10110
assert countBitsKernighan(23) == 4
assert countBitsKernighan(22) == 3
assert countBitsKernighan(0) == 0
for v in range(0, 300):
    assert countBitsKernighan(v) == countBits(v) == bin(v).count("1") == v.bit_count()


# --- Power of two ---
def isPowerOfTwo(n):
    return n > 0 and n & (n - 1) == 0


assert isPowerOfTwo(1) and isPowerOfTwo(2) and isPowerOfTwo(16) and isPowerOfTwo(1024)
assert not isPowerOfTwo(0) and not isPowerOfTwo(6) and not isPowerOfTwo(-8) and not isPowerOfTwo(12)


# --- Odd / even ---
def isOdd(n):
    return n & 1 == 1


assert isOdd(23) and isOdd(1) and not isOdd(22) and not isOdd(0)


# --- Masks: set / clear / test / toggle bit k ---
def get_bit(n, k):
    return (n >> k) & 1


def set_bit(n, k):
    return n | (1 << k)


def clear_bit(n, k):
    return n & ~(1 << k)


def toggle_bit(n, k):
    return n ^ (1 << k)


assert 1 << 0 == 1 and 1 << 3 == 8 and 1 << 4 == 16
assert [get_bit(23, k) for k in range(5)] == [1, 1, 1, 0, 1]
assert set_bit(23, 3) == 31 == 0b11111
assert set_bit(23, 0) == 23            # already set: no change
assert clear_bit(23, 0) == 22 == 0b10110
assert clear_bit(23, 3) == 23          # already clear: no change
assert toggle_bit(23, 3) == 31
assert toggle_bit(31, 3) == 23
assert ~(1 << 2) == -5                 # ...11111011


# --- XOR: single number ---
def singleNumber(nums):
    result = 0
    for x in nums:
        result ^= x
    return result


assert 5 ^ 5 == 0 and 5 ^ 0 == 5
assert singleNumber([4, 1, 2, 1, 2]) == 4
assert singleNumber([2, 2, 1]) == 1
assert singleNumber([7]) == 7
# trace of the running XOR on [4,1,2,1,2]
run, seen = 0, []
for x in [4, 1, 2, 1, 2]:
    run ^= x
    seen.append(run)
assert seen == [4, 5, 7, 6, 4], seen
# order does not matter
assert singleNumber([1, 2, 4, 2, 1]) == 4


# --- Missing number with XOR ---
def missingNumber(nums):
    result = len(nums)
    for i, x in enumerate(nums):
        result ^= i ^ x
    return result


assert missingNumber([3, 0, 1]) == 2
assert missingNumber([0, 1]) == 2
assert missingNumber([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8


# --- Bitmask as a set ---
def subsets_by_mask(items):
    n = len(items)
    out = []
    for mask in range(1 << n):
        sub = [items[i] for i in range(n) if mask >> i & 1]
        out.append(sub)
    return out


subs = subsets_by_mask(["a", "b", "c"])
assert len(subs) == 8
assert subs[0] == [] and subs[7] == ["a", "b", "c"]
assert subs[0b101] == ["a", "c"]
assert sorted(map(tuple, subs)) == sorted(
    [(), ("a",), ("b",), ("c",), ("a", "b"), ("a", "c"), ("b", "c"), ("a", "b", "c")]
)

# set operations on masks
A = 0b0110  # {1, 2}
B = 0b0011  # {0, 1}
assert A | B == 0b0111   # union
assert A & B == 0b0010   # intersection
assert A & ~B == 0b0100  # difference A - B
assert (A >> 2) & 1 == 1  # 2 in A
assert (A >> 0) & 1 == 0  # 0 not in A

# --- Hamming distance ---
def hammingDistance(a, b):
    return countBitsKernighan(a ^ b)


assert hammingDistance(1, 4) == 2
assert hammingDistance(23, 22) == 1


# --- Reverse bits of a 32-bit int ---
def reverseBits(n):
    res = 0
    for i in range(32):
        bit = (n >> i) & 1
        res |= bit << (31 - i)
    return res


assert reverseBits(0b00000010100101000001111010011100) == 964176192
assert reverseBits(1) == 1 << 31
assert reverseBits(0) == 0


# --- Sum of two integers without + (32-bit two's complement) ---
def getSum(a, b):
    mask = 0xFFFFFFFF
    while b != 0:
        carry = (a & b) << 1
        a = (a ^ b) & mask
        b = carry & mask
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)


assert getSum(1, 2) == 3
assert getSum(2, 3) == 5
assert getSum(-1, 1) == 0
assert getSum(-12, 5) == -7
assert getSum(20, -30) == -10

# --- Python: no overflow, ~n == -n - 1, two's complement view ---
assert (1 << 100) == 2 ** 100
assert (1 << 100) > 0
assert ~0 == -1 and ~1 == -2 and ~23 == -24 and ~(-1) == 0
for v in range(-50, 50):
    assert ~v == -v - 1
assert bin(-5) == "-0b101"               # Python shows sign + magnitude
assert (-5) & 0xFF == 0b11111011 == 251  # 8-bit two's complement of -5
assert (-1) & 0xFF == 255
assert -8 >> 1 == -4                     # arithmetic shift keeps the sign
assert -7 >> 1 == -4                     # rounds toward minus infinity, like //
assert -7 // 2 == -4

print("all checks passed")
