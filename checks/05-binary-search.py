# Checks for site/topics/05-binary-search.html
# Every function on the page lives here and is tested on the lesson's own examples.

import bisect
import math

# ---------------------------------------------------------------
# Lesson 14: search an array (NeetCode version, exact match)
# ---------------------------------------------------------------
arr = [1, 3, 3, 4, 5, 6, 7, 8]      # the array in NeetCode's code block


def binarySearch(arr, target):
    L, R = 0, len(arr) - 1

    while L <= R:
        mid = (L + R) // 2

        if target > arr[mid]:
            L = mid + 1
        elif target < arr[mid]:
            R = mid - 1
        else:
            return mid
    return -1


nums = [1, 2, 3, 4, 5, 6, 7, 8]     # the array in NeetCode's walkthrough
assert binarySearch(nums, 5) == 4
assert binarySearch(nums, 9) == -1
assert binarySearch(nums, 1) == 0
assert binarySearch(nums, 8) == 7
assert binarySearch(nums, 0) == -1
assert binarySearch([], 3) == -1
assert binarySearch([7], 7) == 0
assert binarySearch([7], 3) == -1
assert binarySearch(arr, 4) == 3
assert binarySearch(arr, 3) in (1, 2)     # duplicates: either index is valid
assert binarySearch(arr, 2) == -1


# --- traced version, records (L, R, mid, arr[mid], action) per loop turn ---
def binarySearchTrace(arr, target):
    L, R = 0, len(arr) - 1
    rows = []
    while L <= R:
        mid = (L + R) // 2
        if target > arr[mid]:
            rows.append((L, R, mid, arr[mid], "L = mid + 1"))
            L = mid + 1
        elif target < arr[mid]:
            rows.append((L, R, mid, arr[mid], "R = mid - 1"))
            R = mid - 1
        else:
            rows.append((L, R, mid, arr[mid], "return mid"))
            return mid, rows, (L, R)
    rows.append((L, R, None, None, "L > R -> return -1"))
    return -1, rows, (L, R)


res, rows, final = binarySearchTrace(nums, 5)
assert res == 4
assert rows == [
    (0, 7, 3, 4, "L = mid + 1"),
    (4, 7, 5, 6, "R = mid - 1"),
    (4, 4, 4, 5, "return mid"),
], rows

res, rows, final = binarySearchTrace(nums, 9)
assert res == -1
assert rows == [
    (0, 7, 3, 4, "L = mid + 1"),
    (4, 7, 5, 6, "L = mid + 1"),
    (6, 7, 6, 7, "L = mid + 1"),
    (7, 7, 7, 8, "L = mid + 1"),
    (8, 7, None, None, "L > R -> return -1"),
], rows
assert final == (8, 7)          # L walked off the right end; L > R


# --- overflow-safe mid ---
def binary_search_safe_mid(arr, target):
    L, R = 0, len(arr) - 1
    while L <= R:
        mid = L + (R - L) // 2
        if target > arr[mid]:
            L = mid + 1
        elif target < arr[mid]:
            R = mid - 1
        else:
            return mid
    return -1


for t in range(0, 11):
    assert binary_search_safe_mid(nums, t) == binarySearch(nums, t)

# Python ints do not overflow: this is fine in Python, would overflow a 32-bit int
big = 2**31 - 1
assert (big + big) // 2 == big
assert big + (big - big) // 2 == big


# --- log2 sanity: halving n -> n/2 -> n/4 ... -> 1 takes log2(n) steps ---
def halvings(n):
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


assert halvings(8) == 3 == int(math.log2(8))
assert halvings(1024) == 10 == int(math.log2(1024))
assert halvings(1_000_000) == 19 == math.floor(math.log2(1_000_000))
# worst case comparisons for n=8 is at most floor(log2 8) + 1 = 4 (the target=9 trace above did 4)
assert len([r for r in binarySearchTrace(nums, 9)[1] if r[2] is not None]) == 4


# ---------------------------------------------------------------
# Lesson 15: search a range (guess the number)
# ---------------------------------------------------------------
# Return 1 if n is too big, -1 if too small, 0 if correct
def isCorrect(n):
    if n > 10:
        return 1
    elif n < 10:
        return -1
    else:
        return 0


# Binary search on some range of values
def binarySearchRange(low, high):

    while low <= high:
        mid = (low + high) // 2

        if isCorrect(mid) > 0:
            high = mid - 1
        elif isCorrect(mid) < 0:
            low = mid + 1
        else:
            return mid
    return -1


assert isCorrect(50) == 1
assert isCorrect(3) == -1
assert isCorrect(10) == 0
assert binarySearchRange(1, 100) == 10
assert binarySearchRange(1, 10) == 10
assert binarySearchRange(10, 10) == 10
assert binarySearchRange(11, 100) == -1
assert binarySearchRange(1, 9) == -1


def binarySearchRangeTrace(low, high):
    rows = []
    while low <= high:
        mid = (low + high) // 2
        r = isCorrect(mid)
        if r > 0:
            rows.append((low, high, mid, "too big", "high = mid - 1"))
            high = mid - 1
        elif r < 0:
            rows.append((low, high, mid, "too small", "low = mid + 1"))
            low = mid + 1
        else:
            rows.append((low, high, mid, "correct", "return mid"))
            return mid, rows
    return -1, rows


res, rows = binarySearchRangeTrace(1, 100)
assert res == 10
assert rows == [
    (1, 100, 50, "too big", "high = mid - 1"),
    (1, 49, 25, "too big", "high = mid - 1"),
    (1, 24, 12, "too big", "high = mid - 1"),
    (1, 11, 6, "too small", "low = mid + 1"),
    (7, 11, 9, "too small", "low = mid + 1"),
    (10, 11, 10, "correct", "return mid"),
], rows
assert len(rows) == 6 <= math.floor(math.log2(100)) + 1   # 6 <= 7


# ---------------------------------------------------------------
# Template 1: exact match (same as binarySearch, shown as a template)
# ---------------------------------------------------------------
def exact_match(nums, target):
    L, R = 0, len(nums) - 1
    while L <= R:
        mid = L + (R - L) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            L = mid + 1
        else:
            R = mid - 1
    return -1


assert exact_match(nums, 5) == 4
assert exact_match(nums, 9) == -1


# ---------------------------------------------------------------
# Template 2: boundary / lower bound / first True  (while L < R)
# ---------------------------------------------------------------
def lower_bound(nums, target):
    """First index i with nums[i] >= target. Returns len(nums) if none."""
    L, R = 0, len(nums)            # R is one past the end: "not found" is a valid answer
    while L < R:
        mid = L + (R - L) // 2
        if nums[mid] < target:
            L = mid + 1            # mid is too small: answer is to the right
        else:
            R = mid                # mid could be the answer: keep it
    return L


assert lower_bound([1, 2, 2, 2, 5], 2) == 1
assert lower_bound([1, 2, 2, 2, 5], 3) == 4
assert lower_bound([1, 2, 2, 2, 5], 6) == 5
assert lower_bound([1, 2, 2, 2, 5], 0) == 0
assert lower_bound(nums, 5) == 4
assert lower_bound(nums, 9) == 8
assert lower_bound([], 3) == 0
for t in range(0, 8):
    assert lower_bound([1, 2, 2, 2, 5], t) == bisect.bisect_left([1, 2, 2, 2, 5], t)


def upper_bound(nums, target):
    """First index i with nums[i] > target."""
    L, R = 0, len(nums)
    while L < R:
        mid = L + (R - L) // 2
        if nums[mid] <= target:
            L = mid + 1
        else:
            R = mid
    return L


for t in range(0, 8):
    assert upper_bound([1, 2, 2, 2, 5], t) == bisect.bisect_right([1, 2, 2, 2, 5], t)


def first_true(n, is_true):
    """Smallest i in [0, n) with is_true(i) True, given F F F T T T. Returns n if none."""
    L, R = 0, n
    while L < R:
        mid = L + (R - L) // 2
        if is_true(mid):
            R = mid
        else:
            L = mid + 1
    return L


flags = [False, False, False, True, True, True]
assert first_true(len(flags), lambda i: flags[i]) == 3
assert first_true(6, lambda i: False) == 6
assert first_true(6, lambda i: True) == 0


# First Bad Version (LC 278) style: versions 1..n, isBadVersion monotonic F..F T..T
def first_bad_version(n, isBadVersion):
    L, R = 1, n
    while L < R:
        mid = L + (R - L) // 2
        if isBadVersion(mid):
            R = mid
        else:
            L = mid + 1
    return L


assert first_bad_version(5, lambda v: v >= 4) == 4
assert first_bad_version(1, lambda v: v >= 1) == 1
assert first_bad_version(10, lambda v: v >= 10) == 10


# Search Insert Position (LC 35) is exactly lower_bound
def search_insert(nums, target):
    return lower_bound(nums, target)


assert search_insert([1, 3, 5, 6], 5) == 2
assert search_insert([1, 3, 5, 6], 2) == 1
assert search_insert([1, 3, 5, 6], 7) == 4


# Find First and Last Position (LC 34) = lower_bound + upper_bound - 1
def search_range(nums, target):
    lo = lower_bound(nums, target)
    if lo == len(nums) or nums[lo] != target:
        return [-1, -1]
    return [lo, upper_bound(nums, target) - 1]


assert search_range([5, 7, 7, 8, 8, 10], 8) == [3, 4]
assert search_range([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
assert search_range([], 0) == [-1, -1]


# ---------------------------------------------------------------
# Template 3: binary search on the answer (Koko Eating Bananas, LC 875)
# ---------------------------------------------------------------
def min_eating_speed(piles, h):
    def can_finish(k):                       # the "isCorrect" black box
        hours = 0
        for p in piles:
            hours += (p + k - 1) // k        # ceil(p / k) with integers
        return hours <= h

    L, R = 1, max(piles)                     # answer space: speeds 1..max pile
    while L < R:
        mid = L + (R - L) // 2
        if can_finish(mid):
            R = mid                          # mid works: try slower
        else:
            L = mid + 1                      # too slow: need faster
    return L


assert min_eating_speed([3, 6, 7, 11], 8) == 4
assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
assert min_eating_speed([30, 11, 23, 4, 20], 6) == 23
assert (7 + 4 - 1) // 4 == math.ceil(7 / 4) == 2


# Sqrt(x) (LC 69): largest k with k*k <= x  -> "last True" flavour
def my_sqrt(x):
    L, R = 0, x
    while L <= R:
        mid = L + (R - L) // 2
        if mid * mid <= x:
            L = mid + 1                       # mid fits: remember it, look right
        else:
            R = mid - 1
    return R                                  # R stops on the last mid that fit


assert my_sqrt(4) == 2
assert my_sqrt(8) == 2
assert my_sqrt(0) == 0
assert my_sqrt(1) == 1
for x in range(0, 200):
    assert my_sqrt(x) == math.isqrt(x), x


# ---------------------------------------------------------------
# Search a 2D Matrix (LC 74): flatten index math
# ---------------------------------------------------------------
def search_matrix(matrix, target):
    rows, cols = len(matrix), len(matrix[0])
    L, R = 0, rows * cols - 1
    while L <= R:
        mid = L + (R - L) // 2
        val = matrix[mid // cols][mid % cols]
        if val == target:
            return True
        if val < target:
            L = mid + 1
        else:
            R = mid - 1
    return False


m = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]
assert search_matrix(m, 3) is True
assert search_matrix(m, 13) is False
assert search_matrix(m, 60) is True


# ---------------------------------------------------------------
# Find Minimum in Rotated Sorted Array (LC 153): compare mid to R
# ---------------------------------------------------------------
def find_min_rotated(nums):
    L, R = 0, len(nums) - 1
    while L < R:
        mid = L + (R - L) // 2
        if nums[mid] > nums[R]:
            L = mid + 1                       # min is to the right of mid
        else:
            R = mid                           # mid could be the min
    return nums[L]


assert find_min_rotated([3, 4, 5, 1, 2]) == 1
assert find_min_rotated([4, 5, 6, 7, 0, 1, 2]) == 0
assert find_min_rotated([11, 13, 15, 17]) == 11
assert find_min_rotated([2, 1]) == 1


# ---------------------------------------------------------------
# bisect module
# ---------------------------------------------------------------
a = [1, 2, 2, 2, 5]
assert bisect.bisect_left(a, 2) == 1
assert bisect.bisect_right(a, 2) == 4
assert bisect.bisect_left(a, 3) == 4
assert bisect.bisect_left(a, 9) == 5
b = a[:]
bisect.insort(b, 3)
assert b == [1, 2, 2, 2, 3, 5]
i = bisect.bisect_left(nums, 5)
assert i < len(nums) and nums[i] == 5          # "found" check with bisect_left
i = bisect.bisect_left(nums, 9)
assert not (i < len(nums) and nums[i] == 9)


# the "recursive" version, to show it is the same idea as merge sort's halving
def binary_search_rec(arr, target, L, R):
    if L > R:
        return -1
    mid = L + (R - L) // 2
    if arr[mid] == target:
        return mid
    if target > arr[mid]:
        return binary_search_rec(arr, target, mid + 1, R)
    return binary_search_rec(arr, target, L, mid - 1)


assert binary_search_rec(nums, 5, 0, 7) == 4
assert binary_search_rec(nums, 9, 0, 7) == -1

# The common off-by-one bug: while L < R with R = len-1 misses a target at the last index
def buggy_search(arr, target):
    L, R = 0, len(arr) - 1
    while L < R:                              # BUG
        mid = (L + R) // 2
        if target > arr[mid]:
            L = mid + 1
        elif target < arr[mid]:
            R = mid - 1
        else:
            return mid
    return -1


assert buggy_search([7], 7) == -1             # demonstrates the bug: 7 is there, but never checked
assert binarySearch([7], 7) == 0

print("all checks passed")
