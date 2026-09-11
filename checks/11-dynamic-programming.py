# Checks for site/topics/11-dynamic-programming.html
# Every function that appears on the page is here, tested on the lesson's own examples.

from functools import lru_cache, cache

# ============================================================
# Lesson 32: 1-D DP - fibonacci
# ============================================================

# --- brute force (NeetCode) ---
def bruteForce(n):
    if n <= 1:
        return n
    return bruteForce(n - 1) + bruteForce(n - 2)


# --- count how many calls the brute force makes (for the tree diagram) ---
def bruteForceCount(n, counter):
    counter[0] += 1
    if n <= 1:
        return n
    return bruteForceCount(n - 1, counter) + bruteForceCount(n - 2, counter)


calls = [0]
assert bruteForceCount(5, calls) == 5
assert calls[0] == 15, calls          # 15 nodes in the bruteForce(5) tree

# how many times is each F(k) computed inside bruteForce(5)?
def countCalls(n, seen):
    seen[n] = seen.get(n, 0) + 1
    if n <= 1:
        return n
    return countCalls(n - 1, seen) + countCalls(n - 2, seen)


seen = {}
countCalls(5, seen)
assert seen[2] == 3, seen             # F(2) computed three times (lesson claim)
assert seen[3] == 2, seen             # F(3) computed twice
assert seen[1] == 5 and seen[0] == 3, seen


# --- top-down memoization (NeetCode) ---
def memoization(n, cache):
    if n <= 1:
        return n
    if n in cache:
        return cache[n]

    cache[n] = memoization(n - 1, cache) + memoization(n - 2, cache)
    return cache[n]


# count real (non-cache) computations for the memo diagram
def memoCount(n, cache, counter):
    counter[0] += 1                   # every call, including cache hits
    if n <= 1:
        return n
    if n in cache:
        return cache[n]
    cache[n] = memoCount(n - 1, cache, counter) + memoCount(n - 2, cache, counter)
    return cache[n]


c = [0]
memo = {}
assert memoCount(5, memo, c) == 5
assert c[0] == 9, c                   # 15 calls shrink to 9 (5 real + 1 base F(1) ... see page)
assert sorted(memo) == [2, 3, 4, 5]   # only n-1 = 4 stored entries: F(2)..F(5)


# --- bottom-up with a full table (page adds this as the middle step) ---
def tabulation(n):
    if n < 2:
        return n
    table = [0] * (n + 1)
    table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]


def tabulationTable(n):
    table = [0] * (n + 1)
    if n >= 1:
        table[1] = 1
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table


assert tabulationTable(5) == [0, 1, 1, 2, 3, 5]      # lesson's array


# --- bottom-up O(1) space (NeetCode) ---
def dp(n):
    if n < 2:
        return n

    dp = [0, 1]
    i = 2
    while i <= n:
        tmp = dp[1]
        dp[1] = dp[0] + dp[1]
        dp[0] = tmp
        i += 1
    return dp[1]


# trace of dp(5) for the trace table
def dpTrace(n):
    rows = []
    d = [0, 1]
    i = 2
    rows.append((None, d[0], d[1]))
    while i <= n:
        tmp = d[1]
        d[1] = d[0] + d[1]
        d[0] = tmp
        rows.append((i, d[0], d[1]))
        i += 1
    return rows


assert dpTrace(5) == [(None, 0, 1), (2, 1, 1), (3, 1, 2), (4, 2, 3), (5, 3, 5)], dpTrace(5)


# --- idiomatic Python: tuple swap ---
def fib_two_vars(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# --- idiomatic Python: lru_cache / cache decorator ---
@lru_cache(maxsize=None)
def fib_lru(n):
    if n <= 1:
        return n
    return fib_lru(n - 1) + fib_lru(n - 2)


@cache
def fib_cache(n):
    if n <= 1:
        return n
    return fib_cache(n - 1) + fib_cache(n - 2)


# all versions agree for n in 0..15
expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
for n in range(16):
    assert bruteForce(n) == expected[n], n
    assert memoization(n, {}) == expected[n], n
    assert tabulation(n) == expected[n], n
    assert dp(n) == expected[n], n
    assert fib_two_vars(n) == expected[n], n
    assert fib_lru(n) == expected[n], n
    assert fib_cache(n) == expected[n], n

# the cached versions handle big n instantly; brute force could not
assert fib_cache(100) == 354224848179261915075
assert dp(100) == 354224848179261915075
assert fib_lru.cache_info().hits > 0


# ============================================================
# Lesson 33: 2-D DP - unique paths
# ============================================================

# Brute Force - Time: O(2 ^ (n + m)), Space: O(n + m)
def bruteForce2D(r, c, rows, cols):
    if r == rows or c == cols:
        return 0
    if r == rows - 1 and c == cols - 1:
        return 1

    return (bruteForce2D(r + 1, c, rows, cols) +
            bruteForce2D(r, c + 1, rows, cols))


# Memoization - Time and Space: O(n * m)
def memoization2D(r, c, rows, cols, cache):
    if r == rows or c == cols:
        return 0
    if cache[r][c] > 0:
        return cache[r][c]
    if r == rows - 1 and c == cols - 1:
        return 1

    cache[r][c] = (memoization2D(r + 1, c, rows, cols, cache) +
                   memoization2D(r, c + 1, rows, cols, cache))
    return cache[r][c]


# Dynamic Programming - Time: O(n * m), Space: O(m), where m is num of cols
def dp2D(rows, cols):
    prevRow = [0] * cols

    for r in range(rows - 1, -1, -1):
        curRow = [0] * cols
        curRow[cols - 1] = 1
        for c in range(cols - 2, -1, -1):
            curRow[c] = curRow[c + 1] + prevRow[c]
        prevRow = curRow
    return prevRow[0]


# trace of every row for the 3x3 trace table
def dp2DTrace(rows, cols):
    out = []
    prevRow = [0] * cols
    out.append(("init", list(prevRow)))
    for r in range(rows - 1, -1, -1):
        curRow = [0] * cols
        curRow[cols - 1] = 1
        for c in range(cols - 2, -1, -1):
            curRow[c] = curRow[c + 1] + prevRow[c]
        prevRow = curRow
        out.append((r, list(curRow)))
    return out


assert dp2DTrace(3, 3) == [("init", [0, 0, 0]),
                            (2, [1, 1, 1]),
                            (1, [3, 2, 1]),
                            (0, [6, 3, 1])], dp2DTrace(3, 3)

assert dp2DTrace(4, 4) == [("init", [0, 0, 0, 0]),
                            (3, [1, 1, 1, 1]),
                            (2, [4, 3, 2, 1]),
                            (1, [10, 6, 3, 1]),
                            (0, [20, 10, 4, 1])], dp2DTrace(4, 4)


# full cache grid after top-down on 4x4 (for the cache-grid diagram)
def memoGrid(rows, cols):
    cache = [[0] * cols for _ in range(rows)]
    memoization2D(0, 0, rows, cols, cache)
    return cache


g = memoGrid(4, 4)
assert g == [[20, 10, 4, 1],
             [10, 6, 3, 1],
             [4, 3, 2, 1],
             [1, 1, 1, 0]], g
# note: the bottom-right (3,3) stays 0 in the cache because it returns 1 before caching;
# the last column and last row are all 1 (only one way: straight down / straight right)


# count brute-force calls on 4x4 to show the overlap (for the diagram caption)
def bruteCount2D(r, c, rows, cols, counter):
    counter[0] += 1
    if r == rows or c == cols:
        return 0
    if r == rows - 1 and c == cols - 1:
        return 1
    return (bruteCount2D(r + 1, c, rows, cols, counter) +
            bruteCount2D(r, c + 1, rows, cols, counter))


cnt = [0]
assert bruteCount2D(0, 0, 4, 4, cnt) == 20
brute_calls_4x4 = cnt[0]
assert brute_calls_4x4 == 99, brute_calls_4x4   # 99 calls for 16 cells

# how many times is cell (1,1) visited by brute force on 4x4?
def visitCount(r, c, rows, cols, seen):
    if r == rows or c == cols:
        return 0
    seen[(r, c)] = seen.get((r, c), 0) + 1
    if r == rows - 1 and c == cols - 1:
        return 1
    return (visitCount(r + 1, c, rows, cols, seen) +
            visitCount(r, c + 1, rows, cols, seen))


seenCells = {}
visitCount(0, 0, 4, 4, seenCells)
assert seenCells[(1, 1)] == 2, seenCells       # reached by down-right and right-down
assert seenCells[(2, 2)] == 6, seenCells
assert seenCells[(3, 3)] == 20, seenCells      # visited once per path


# --- idiomatic Python: lru_cache version of unique paths ---
def uniquePaths_cache(rows, cols):
    @cache
    def go(r, c):
        if r == rows or c == cols:
            return 0
        if r == rows - 1 and c == cols - 1:
            return 1
        return go(r + 1, c) + go(r, c + 1)
    return go(0, 0)


# --- full 2-D grid bottom-up (the middle step, before the row trick) ---
def uniquePaths_grid(rows, cols):
    grid = [[0] * cols for _ in range(rows)]
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if r == rows - 1 and c == cols - 1:
                grid[r][c] = 1
            else:
                down = grid[r + 1][c] if r + 1 < rows else 0
                right = grid[r][c + 1] if c + 1 < cols else 0
                grid[r][c] = down + right
    return grid[0][0]


for rows, cols, want in [(3, 3, 6), (4, 4, 20), (3, 7, 28), (1, 1, 1), (1, 5, 1), (2, 2, 2)]:
    assert bruteForce2D(0, 0, rows, cols) == want, (rows, cols)
    cache2 = [[0] * cols for _ in range(rows)]
    assert memoization2D(0, 0, rows, cols, cache2) == want, (rows, cols)
    assert dp2D(rows, cols) == want, (rows, cols)
    assert uniquePaths_cache(rows, cols) == want, (rows, cols)
    assert uniquePaths_grid(rows, cols) == want, (rows, cols)


# ============================================================
# Patterns: 1-D "dp[i] depends on dp[i-1], dp[i-2]" family
# ============================================================

# Climbing Stairs (LC 70): ways to reach step n taking 1 or 2 steps
def climbStairs(n):
    one, two = 1, 1           # ways from step n and step n-1 (both 1)
    for _ in range(n - 1):
        one, two = one + two, one
    return one


assert [climbStairs(n) for n in range(1, 8)] == [1, 2, 3, 5, 8, 13, 21]


# Min Cost Climbing Stairs (LC 746)
def minCostClimbingStairs(cost):
    a, b = 0, 0               # min cost to stand on step i-2 and i-1
    for i in range(2, len(cost) + 1):
        a, b = b, min(b + cost[i - 1], a + cost[i - 2])
    return b


assert minCostClimbingStairs([10, 15, 20]) == 15
assert minCostClimbingStairs([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]) == 6


# House Robber (LC 198): rob or skip
def rob(nums):
    rob1, rob2 = 0, 0         # best up to i-2, best up to i-1
    for n in nums:
        rob1, rob2 = rob2, max(rob1 + n, rob2)
    return rob2


assert rob([1, 2, 3, 1]) == 4
assert rob([2, 7, 9, 3, 1]) == 12
assert rob([]) == 0


# ============================================================
# Patterns: 2-D grid family - Min Path Sum (LC 64)
# ============================================================
def minPathSum(grid):
    rows, cols = len(grid), len(grid[0])
    prev = [float("inf")] * cols
    for r in range(rows - 1, -1, -1):
        cur = [0] * cols
        for c in range(cols - 1, -1, -1):
            if r == rows - 1 and c == cols - 1:
                cur[c] = grid[r][c]
            else:
                right = cur[c + 1] if c + 1 < cols else float("inf")
                down = prev[c]
                cur[c] = grid[r][c] + min(right, down)
        prev = cur
    return prev[0]


assert minPathSum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
assert minPathSum([[1, 2, 3], [4, 5, 6]]) == 12


# ============================================================
# Patterns: memo decorator template (generic)
# ============================================================
def solve_with_memo(n):
    @cache
    def f(i):
        if i <= 1:            # base case
            return i
        return f(i - 1) + f(i - 2)   # recurrence
    return f(n)


assert solve_with_memo(10) == 55

# Self-check traces: dp(6) rows and a 2x3 grid
assert dpTrace(6)[-1] == (6, 5, 8)
assert dp2DTrace(2, 3) == [("init", [0, 0, 0]), (1, [1, 1, 1]), (0, [3, 2, 1])]
assert dp2D(2, 3) == 3

print("all checks passed")
