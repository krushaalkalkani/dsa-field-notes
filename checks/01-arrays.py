# Checks for site/topics/01-arrays.html
# Every function / class shown on the page lives here and is tested on the
# lesson's own examples. Run: python3 checks/01-arrays.py

# ============================ Lesson 1: RAM ============================

# Integers in binary, one byte each (lesson: 1 = 00000001, 3 = 00000011, 5 = 00000101)
assert format(1, "08b") == "00000001"
assert format(3, "08b") == "00000011"
assert format(5, "08b") == "00000101"
assert bin(5) == "0b101"

# A byte is 8 bits; 8 GB of RAM = 8 * 1024^3 bytes
assert 8 * 1024 ** 3 == 8_589_934_592


def address_of(start, i, size):
    """Address of element i when each element takes `size` bytes."""
    return start + i * size


# int array [1, 3, 5]: 4 bytes each -> $0, $4, $8
assert [address_of(0, i, 4) for i in range(3)] == [0, 4, 8]
# char array ['a', 'b', 'c']: 1 byte each -> $0, $1, $2
assert [address_of(0, i, 1) for i in range(3)] == [0, 1, 2]
# starting somewhere else in RAM still works
assert address_of(100, 2, 4) == 108


# ============================ Lesson 2: Static arrays ============================

myArray = [1, 3, 5]
assert myArray[0] == 1
assert myArray[2] == 5
i = 1
assert myArray[i] == 3

# traversing, both forms from the lesson
seen = []
for i in range(len(myArray)):
    seen.append(myArray[i])
assert seen == [1, 3, 5]

seen = []
i = 0
while i < len(myArray):
    seen.append(myArray[i])
    i += 1
assert seen == [1, 3, 5]

# last index is n - 1
assert len(myArray) - 1 == 2
assert myArray[len(myArray) - 1] == 5


# Remove from the last position in the array if the array
# is not empty (i.e. length is non-zero).
def removeEnd(arr, length):
    if length > 0:
        # Overwrite last element with some default value.
        # We would also consider the length to be decreased by 1.
        arr[length - 1] = 0


arr = [4, 5, 6]
removeEnd(arr, 3)
assert arr == [4, 5, 0], arr
removeEnd(arr, 0)          # empty array: nothing happens
assert arr == [4, 5, 0], arr

# a version that also returns the new length (what the lesson says "we would consider")
def removeEnd2(arr, length):
    if length > 0:
        arr[length - 1] = 0
        length -= 1
    return length


arr = [4, 5, 6]
assert removeEnd2(arr, 3) == 2 and arr == [4, 5, 0]
assert removeEnd2(arr, 0) == 0


# Remove value at index i before shifting elements to the left.
# Assuming i is a valid index.
def removeMiddle(arr, i, length):
    # Shift starting from i + 1 to end.
    for index in range(i + 1, length):
        arr[index - 1] = arr[index]
    # No need to 'remove' arr[i], since we already shifted


arr = [4, 5, 6, 7, 8]
removeMiddle(arr, 1, 5)
assert arr == [4, 6, 7, 8, 8], arr          # old last slot still holds 8 (stale)
arr = [4, 5, 6, 7, 8]
removeMiddle(arr, 0, 5)                     # worst case: every element shifts
assert arr == [5, 6, 7, 8, 8], arr
arr = [4, 5, 6, 7, 8]
removeMiddle(arr, 4, 5)                     # last index: loop body never runs
assert arr == [4, 5, 6, 7, 8], arr

# trace of removeMiddle([4,5,6,7,8], 1, 5) step by step
arr = [4, 5, 6, 7, 8]
trace = []
for index in range(2, 5):
    arr[index - 1] = arr[index]
    trace.append(list(arr))
assert trace == [[4, 6, 6, 7, 8], [4, 6, 7, 7, 8], [4, 6, 7, 8, 8]], trace


# Insert n into arr at the next open position.
# Length is the number of 'real' values in arr, and capacity
# is the size (aka memory allocated for the fixed size array).
def insertEnd(arr, n, length, capacity):
    if length < capacity:
        arr[length] = n


arr = [4, 5, 0, 0]          # length 2, capacity 4
insertEnd(arr, 6, 2, 4)
assert arr == [4, 5, 6, 0], arr
insertEnd(arr, 7, 3, 4)
assert arr == [4, 5, 6, 7], arr
insertEnd(arr, 8, 4, 4)     # full: nothing happens
assert arr == [4, 5, 6, 7], arr


# Insert n into index i after shifting elements to the right.
# Assuming i is a valid index and arr is not full.
def insertMiddle(arr, i, n, length):
    # Shift starting from the end to i.
    for index in range(length - 1, i - 1, -1):
        arr[index + 1] = arr[index]
    # Insert at i
    arr[i] = n


# with spare capacity: [4, 5, 6, _] insert 8 at index 1
arr = [4, 5, 6, 0]
insertMiddle(arr, 1, 8, 3)
assert arr == [4, 8, 5, 6], arr
# insert at index 0 (worst case, every element shifts)
arr = [4, 5, 6, 0]
insertMiddle(arr, 0, 8, 3)
assert arr == [8, 4, 5, 6], arr

# trace of the shifting loop for [4,5,6,_], i=1, length=3: index goes 2, 1
arr = [4, 5, 6, 0]
trace = []
for index in range(2, 0, -1):
    arr[index + 1] = arr[index]
    trace.append(list(arr))
assert trace == [[4, 5, 6, 6], [4, 5, 5, 6]], trace
arr[1] = 8
assert arr == [4, 8, 5, 6]


# lesson example: no spare capacity -> the last element 6 falls off
def insertMiddleFull(arr, i, n, length):
    """Same as insertMiddle but when the array is full (length == capacity)
    the last value is lost: we can only shift up to index length-1."""
    for index in range(length - 2, i - 1, -1):
        arr[index + 1] = arr[index]
    arr[i] = n


arr = [4, 5, 6]
insertMiddleFull(arr, 1, 8, 3)
assert arr == [4, 8, 5], arr                # 6 is gone

# Python's own list does the shifting for you (still O(n))
lst = [4, 5, 6]
lst.insert(1, 8)
assert lst == [4, 8, 5, 6]
lst.pop(1)
assert lst == [4, 5, 6]
lst.pop()                   # end: O(1)
assert lst == [4, 5]
del lst[0]                  # shift left, O(n)
assert lst == [5]
lst.append(9)
assert lst == [5, 9]


# ============================ Lesson 3: Dynamic arrays ============================

class DynamicArray:
    def __init__(self, capacity=1):
        self.capacity = capacity
        self.length = 0
        self.arr = [0] * capacity
        self.resizes = 0            # for the notes only: how many times we copied

    def get(self, i):
        return self.arr[i]

    def set(self, i, n):
        self.arr[i] = n

    # Insert n in the last position of the array
    def pushback(self, n):
        if self.length == self.capacity:
            self.resize()
        # insert at next empty position
        self.arr[self.length] = n
        self.length += 1

    def popback(self):
        if self.length > 0:
            self.length -= 1
        return self.arr[self.length]

    def resize(self):
        # Create new array of double capacity
        self.capacity = 2 * self.capacity
        newArr = [0] * self.capacity
        # Copy elements to newArr
        for i in range(self.length):
            newArr[i] = self.arr[i]
        self.arr = newArr
        self.resizes += 1

    def getSize(self):
        return self.length

    def getCapacity(self):
        return self.capacity


d = DynamicArray(3)
for v in [1, 3, 5]:
    d.pushback(v)
assert d.getSize() == 3 and d.getCapacity() == 3
d.pushback(7)                       # full -> resize 3 -> 6, then insert
assert d.getCapacity() == 6 and d.getSize() == 4
assert d.arr[:4] == [1, 3, 5, 7] and d.get(3) == 7
d.set(0, 9)
assert d.get(0) == 9
assert d.popback() == 7 and d.getSize() == 3
assert d.resizes == 1

# capacity growth from 1: 1 -> 2 -> 4 -> 8 while pushing 8 values
d = DynamicArray(1)
caps = []
for v in range(8):
    d.pushback(v)
    caps.append(d.getCapacity())
assert caps == [1, 2, 4, 4, 8, 8, 8, 8], caps   # resize fires on pushes 2, 3, 5
assert d.resizes == 3
assert [d.get(i) for i in range(8)] == [0, 1, 2, 3, 4, 5, 6, 7]

# empty popback does not crash
e = DynamicArray()
assert e.popback() == 0 and e.getSize() == 0


# Why double? Cost of building a size-8 array from size 1.
def build_cost(n):
    """Count every write (inserts + copies during resizes) while pushing n items,
    starting from capacity 1 and doubling."""
    cap, length, writes = 1, 0, 0
    for _ in range(n):
        if length == cap:
            writes += length        # copy every existing element
            cap *= 2
        writes += 1                 # the insert itself
        length += 1
    return writes


# lesson: 1 + 2 + 4 + 8 = 15 operations for a size-8 array
assert 1 + 2 + 4 + 8 == 15
assert build_cost(8) == 8 + (1 + 2 + 4) == 15
# last term >= sum of everything before it
assert 1 + 2 + 4 == 7 and 7 < 8
# lesson claim: for array size n (n = final capacity, a power of two) at most 2n operations
for n in [1, 2, 4, 8, 16, 1024]:
    assert build_cost(n) == 2 * n - 1, (n, build_cost(n))
    assert build_cost(n) <= 2 * n
# for any n the copies total capacity-1 < 2n, so total work < 3n: still O(n)
for n in [3, 5, 7, 9, 100, 1000]:
    assert build_cost(n) < 3 * n, (n, build_cost(n))
assert build_cost(5) == 12          # 5 inserts + copies of 1 + 2 + 4

# per-insert cost: mostly 1, occasionally big
costs = []
cap, length = 1, 0
for _ in range(8):
    c = 1
    if length == cap:
        c += length
        cap *= 2
    costs.append(c)
    length += 1
assert costs == [1, 2, 3, 1, 5, 1, 1, 1], costs
assert sum(costs) == 15

# Python's built-in list is a dynamic array
lst = []
for v in range(8):
    lst.append(v)
assert lst == [0, 1, 2, 3, 4, 5, 6, 7]


# ============================ Lesson 4: Stacks ============================

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, n):
        # using the pushback function from dynamic arrays to add to the stack
        self.stack.append(n)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def isEmpty(self):
        return len(self.stack) == 0


s = Stack()
assert s.isEmpty()
for v in [1, 2, 3, 4]:
    s.push(v)
assert s.stack == [1, 2, 3, 4]
assert s.peek() == 4 and s.stack == [1, 2, 3, 4]      # peek does not remove
assert s.pop() == 4
assert s.pop() == 3
assert s.peek() == 2
assert not s.isEmpty()
assert s.pop() == 2 and s.pop() == 1
assert s.isEmpty()

# popping an empty stack raises -> always check first
try:
    s.pop()
    raised = False
except IndexError:
    raised = True
assert raised


def safe_pop(stack):
    if not stack:
        return None
    return stack.pop()


assert safe_pop([]) is None
assert safe_pop([7]) == 7


# a stack reverses a sequence
def reverse_string(s):
    stack = []
    for ch in s:
        stack.append(ch)
    out = []
    while stack:
        out.append(stack.pop())
    return "".join(out)


assert reverse_string("abc") == "cba"
assert reverse_string("") == ""
assert reverse_string("neet") == "teen"


# ============================ Patterns ============================

# Move 1: two pointers (slow writer, fast reader) - LC 26 Remove Duplicates from Sorted Array
def removeDuplicates(nums):
    if not nums:
        return 0
    L = 0                               # index of the last unique value written
    for R in range(1, len(nums)):
        if nums[R] != nums[L]:
            L += 1
            nums[L] = nums[R]
    return L + 1


nums = [1, 1, 2]
assert removeDuplicates(nums) == 2 and nums[:2] == [1, 2]
nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
assert removeDuplicates(nums) == 5 and nums[:5] == [0, 1, 2, 3, 4]
assert removeDuplicates([]) == 0


# two pointers from both ends: reverse in place
def reverse_in_place(arr):
    L, R = 0, len(arr) - 1
    while L < R:
        arr[L], arr[R] = arr[R], arr[L]
        L += 1
        R -= 1
    return arr


assert reverse_in_place([1, 3, 5]) == [5, 3, 1]
assert reverse_in_place([1, 2, 3, 4]) == [4, 3, 2, 1]
assert reverse_in_place([]) == []


# Move 2: sliding window - LC 121 Best Time to Buy and Sell Stock
def maxProfit(prices):
    L, best = 0, 0                      # L = cheapest day so far
    for R in range(1, len(prices)):
        if prices[R] < prices[L]:
            L = R                       # found a cheaper buy day: slide the window start
        else:
            best = max(best, prices[R] - prices[L])
    return best


assert maxProfit([7, 1, 5, 3, 6, 4]) == 5
assert maxProfit([7, 6, 4, 3, 1]) == 0
assert maxProfit([1]) == 0


# fixed-size window: max sum of any k neighbors
def max_sum_window(arr, k):
    window = sum(arr[:k])
    best = window
    for R in range(k, len(arr)):
        window += arr[R] - arr[R - k]   # add the new right cell, drop the old left cell
        best = max(best, window)
    return best


assert max_sum_window([2, 1, 5, 1, 3, 2], 3) == 9
assert max_sum_window([1, 3, 5], 1) == 5
assert max_sum_window([1, 3, 5], 3) == 9


# Move 3: prefix sum - LC 303 Range Sum Query
class NumArray:
    def __init__(self, nums):
        self.prefix = [0]
        for n in nums:
            self.prefix.append(self.prefix[-1] + n)

    def sumRange(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]


na = NumArray([-2, 0, 3, -5, 2, -1])
assert na.prefix == [0, -2, -2, 1, -4, -2, -3]
assert na.sumRange(0, 2) == 1
assert na.sumRange(2, 5) == -1
assert na.sumRange(0, 5) == -3


# Move 4: stack for matching - LC 20 Valid Parentheses
def isValid(s):
    stack = []
    close_to_open = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in close_to_open:                     # a closing bracket
            if stack and stack[-1] == close_to_open[ch]:
                stack.pop()
            else:
                return False
        else:                                       # an opening bracket
            stack.append(ch)
    return not stack


assert isValid("()") is True
assert isValid("()[]{}") is True
assert isValid("(]") is False
assert isValid("([)]") is False
assert isValid("{[]}") is True
assert isValid("(") is False
assert isValid(")") is False
assert isValid("") is True


# Move 4b: stack that also answers "what is the minimum?" - LC 155 Min Stack
class MinStack:
    def __init__(self):
        self.stack = []
        self.minStack = []          # minStack[-1] is the min of everything in stack

    def push(self, val):
        self.stack.append(val)
        val = min(val, self.minStack[-1] if self.minStack else val)
        self.minStack.append(val)

    def pop(self):
        self.stack.pop()
        self.minStack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.minStack[-1]


ms = MinStack()
ms.push(-2)
ms.push(0)
ms.push(-3)
assert ms.getMin() == -3
ms.pop()
assert ms.top() == 0
assert ms.getMin() == -2


# Practice sanity: LC 1929 Concatenation of Array, LC 27 Remove Element, LC 283 Move Zeroes
def getConcatenation(nums):
    return nums + nums


assert getConcatenation([1, 2, 1]) == [1, 2, 1, 1, 2, 1]


def removeElement(nums, val):
    k = 0
    for i in range(len(nums)):
        if nums[i] != val:
            nums[k] = nums[i]
            k += 1
    return k


nums = [3, 2, 2, 3]
assert removeElement(nums, 3) == 2 and sorted(nums[:2]) == [2, 2]
nums = [0, 1, 2, 2, 3, 0, 4, 2]
assert removeElement(nums, 2) == 5 and sorted(nums[:5]) == [0, 0, 1, 3, 4]


def moveZeroes(nums):
    L = 0
    for R in range(len(nums)):
        if nums[R] != 0:
            nums[L], nums[R] = nums[R], nums[L]
            L += 1
    return nums


assert moveZeroes([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]
assert moveZeroes([0]) == [0]


# LC 682 Baseball Game: a stack that reads back
def calPoints(operations):
    stack = []
    for op in operations:
        if op == "+":
            stack.append(stack[-1] + stack[-2])
        elif op == "D":
            stack.append(2 * stack[-1])
        elif op == "C":
            stack.pop()
        else:
            stack.append(int(op))
    return sum(stack)


assert calPoints(["5", "2", "C", "D", "+"]) == 30
assert calPoints(["5", "-2", "4", "C", "D", "9", "+", "+"]) == 27
assert calPoints(["1", "C"]) == 0

print("all checks passed")
