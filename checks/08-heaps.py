# Checks for site/topics/08-heaps.html
# Every class / function that appears on the page is here, tested on the
# lesson's own example heap [14,19,16,21,26,19,68,65,30].

import heapq
from collections import Counter

# ---------------------------------------------------------------- lesson 23
class Heap:
    def __init__(self):
        self.heap = [0]          # index 0 holds a dummy value

    # ------------------------------------------------------------ lesson 24
    def push(self, val):
        self.heap.append(val)
        i = len(self.heap) - 1

        # Percolate up
        while i > 1 and self.heap[i] < self.heap[i // 2]:
            tmp = self.heap[i]
            self.heap[i] = self.heap[i // 2]
            self.heap[i // 2] = tmp
            i = i // 2

    def pop(self):
        if len(self.heap) == 1:
            return None
        if len(self.heap) == 2:
            return self.heap.pop()

        res = self.heap[1]
        # Move last value to root
        self.heap[1] = self.heap.pop()
        i = 1
        # Percolate down
        while 2 * i < len(self.heap):
            if (2 * i + 1 < len(self.heap) and
                self.heap[2 * i + 1] < self.heap[2 * i] and
                self.heap[i] > self.heap[2 * i + 1]):
                # Swap right child
                tmp = self.heap[i]
                self.heap[i] = self.heap[2 * i + 1]
                self.heap[2 * i + 1] = tmp
                i = 2 * i + 1
            elif self.heap[i] > self.heap[2 * i]:
                # Swap left child
                tmp = self.heap[i]
                self.heap[i] = self.heap[2 * i]
                self.heap[2 * i] = tmp
                i = 2 * i
            else:
                break
        return res

    # ------------------------------------------------------------ lesson 25
    def heapify(self, arr):
        # 0-th position is moved to the end
        arr.append(arr[0])

        self.heap = arr
        cur = (len(self.heap) - 1) // 2
        while cur > 0:
            # Percolate down
            i = cur
            while 2 * i < len(self.heap):
                if (2 * i + 1 < len(self.heap) and
                    self.heap[2 * i + 1] < self.heap[2 * i] and
                    self.heap[i] > self.heap[2 * i + 1]):
                    # Swap right child
                    tmp = self.heap[i]
                    self.heap[i] = self.heap[2 * i + 1]
                    self.heap[2 * i + 1] = tmp
                    i = 2 * i + 1
                elif self.heap[i] > self.heap[2 * i]:
                    # Swap left child
                    tmp = self.heap[i]
                    self.heap[i] = self.heap[2 * i]
                    self.heap[2 * i] = tmp
                    i = 2 * i
                else:
                    break
            cur -= 1


def is_min_heap(h):
    """h is 1-indexed (h[0] is the dummy). Every child >= its parent."""
    for i in range(2, len(h)):
        if h[i] < h[i // 2]:
            return False
    return True


# --- index formulas (1-indexed) on node 19 at index 2 ---
LESSON = [14, 19, 16, 21, 26, 19, 68, 65, 30]
h1 = [0] + LESSON
i = 2
assert h1[i] == 19
assert h1[2 * i] == 21          # left child at index 4
assert h1[2 * i + 1] == 26      # right child at index 5
assert h1[i // 2] == 14         # parent at index 1
assert is_min_heap(h1)

# --- push(17): three percolate-up steps, array after each swap ---
hp = Heap()
hp.heap = [0] + LESSON[:]
hp.push(17)
assert hp.heap == [0, 14, 17, 16, 21, 19, 19, 68, 65, 30, 26], hp.heap
assert is_min_heap(hp.heap)

# manual re-trace of the same push, recording the array after each swap
trace = []
h = [0] + LESSON[:]
h.append(17)
trace.append(h[:])                          # after append: 17 at index 10
i = len(h) - 1
while i > 1 and h[i] < h[i // 2]:
    h[i], h[i // 2] = h[i // 2], h[i]
    i //= 2
    trace.append(h[:])
assert trace == [
    [0, 14, 19, 16, 21, 26, 19, 68, 65, 30, 17],   # appended at 10
    [0, 14, 19, 16, 21, 17, 19, 68, 65, 30, 26],   # swap with 26 (idx 5)
    [0, 14, 17, 16, 21, 19, 19, 68, 65, 30, 26],   # swap with 19 (idx 2)
], trace
assert i == 2 and h[1] == 14                       # stopped under 14

# --- pop(): 30 to root, then swap with 16, then with 19 ---
hp = Heap()
hp.heap = [0] + LESSON[:]
assert hp.pop() == 14
assert hp.heap == [0, 16, 19, 19, 21, 26, 30, 68, 65], hp.heap
assert is_min_heap(hp.heap)

# manual re-trace of pop, recording the array after each swap
h = [0] + LESSON[:]
res = h[1]
h[1] = h.pop()
trace = [h[:]]                                     # 30 moved to root
i = 1
while 2 * i < len(h):
    if 2 * i + 1 < len(h) and h[2 * i + 1] < h[2 * i] and h[i] > h[2 * i + 1]:
        h[i], h[2 * i + 1] = h[2 * i + 1], h[i]
        i = 2 * i + 1
    elif h[i] > h[2 * i]:
        h[i], h[2 * i] = h[2 * i], h[i]
        i = 2 * i
    else:
        break
    trace.append(h[:])
assert res == 14
assert trace == [
    [0, 30, 19, 16, 21, 26, 19, 68, 65],   # last element 30 moved to root
    [0, 16, 19, 30, 21, 26, 19, 68, 65],   # swap with right child 16 (idx 3)
    [0, 16, 19, 19, 21, 26, 30, 68, 65],   # swap with left child 19 (idx 6)
], trace

# edge cases of pop
hp = Heap()
assert hp.pop() is None                    # empty heap
hp.push(5)
assert hp.pop() == 5 and hp.heap == [0]    # one element, no percolation

# pop everything: comes out sorted
hp = Heap()
for v in LESSON:
    hp.push(v)
out = [hp.pop() for _ in range(len(LESSON))]
assert out == sorted(LESSON), out
assert hp.pop() is None

# --- heapify on an unsorted list ---
arr = [68, 30, 65, 21, 19, 14, 26, 16, 19]
hp = Heap()
hp.heapify(arr)
assert hp.heap[0] == 68                    # stale copy at index 0 is ignored
assert hp.heap[-1] == 68                   # the real 68 now lives at the end
assert hp.heap[1:] == [14, 19, 16, 19, 65, 26, 21, 30, 68], hp.heap
assert is_min_heap(hp.heap)
assert sorted(hp.heap[1:]) == sorted([68, 30, 65, 21, 19, 14, 26, 16, 19])
assert (len(hp.heap) - 1) // 2 == 4        # first non-leaf is index 4 = n // 2

# manual re-trace of heapify: state after each cur finishes
h = [68, 30, 65, 21, 19, 14, 26, 16, 19]
h.append(h[0])
states = {}
cur = (len(h) - 1) // 2
while cur > 0:
    i = cur
    while 2 * i < len(h):
        if 2 * i + 1 < len(h) and h[2 * i + 1] < h[2 * i] and h[i] > h[2 * i + 1]:
            h[i], h[2 * i + 1] = h[2 * i + 1], h[i]
            i = 2 * i + 1
        elif h[i] > h[2 * i]:
            h[i], h[2 * i] = h[2 * i], h[i]
            i = 2 * i
        else:
            break
    states[cur] = h[1:]
    cur -= 1
assert states[4] == [30, 65, 21, 19, 14, 26, 16, 19, 68]    # 19 vs (19,68): no swap
assert states[3] == [30, 65, 16, 19, 14, 26, 21, 19, 68]    # 21 <-> 16
assert states[2] == [30, 14, 16, 19, 65, 26, 21, 19, 68]    # 65 <-> 14
assert states[1] == [14, 19, 16, 19, 65, 26, 21, 30, 68]    # 30 sinks 3 levels

# heapify on the lesson heap itself changes nothing (already valid)
hp = Heap()
hp.heapify(LESSON[:])
assert hp.heap[1:] == [19, 16, 21, 26, 19, 68, 65, 30, 14] or is_min_heap(hp.heap)
# (the first element moved to the end, so the layout differs, but it is a heap)
assert is_min_heap(hp.heap)

# pop from heapified heap gives sorted order
hp = Heap()
hp.heapify([68, 30, 65, 21, 19, 14, 26, 16, 19])
out = [hp.pop() for _ in range(9)]
assert out == [14, 16, 19, 19, 21, 26, 30, 65, 68]

# --- O(n) heapify: the "work halves per level" sum ---
# For a perfect tree of height H with n = 2^(H+1) - 1 nodes, total percolate
# distance = sum over levels of (nodes at that level * levels below it) < n.
for H in range(1, 12):
    n = 2 ** (H + 1) - 1
    work = sum((2 ** lvl) * (H - lvl) for lvl in range(H + 1))
    assert work < n, (H, n, work)
    leaves = 2 ** H
    assert leaves == (n + 1) // 2          # about n/2 leaves

# ---------------------------------------------------------------- heapq
# 0-indexed: children 2i+1, 2i+2, parent (i-1)//2
hq = LESSON[:]
heapq.heapify(hq)
assert hq[0] == 14
for i in range(1, len(hq)):
    assert hq[i] >= hq[(i - 1) // 2]

heapq.heappush(hq, 17)
assert hq[0] == 14
assert heapq.heappop(hq) == 14
assert hq[0] == 16

# pop order equals sorted order
hq = LESSON[:]
heapq.heapify(hq)
assert [heapq.heappop(hq) for _ in range(len(hq))] == sorted(LESSON)

# our Heap and heapq agree on every pop
mine = Heap()
mine.heapify([68, 30, 65, 21, 19, 14, 26, 16, 19])
theirs = [68, 30, 65, 21, 19, 14, 26, 16, 19]
heapq.heapify(theirs)
for _ in range(9):
    assert mine.pop() == heapq.heappop(theirs)

# heappushpop / heapreplace
hq = [1, 3, 5]
assert heapq.heappushpop(hq, 0) == 0 and hq == [1, 3, 5]     # push then pop
assert heapq.heapreplace(hq, 0) == 1 and hq[0] == 0          # pop then push

# nlargest / nsmallest
nums = [5, 1, 9, 3, 7]
assert heapq.nlargest(2, nums) == [9, 7]
assert heapq.nsmallest(2, nums) == [1, 3]
words = ["kiwi", "fig", "banana"]
assert heapq.nsmallest(1, words, key=len) == ["fig"]

# max-heap via negation
maxh = []
for v in [3, 10, 7]:
    heapq.heappush(maxh, -v)
assert -maxh[0] == 10
assert -heapq.heappop(maxh) == 10
assert -heapq.heappop(maxh) == 7


def lastStoneWeight(stones):
    heap = [-s for s in stones]
    heapq.heapify(heap)
    while len(heap) > 1:
        first = -heapq.heappop(heap)          # heaviest
        second = -heapq.heappop(heap)         # second heaviest
        if first != second:
            heapq.heappush(heap, -(first - second))
    return -heap[0] if heap else 0


assert lastStoneWeight([2, 7, 4, 1, 8, 1]) == 1
assert lastStoneWeight([1]) == 1
assert lastStoneWeight([2, 2]) == 0

# tuples: priority first, tie-breaker second
tasks = []
heapq.heappush(tasks, (2, 1, "write tests"))
heapq.heappush(tasks, (1, 2, "fix bug"))
heapq.heappush(tasks, (1, 0, "answer pager"))
assert heapq.heappop(tasks) == (1, 0, "answer pager")
assert heapq.heappop(tasks) == (1, 2, "fix bug")
assert heapq.heappop(tasks) == (2, 1, "write tests")

# tuple with an unorderable payload needs a tie-breaker
class Job:
    def __init__(self, name):
        self.name = name

bad = []
heapq.heappush(bad, (1, Job("a")))
try:
    heapq.heappush(bad, (1, Job("b")))
    raised = False
except TypeError:
    raised = True
assert raised

good = []
heapq.heappush(good, (1, 0, Job("a")))
heapq.heappush(good, (1, 1, Job("b")))      # counter breaks the tie
assert heapq.heappop(good)[2].name == "a"

# ---------------------------------------------------------------- patterns
# Move 1: top-K with a size-k heap (LC 215 / 703 / 973 / 347)
def findKthLargest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)          # throw away the smallest
    return heap[0]                       # k-th largest sits at the root


assert findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5
assert findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4


class KthLargest:                        # LC 703
    def __init__(self, k, nums):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val):
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]


kl = KthLargest(3, [4, 5, 8, 2])
assert kl.add(3) == 4
assert kl.add(5) == 5
assert kl.add(10) == 5
assert kl.add(9) == 8
assert kl.add(4) == 8


def kClosest(points, k):                 # LC 973
    heap = []
    for x, y in points:
        d = x * x + y * y
        heapq.heappush(heap, (-d, x, y))     # max-heap on distance
        if len(heap) > k:
            heapq.heappop(heap)              # drop the farthest
    return [[x, y] for _, x, y in heap]


assert sorted(kClosest([[1, 3], [-2, 2]], 1)) == [[-2, 2]]
assert sorted(kClosest([[3, 3], [5, -1], [-2, 4]], 2)) == [[-2, 4], [3, 3]]


def topKFrequent(nums, k):               # LC 347
    count = Counter(nums)
    return [x for x, _ in heapq.nlargest(k, count.items(), key=lambda p: p[1])]


assert sorted(topKFrequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
assert topKFrequent([1], 1) == [1]


# Move 2: k-way merge (LC 23 on plain lists)
def mergeKSorted(lists):
    heap = []
    for li, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], li, 0))    # (value, which list, index)
    out = []
    while heap:
        val, li, j = heapq.heappop(heap)
        out.append(val)
        if j + 1 < len(lists[li]):
            heapq.heappush(heap, (lists[li][j + 1], li, j + 1))
    return out


assert mergeKSorted([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
assert mergeKSorted([]) == []
assert mergeKSorted([[]]) == []


# Move 3: two heaps for a running median (LC 295)
class MedianFinder:
    def __init__(self):
        self.small = []      # max-heap (negated): lower half
        self.large = []      # min-heap: upper half

    def addNum(self, num):
        heapq.heappush(self.small, -num)
        # every element of small must be <= every element of large
        if self.large and -self.small[0] > self.large[0]:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        # sizes may differ by at most 1
        if len(self.small) > len(self.large) + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small) + 1:
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        if len(self.large) > len(self.small):
            return self.large[0]
        return (-self.small[0] + self.large[0]) / 2


mf = MedianFinder()
mf.addNum(1)
mf.addNum(2)
assert mf.findMedian() == 1.5
mf.addNum(3)
assert mf.findMedian() == 2
mf.addNum(10)
mf.addNum(-5)
assert mf.findMedian() == 2                  # sorted: -5 1 2 3 10
import random
random.seed(8)
mf = MedianFinder()
seen = []
for _ in range(200):
    v = random.randint(-50, 50)
    mf.addNum(v)
    seen.append(v)
    s = sorted(seen)
    m = len(s)
    expect = s[m // 2] if m % 2 else (s[m // 2 - 1] + s[m // 2]) / 2
    assert mf.findMedian() == expect

# Move 4: heap vs sorting - k smallest of a big list, both ways agree
big = [random.randint(0, 10 ** 6) for _ in range(5000)]
assert heapq.nsmallest(5, big) == sorted(big)[:5]

# ---------------------------------------------------------------- quiz traces
# Q: push 12 onto the lesson heap
hp = Heap()
hp.heap = [0] + LESSON[:]
hp.push(12)
assert hp.heap == [0, 12, 14, 16, 21, 19, 19, 68, 65, 30, 26], hp.heap

# Q: two pops from the lesson heap
hp = Heap()
hp.heap = [0] + LESSON[:]
assert hp.pop() == 14 and hp.pop() == 16
# after pop 1: [0,16,19,19,21,26,30,68,65]; pop 2 moves 65 to the root,
# ties (19 vs 19) go LEFT, then 65 vs (21,26) goes left again
assert hp.heap == [0, 19, 21, 19, 65, 26, 30, 68], hp.heap

print("all checks passed")
