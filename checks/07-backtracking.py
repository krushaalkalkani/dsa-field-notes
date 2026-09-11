# Checks for site/topics/07-backtracking.html
# Every function on the page lives here and is tested on the lesson's own trees.

# --- Lesson code: TreeNode, canReachLeaf, leafPath ---
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def canReachLeaf(root):
    if not root or root.val == 0:
        return False

    if not root.left and not root.right:
        return True
    if canReachLeaf(root.left):
        return True
    if canReachLeaf(root.right):
        return True
    return False


def leafPath(root, path):
    if not root or root.val == 0:
        return False
    path.append(root.val)

    if not root.left and not root.right:
        return True
    if leafPath(root.left, path):
        return True
    if leafPath(root.right, path):
        return True
    path.pop()
    return False


# helper: build a tree from a LeetCode-style level-order list (None = missing)
def build(level):
    if not level or level[0] is None:
        return None
    nodes = [TreeNode(v) if v is not None else None for v in level]
    kids = nodes[1:]           # children in order, consumed two at a time
    kids.reverse()
    for node in nodes:
        if node is None:
            continue
        if kids:
            node.left = kids.pop()
        if kids:
            node.right = kids.pop()
    return nodes[0]


# Tree A from the lesson: [4,0,1,null,7,2,0]
A = build([4, 0, 1, None, 7, 2, 0])
assert A.val == 4
assert A.left.val == 0 and A.left.left is None and A.left.right.val == 7
assert A.right.val == 1 and A.right.left.val == 2 and A.right.right.val == 0
assert canReachLeaf(A) is True
pathA = []
assert leafPath(A, pathA) is True
assert pathA == [4, 1, 2], pathA

# Tree B from the lesson: [4,0,1,null,7,3,2,null,null,null,0]
B = build([4, 0, 1, None, 7, 3, 2, None, None, None, 0])
assert B.val == 4
assert B.left.val == 0 and B.left.left is None and B.left.right.val == 7
assert B.right.val == 1 and B.right.left.val == 3 and B.right.right.val == 2
assert B.right.left.left is None and B.right.left.right.val == 0
assert B.right.right.left is None and B.right.right.right is None
assert canReachLeaf(B) is True
pathB = []
assert leafPath(B, pathB) is True
assert pathB == [4, 1, 2], pathB

# Edge cases from the lesson text
assert canReachLeaf(None) is False            # empty tree -> no valid path
assert canReachLeaf(TreeNode(0)) is False     # root is 0
assert canReachLeaf(TreeNode(5)) is True      # single node is a leaf
p = []
assert leafPath(None, p) is False and p == []
p = []
assert leafPath(TreeNode(0), p) is False and p == []   # never appended
p = []
assert leafPath(TreeNode(5), p) is True and p == [5]

# A tree with NO valid path: every leaf sits under a 0 or is a 0
C = build([1, 0, 2, None, None, 0, 0])
assert canReachLeaf(C) is False
pC = []
assert leafPath(C, pC) is False
assert pC == [], pC                           # path fully un-chosen on failure


# --- Instrumented leafPath for the trace table on the page ---
def leafPath_traced(root, path, log):
    name = "None" if root is None else str(root.val)
    if not root or root.val == 0:
        log.append((name, list(path), "False (base)"))
        return False
    path.append(root.val)
    if not root.left and not root.right:
        log.append((name, list(path), "True (leaf)"))
        return True
    if leafPath_traced(root.left, path, log):
        log.append((name, list(path), "True (from left)"))
        return True
    if leafPath_traced(root.right, path, log):
        log.append((name, list(path), "True (from right)"))
        return True
    path.pop()
    log.append((name, list(path), "False (popped)"))
    return False


log = []
assert leafPath_traced(B, [], log) is True
# Order of returns as the trace table on the page lists them
expected_returns = [
    ("0", [4], "False (base)"),               # 4's left child is 0
    ("None", [4, 1, 3], "False (base)"),      # 3's left is null
    ("0", [4, 1, 3], "False (base)"),         # 3's right is 0
    ("3", [4, 1], "False (popped)"),          # pop 3
    ("2", [4, 1, 2], "True (leaf)"),          # 2 is a leaf
    ("1", [4, 1, 2], "True (from right)"),
    ("4", [4, 1, 2], "True (from right)"),
]
assert log == expected_returns, log


# --- Pattern 1: the universal template (choose / explore / un-choose) ---
def backtrack_template(candidates):
    """Enumerate every ordered selection of distinct items (all permutations of
    every length). Exists to show the three-line shape; tested below."""
    res, choice = [], []

    def explore():
        res.append(list(choice))          # record the current state
        for c in candidates:
            if c in choice:
                continue                  # prune: cannot reuse
            choice.append(c)              # choose
            explore()                     # explore
            choice.pop()                  # un-choose
    explore()
    return res


t = backtrack_template([1, 2])
assert t == [[], [1], [1, 2], [2], [2, 1]], t


# --- Pattern 2: subsets ---
def subsets(nums):
    res, cur = [], []

    def dfs(i):
        if i == len(nums):
            res.append(cur[:])            # copy! cur keeps changing
            return
        cur.append(nums[i])               # choose nums[i]
        dfs(i + 1)
        cur.pop()                         # un-choose
        dfs(i + 1)                        # skip nums[i]
    dfs(0)
    return res


assert subsets([1, 2]) == [[1, 2], [1], [2], []], subsets([1, 2])
assert len(subsets([1, 2, 3])) == 8
assert sorted(map(sorted, subsets([1, 2, 3]))) == sorted(
    [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]])
assert subsets([]) == [[]]


# --- Pattern 3: permutations ---
def permutations(nums):
    res, cur, used = [], [], [False] * len(nums)

    def dfs():
        if len(cur) == len(nums):
            res.append(cur[:])
            return
        for i in range(len(nums)):
            if used[i]:
                continue
            used[i] = True                # choose
            cur.append(nums[i])
            dfs()                         # explore
            cur.pop()                     # un-choose
            used[i] = False
    dfs()
    return res


assert permutations([1, 2, 3]) == [
    [1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
assert permutations([]) == [[]]
assert len(permutations([1, 2, 3, 4])) == 24


# --- Pattern 4: combinations (choose k of n, order does not matter) ---
def combinations(n, k):
    res, cur = [], []

    def dfs(start):
        if len(cur) == k:
            res.append(cur[:])
            return
        for i in range(start, n + 1):
            cur.append(i)                 # choose
            dfs(i + 1)                    # explore only larger numbers
            cur.pop()                     # un-choose
    dfs(1)
    return res


assert combinations(4, 2) == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
assert combinations(3, 3) == [[1, 2, 3]]
assert combinations(3, 0) == [[]]
assert len(combinations(5, 3)) == 10


# --- Path Sum II style: collect ALL valid root-to-leaf paths (the "all
# solutions" version of leafPath). Used on the page to show that a
# collecting version records a COPY and never returns early.
def allLeafPaths(root):
    res, path = [], []

    def dfs(node):
        if not node or node.val == 0:
            return
        path.append(node.val)
        if not node.left and not node.right:
            res.append(path[:])
        else:
            dfs(node.left)
            dfs(node.right)
        path.pop()
    dfs(root)
    return res


assert allLeafPaths(A) == [[4, 1, 2]]
assert allLeafPaths(B) == [[4, 1, 2]]
assert allLeafPaths(C) == []
D = build([1, 2, 3, 4, 5, None, 6])
assert allLeafPaths(D) == [[1, 2, 4], [1, 2, 5], [1, 3, 6]]


# --- Self-check helper claims ---
# Space: the path list never holds more than h+1... it holds at most the
# number of nodes on the current root-to-node path, which is <= height+1.
def max_path_len(root):
    best = [0]
    path = []

    def dfs(node):
        if not node or node.val == 0:
            return False
        path.append(node.val)
        best[0] = max(best[0], len(path))
        if not node.left and not node.right:
            return True
        if dfs(node.left) or dfs(node.right):
            return True
        path.pop()
        return False
    dfs(root)
    return best[0]


assert max_path_len(B) == 3      # 4 -> 1 -> 3 was the deepest the list got

print("all checks passed")
