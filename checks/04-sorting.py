# Checks for site/topics/04-sorting.html
# Every function that appears on the page is here, tested on the lesson's own arrays
# plus edge cases: empty, one element, duplicates, already sorted, reverse sorted.

import random
from itertools import permutations
from functools import cmp_to_key
from collections import Counter


# ---------------------------------------------------------------- Lesson 10: insertion sort
def insertionSort(arr):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        j = i - 1
        while j >= 0 and arr[j + 1] < arr[j]:
            # arr[j] and arr[j + 1] are out of order so swap them
            tmp = arr[j + 1]
            arr[j + 1] = arr[j]
            arr[j] = tmp
            j -= 1
    return arr


def insertion_sort_py(arr):
    # idiomatic Python: tuple swap
    for i in range(1, len(arr)):
        j = i - 1
        while j >= 0 and arr[j + 1] < arr[j]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
            j -= 1
    return arr


def insertion_sort_trace(arr):
    """Returns the array state after every pass i (used for the trace table)."""
    states = []
    for i in range(1, len(arr)):
        j = i - 1
        swaps = 0
        while j >= 0 and arr[j + 1] < arr[j]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
            j -= 1
            swaps += 1
        states.append((i, swaps, list(arr)))
    return states


# ---------------------------------------------------------------- Lesson 11: merge sort
# Implementation of MergeSort
def mergeSort(arr, s, e):
    if e - s + 1 <= 1:
        return arr

    # The middle index of the array
    m = (s + e) // 2

    # Sort the left half
    mergeSort(arr, s, m)

    # Sort the right half
    mergeSort(arr, m + 1, e)

    # Merge sorted halfs
    merge(arr, s, m, e)

    return arr


# Merge in-place
def merge(arr, s, m, e):
    # Copy the sorted left & right halfs to temp arrays
    L = arr[s: m + 1]
    R = arr[m + 1: e + 1]

    i = 0  # index for L
    j = 0  # index for R
    k = s  # index for arr

    # Merge the two sorted halfs into the original array
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # One of the halfs will have elements remaining
    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1
    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1


def merge_sort_py(arr):
    """Returns a new sorted list (the 'slice and rebuild' version people write in interviews)."""
    if len(arr) <= 1:
        return arr
    m = len(arr) // 2
    left = merge_sort_py(arr[:m])
    right = merge_sort_py(arr[m:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def merge_trace(L, R):
    """Step table for the three-pointer merge."""
    arr = [None] * (len(L) + len(R))
    i = j = k = 0
    rows = []
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            arr[k] = L[i]; taken = f"L[{i}]={L[i]}"; i += 1
        else:
            arr[k] = R[j]; taken = f"R[{j}]={R[j]}"; j += 1
        k += 1
        rows.append((taken, i, j, k, list(arr)))
    while i < len(L):
        arr[k] = L[i]; rows.append((f"L[{i}]={L[i]} (leftover)", i + 1, j, k + 1, list(arr))); i += 1; k += 1
    while j < len(R):
        arr[k] = R[j]; rows.append((f"R[{j}]={R[j]} (leftover)", i, j + 1, k + 1, list(arr))); j += 1; k += 1
    return rows


# ---------------------------------------------------------------- Lesson 12: quick sort
# Implementation of QuickSort
def quickSort(arr: list[int], s: int, e: int) -> list[int]:
    if e - s + 1 <= 1:
        return arr

    pivot = arr[e]
    left = s  # pointer for left side

    # Partition: elements smaller than pivot on left side
    for i in range(s, e):
        if arr[i] < pivot:
            tmp = arr[left]
            arr[left] = arr[i]
            arr[i] = tmp
            left += 1

    # Move pivot in-between left & right sides
    arr[e] = arr[left]
    arr[left] = pivot

    # Quick sort left side
    quickSort(arr, s, left - 1)

    # Quick sort right side
    quickSort(arr, left + 1, e)

    return arr


def partition_trace(arr, s, e):
    """Row per i for the partition step (used for the trace table)."""
    pivot = arr[e]
    left = s
    rows = []
    for i in range(s, e):
        if arr[i] < pivot:
            arr[left], arr[i] = arr[i], arr[left]
            left += 1
            rows.append((i, arr[i] if i != left - 1 else arr[left - 1], True, left, list(arr)))
        else:
            rows.append((i, arr[i], False, left, list(arr)))
    arr[e], arr[left] = arr[left], arr[e]
    rows.append(("pivot swap", pivot, None, left, list(arr)))
    return rows


def quick_sort_random(arr, s, e):
    """Randomized pivot: swap a random element into the last slot, then partition as before."""
    if e - s + 1 <= 1:
        return arr
    r = random.randint(s, e)
    arr[r], arr[e] = arr[e], arr[r]
    pivot = arr[e]
    left = s
    for i in range(s, e):
        if arr[i] < pivot:
            arr[left], arr[i] = arr[i], arr[left]
            left += 1
    arr[e], arr[left] = arr[left], arr[e]
    quick_sort_random(arr, s, left - 1)
    quick_sort_random(arr, left + 1, e)
    return arr


# ---------------------------------------------------------------- Lesson 13: bucket sort
def bucketSort(arr):
    # Assuming arr only contains 0, 1 or 2
    counts = [0, 0, 0]

    # Count the quantity of each val in arr
    for n in arr:
        counts[n] += 1

    # Fill each bucket in the original array
    i = 0
    for n in range(len(counts)):
        for j in range(counts[n]):
            arr[i] = n
            i += 1
    return arr


def counting_sort(arr, k):
    """General version: values are integers in 0..k inclusive."""
    counts = [0] * (k + 1)
    for n in arr:
        counts[n] += 1
    i = 0
    for v in range(k + 1):
        for _ in range(counts[v]):
            arr[i] = v
            i += 1
    return arr


# ---------------------------------------------------------------- Patterns (Python idioms)
def sort_by_freq_then_value(nums):
    # most frequent first; ties broken by smaller value first
    cnt = Counter(nums)
    return sorted(cnt, key=lambda x: (-cnt[x], x))


def top_k_frequent(nums, k):
    cnt = Counter(nums)
    return sorted(cnt, key=lambda x: -cnt[x])[:k]


def largest_number(nums):
    def compare(a, b):
        if a + b > b + a:
            return -1   # a should come first
        if a + b < b + a:
            return 1
        return 0
    strs = sorted(map(str, nums), key=cmp_to_key(compare))
    return "0" if strs[0] == "0" else "".join(strs)


def merge_intervals(intervals):
    intervals.sort(key=lambda iv: iv[0])
    out = []
    for start, end in intervals:
        if out and start <= out[-1][1]:
            out[-1][1] = max(out[-1][1], end)
        else:
            out.append([start, end])
    return out


def sort_colors(nums):
    # LeetCode 75: bucket sort idea, values only 0/1/2
    counts = [0, 0, 0]
    for n in nums:
        counts[n] += 1
    i = 0
    for v in range(3):
        for _ in range(counts[v]):
            nums[i] = v
            i += 1
    return nums


# ================================================================ TESTS
LESSON = {
    "insertion": [2, 3, 4, 1, 6],
    "merge": [3, 2, 4, 1, 6],
    "quick": [6, 2, 4, 1, 3],
    "bucket": [2, 1, 2, 0, 0, 2],
}
EDGE = [
    [],
    [5],
    [1, 1, 1, 1],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [2, 2, 1, 1, 0, 0],
    [3, -1, 0, -1, 3, 2],
]

# -- insertion sort
assert insertionSort([2, 3, 4, 1, 6]) == [1, 2, 3, 4, 6]
assert insertion_sort_py([2, 3, 4, 1, 6]) == [1, 2, 3, 4, 6]
for a in EDGE:
    assert insertionSort(list(a)) == sorted(a), a
    assert insertion_sort_py(list(a)) == sorted(a), a

# pass-by-pass trace used in the table
trace = insertion_sort_trace([2, 3, 4, 1, 6])
assert trace == [
    (1, 0, [2, 3, 4, 1, 6]),
    (2, 0, [2, 3, 4, 1, 6]),
    (3, 3, [1, 2, 3, 4, 6]),
    (4, 0, [1, 2, 3, 4, 6]),
], trace

# best case: already sorted -> zero swaps; worst case: reversed -> n(n-1)/2 swaps
assert sum(s for _, s, _ in insertion_sort_trace([1, 2, 3, 4, 5])) == 0
assert sum(s for _, s, _ in insertion_sort_trace([5, 4, 3, 2, 1])) == 10

# stability on [7,3,7]: tag each 7 so we can tell them apart, compare by value only
class Tagged:
    def __init__(self, v, tag):
        self.v, self.tag = v, tag
    def __lt__(self, o):
        return self.v < o.v
    def __le__(self, o):
        return self.v <= o.v
    def __repr__(self):
        return f"{self.v}{self.tag}"

t = insertionSort([Tagged(7, "a"), Tagged(3, ""), Tagged(7, "b")])
assert [repr(x) for x in t] == ["3", "7a", "7b"], t   # 7a still before 7b -> stable

# -- merge sort
assert mergeSort([3, 2, 4, 1, 6], 0, 4) == [1, 2, 3, 4, 6]
assert merge_sort_py([3, 2, 4, 1, 6]) == [1, 2, 3, 4, 6]
for a in EDGE:
    b = list(a)
    assert mergeSort(b, 0, len(b) - 1) == sorted(a), a
    assert merge_sort_py(list(a)) == sorted(a), a

# merge() alone on the two sorted halves of the lesson array
arr = [2, 3, 4, 1, 6]
merge(arr, 0, 2, 4)
assert arr == [1, 2, 3, 4, 6], arr

rows = merge_trace([2, 3, 4], [1, 6])
assert [r[0] for r in rows] == ["R[0]=1", "L[0]=2", "L[1]=3", "L[2]=4", "R[1]=6 (leftover)"], rows
assert rows[-1][4] == [1, 2, 3, 4, 6]

# merge sort stability
t = mergeSort([Tagged(7, "a"), Tagged(3, ""), Tagged(7, "b")], 0, 2)
assert [repr(x) for x in t] == ["3", "7a", "7b"]
# exhaustive stability check on small tagged inputs
def is_stable(sort_fn, n=5, trials=300):
    for _ in range(trials):
        vals = [random.randint(0, 2) for _ in range(n)]
        tagged = [Tagged(v, str(i)) for i, v in enumerate(vals)]
        out = sort_fn(tagged)
        for x, y in zip(out, out[1:]):
            if x.v == y.v and int(x.tag) > int(y.tag):
                return False
    return True
assert is_stable(lambda a: insertionSort(a))
assert is_stable(lambda a: mergeSort(a, 0, len(a) - 1))

# -- quick sort
assert quickSort([6, 2, 4, 1, 3], 0, 4) == [1, 2, 3, 4, 6]
for a in EDGE:
    b = list(a)
    assert quickSort(b, 0, len(b) - 1) == sorted(a), a
    b = list(a)
    assert quick_sort_random(b, 0, len(b) - 1) == sorted(a), a
for _ in range(200):
    a = [random.randint(-5, 5) for _ in range(random.randint(0, 12))]
    assert quickSort(list(a), 0, len(a) - 1) == sorted(a)
    assert quick_sort_random(list(a), 0, len(a) - 1) == sorted(a)
    assert mergeSort(list(a), 0, len(a) - 1) == sorted(a)
    assert insertionSort(list(a)) == sorted(a)

# partition trace on the lesson array, pivot = 3
arr = [6, 2, 4, 1, 3]
rows = partition_trace(arr, 0, 4)
assert [r[4] for r in rows] == [
    [6, 2, 4, 1, 3],   # i=0: 6 < 3? no
    [2, 6, 4, 1, 3],   # i=1: 2 < 3  swap(left=0, i=1), left -> 1
    [2, 6, 4, 1, 3],   # i=2: 4 < 3? no
    [2, 1, 4, 6, 3],   # i=3: 1 < 3  swap(left=1, i=3), left -> 2
    [2, 1, 3, 6, 4],   # pivot swap: arr[4] = arr[2], arr[2] = 3
], rows
assert rows[-1][3] == 2   # pivot lands at index 2

# quick sort instability: lesson example [7,3,7,4,5] pivot 5
arr = [Tagged(7, "a"), Tagged(3, ""), Tagged(7, "b"), Tagged(4, ""), Tagged(5, "")]
rows = partition_trace(arr, 0, 4)
# after the loop (before the pivot swap) the 7 from index 0 sits at index 3, behind the other 7
assert [repr(x) for x in rows[3][4]] == ["3", "4", "7b", "7a", "5"], rows[3]
# in this tiny example the final pivot swap moves 7b to the end again
assert [repr(x) for x in rows[4][4]] == ["3", "4", "5", "7a", "7b"], rows[4]

# find a short input where the FINAL output is out of order for equal keys
def first_unstable_quick():
    for n in range(3, 7):
        for vals in sorted(set(permutations([0, 1, 2, 2, 2, 1][:n]))):
            tagged = [Tagged(v, str(i)) for i, v in enumerate(vals)]
            out = quickSort(tagged, 0, n - 1)
            for x, y in zip(out, out[1:]):
                if x.v == y.v and int(x.tag) > int(y.tag):
                    return list(vals), [repr(t) for t in out]
    return None
unstable = first_unstable_quick()
assert unstable is not None
assert not is_stable(lambda a: quickSort(a, 0, len(a) - 1), n=6, trials=2000)
# the examples used on the page: the final pivot swap jumps over the other 7
arr = [Tagged(3, ""), Tagged(4, ""), Tagged(7, "a"), Tagged(7, "b")]
assert [repr(x) for x in quickSort(arr, 0, 3)] == ["3", "4", "7b", "7a"]
arr = [Tagged(2, "a"), Tagged(2, "b"), Tagged(0, ""), Tagged(2, "c"), Tagged(1, "")]
assert [repr(x) for x in quickSort(arr, 0, 4)] == ["0", "1", "2b", "2a", "2c"]

# worst case: sorted input, pivot always the max -> recursion depth n
def quick_depth(arr, s, e, d=0):
    if e - s + 1 <= 1:
        return d
    pivot = arr[e]; left = s
    for i in range(s, e):
        if arr[i] < pivot:
            arr[left], arr[i] = arr[i], arr[left]; left += 1
    arr[e], arr[left] = arr[left], arr[e]
    return max(quick_depth(arr, s, left - 1, d + 1), quick_depth(arr, left + 1, e, d + 1))
assert quick_depth([1, 2, 3, 4, 5, 6, 7, 8], 0, 7) == 7      # height n-1 on sorted input
assert quick_depth([4, 2, 6, 1, 3, 5, 7, 8], 0, 7) <= 7

# -- bucket sort
assert bucketSort([2, 1, 2, 0, 0, 2]) == [0, 0, 1, 2, 2, 2]
assert bucketSort([]) == []
assert bucketSort([1]) == [1]
assert bucketSort([2, 2, 2]) == [2, 2, 2]
assert bucketSort([0, 0, 1, 2]) == [0, 0, 1, 2]
assert bucketSort([2, 1, 0]) == [0, 1, 2]
cnt = [0, 0, 0]
for n in [2, 1, 2, 0, 0, 2]:
    cnt[n] += 1
assert cnt == [2, 1, 3]
assert sum(cnt) == 6      # total writes == n, so the nested loop is O(n)

assert counting_sort([4, 1, 3, 1, 0, 4], 4) == [0, 1, 1, 3, 4, 4]
assert counting_sort([], 3) == []
assert counting_sort([3, 3, 3], 3) == [3, 3, 3]

# -- Python idioms
a = [3, 1, 2]
assert sorted(a) == [1, 2, 3] and a == [3, 1, 2]            # sorted() returns a new list
a.sort(); assert a == [1, 2, 3]                              # list.sort() is in place, returns None
assert sorted([3, 1, 2], reverse=True) == [3, 2, 1]
words = ["banana", "fig", "apple", "kiwi"]
assert sorted(words, key=len) == ["fig", "kiwi", "apple", "banana"]
# stability with key: "peach" and "grape" both length 5, keep input order
assert sorted(["peach", "fig", "grape"], key=len) == ["fig", "peach", "grape"]
pairs = [(2, "b"), (1, "z"), (2, "a")]
assert sorted(pairs) == [(1, "z"), (2, "a"), (2, "b")]      # tuples compare element by element
assert sorted(pairs, key=lambda p: p[0]) == [(1, "z"), (2, "b"), (2, "a")]  # stable on ties
assert sorted(pairs, key=lambda p: (-p[0], p[1])) == [(2, "a"), (2, "b"), (1, "z")]

assert sort_by_freq_then_value([1, 1, 1, 2, 2, 3]) == [1, 2, 3]
assert sort_by_freq_then_value([3, 3, 1, 1, 2]) == [1, 3, 2]
assert set(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == {1, 2}
assert largest_number([10, 2]) == "210"
assert largest_number([3, 30, 34, 5, 9]) == "9534330"
assert largest_number([0, 0]) == "0"
assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 3 + 3], [8, 10], [15, 18]]
assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
assert sort_colors([2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2]

# Timsort in CPython is stable
class Rec:
    def __init__(self, k, tag): self.k, self.tag = k, tag
recs = [Rec(1, "x"), Rec(0, "y"), Rec(1, "z")]
assert [r.tag for r in sorted(recs, key=lambda r: r.k)] == ["y", "x", "z"]

print("all checks passed")
print("unstable quick sort example found by search:", unstable)
