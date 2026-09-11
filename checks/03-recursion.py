# Every function on site/topics/03-recursion.html lives here and is tested
# against the lesson's own examples (5! = 120, fib(5) = 5, fib(4) = 3, ...).
import sys


# --- Lesson 8: factorial, one-branch recursion (NeetCode version) ---
def factorial(n):
    # Base case: n = 0 or 1
    if n <= 1:
        return 1
    # Recursive case: n! = n * (n - 1)!
    return n * factorial(n - 1)


assert factorial(5) == 120
assert factorial(4) == 24
assert factorial(3) == 6
assert factorial(2) == 2
assert factorial(1) == 1
assert factorial(0) == 1
assert factorial(5) == 5 * 4 * 3 * 2 * 1


# --- traced factorial: prints the way down and the way up ---
log = []


def factorial_traced(n, depth=0):
    pad = "    " * depth
    log.append(f"{pad}factorial({n}) called")
    if n <= 1:
        log.append(f"{pad}base case -> return 1")
        return 1
    sub = factorial_traced(n - 1, depth + 1)   # wait here until the smaller call returns
    log.append(f"{pad}factorial({n}) = {n} * {sub} = {n * sub}")
    return n * sub


assert factorial_traced(5) == 120
assert log[0] == "factorial(5) called"
assert log[4] == "                factorial(1) called"
assert log[5] == "                base case -> return 1"
assert log[6] == "            factorial(2) = 2 * 1 = 2"
assert log[-1] == "factorial(5) = 5 * 24 = 120"
assert len(log) == 10, len(log)   # 5 "called" lines + 1 base + 4 multiply lines


# --- no base case -> RecursionError (Python's name for stack overflow) ---
def no_base_case(n):
    return n * no_base_case(n - 1)      # never stops: n goes 5, 4, 3, ..., -1000, ...


try:
    no_base_case(5)
    raise AssertionError("expected RecursionError")
except RecursionError:
    pass


# --- Python's recursion limit ---
default_limit = sys.getrecursionlimit()
assert default_limit == 1000, default_limit         # CPython default
sys.setrecursionlimit(10_000)
assert factorial(3000) > 0                           # would crash under the default limit
sys.setrecursionlimit(default_limit)


# --- Lesson 8: iteration vs recursion (NeetCode's loop, verbatim) ---
n = 5
res = 1
while n > 1:
    res = res * n
    n -= 1
assert res == 120
assert n == 1


def factorial_iter(n):
    res = 1
    while n > 1:
        res = res * n
        n -= 1
    return res


assert [factorial_iter(i) for i in range(7)] == [1, 1, 2, 6, 24, 120, 720]
assert all(factorial_iter(i) == factorial(i) for i in range(12))


# --- Lesson 9: fibonacci, two-branch recursion (NeetCode version) ---
def fibonacci(n):
    # Base case: n = 0 or 1
    if n <= 1:
        return n
    # Recursive case: fib(n) = fib(n - 1) + fib(n - 2)
    return fibonacci(n - 1) + fibonacci(n - 2)


assert [fibonacci(i) for i in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
assert fibonacci(5) == 5
assert fibonacci(4) == 3
assert fibonacci(3) == 2
assert fibonacci(5) == fibonacci(4) + fibonacci(3)


# --- count the calls: how big is the tree? ---
calls = 0


def fib_counted(n):
    global calls
    calls += 1
    if n <= 1:
        return n
    return fib_counted(n - 1) + fib_counted(n - 2)


def count_calls(n):
    global calls
    calls = 0
    fib_counted(n)
    return calls


assert count_calls(4) == 9
assert count_calls(5) == 15
assert count_calls(10) == 177
assert count_calls(20) == 21891
# upper bound from the lesson: at most 1 + 2 + 4 + ... + 2^n = 2^(n+1) - 1 nodes
for k in range(1, 15):
    assert count_calls(k) <= 2 ** (k + 1) - 1
assert 1 + 2 + 4 + 8 == 2 ** 4 - 1


# --- trace of fibonacci(4): call order, depth, and return values ---
events = []


def fib_traced(n, depth=0):
    events.append(("call", n, depth))
    if n <= 1:
        events.append(("ret", n, n))
        return n
    total = fib_traced(n - 1, depth + 1) + fib_traced(n - 2, depth + 1)
    events.append(("ret", n, total))
    return total


assert fib_traced(4) == 3
assert [e for e in events if e[0] == "call"] == [
    ("call", 4, 0), ("call", 3, 1), ("call", 2, 2), ("call", 1, 3), ("call", 0, 3),
    ("call", 1, 2), ("call", 2, 1), ("call", 1, 2), ("call", 0, 2),
]
assert [e for e in events if e[0] == "ret"] == [
    ("ret", 1, 1), ("ret", 0, 0), ("ret", 2, 1), ("ret", 1, 1), ("ret", 3, 2),
    ("ret", 1, 1), ("ret", 0, 0), ("ret", 2, 1), ("ret", 4, 3),
]
assert max(e[2] for e in events if e[0] == "call") == 3   # depth n-1 -> stack is O(n)


# --- Pattern 1: base case first (tiny example) ---
def sum_list(nums, i=0):
    if i == len(nums):              # base case FIRST: nothing left to add
        return 0
    return nums[i] + sum_list(nums, i + 1)   # trust the smaller call


assert sum_list([2, 3, 4, 1, 6]) == 16
assert sum_list([]) == 0
assert sum_list([7]) == 7


# --- Pattern 2: recursion -> iteration ---
def fib_iter(n):
    a, b = 0, 1                      # a = fib(i), b = fib(i + 1)
    for _ in range(n):
        a, b = b, a + b
    return a


assert [fib_iter(i) for i in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
assert all(fib_iter(i) == fibonacci(i) for i in range(15))


def sum_list_iter(nums):
    stack = [0]                      # our own stack replaces the call stack
    total = 0
    while stack:
        i = stack.pop()
        if i == len(nums):
            continue
        total += nums[i]
        stack.append(i + 1)
    return total


assert sum_list_iter([2, 3, 4, 1, 6]) == 16
assert sum_list_iter([]) == 0


# --- Pattern 3: helper function with an accumulator ---
def factorial_acc(n):
    def helper(n, acc):
        if n <= 1:
            return acc               # the answer is already finished
        return helper(n - 1, acc * n)
    return helper(n, 1)


assert factorial_acc(5) == 120
assert factorial_acc(0) == 1
assert all(factorial_acc(i) == factorial(i) for i in range(10))


def reverseString(s):                # LeetCode 344, in place, recursive
    def helper(l, r):
        if l >= r:                   # pointers met or crossed: done
            return
        s[l], s[r] = s[r], s[l]
        helper(l + 1, r - 1)
    helper(0, len(s) - 1)


s = ["h", "e", "l", "l", "o"]
reverseString(s)
assert s == ["o", "l", "l", "e", "h"]
s = ["H", "a", "n", "n", "a", "h"]
reverseString(s)
assert s == ["h", "a", "n", "n", "a", "H"]
s = []
reverseString(s)
assert s == []


# --- Pattern 4: memoization preview (full treatment on the DP page) ---
from functools import lru_cache


@lru_cache(maxsize=None)
def fib_memo(n):
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


assert fib_memo(5) == 5
assert fib_memo(50) == 12586269025
assert all(fib_memo(i) == fib_iter(i) for i in range(30))

memo_calls = 0


def fib_memo_counted(n, memo={}):
    global memo_calls
    memo_calls += 1
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo_counted(n - 1, memo) + fib_memo_counted(n - 2, memo)
    return memo[n]


assert fib_memo_counted(5, {}) == 5
assert memo_calls == 9              # 6 real computations + 3 cache hits (vs 15 calls without memo)


# --- Practice helpers that appear on the page: recursive reverse linked list (LC 206) ---
class ListNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


def reverseList(head):
    if head is None or head.next is None:   # base case: empty or single node
        return head
    new_head = reverseList(head.next)       # trust: reverses everything after head
    head.next.next = head                   # the old "next" now points back at head
    head.next = None                        # head becomes the tail
    return new_head


def build(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


assert to_list(reverseList(build([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
assert to_list(reverseList(build([1]))) == [1]
assert reverseList(None) is None

print("all checks passed")
