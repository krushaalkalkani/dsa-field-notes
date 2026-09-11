# Checks for site/topics/06-trees.html
# Every class / function that appears on the page lives here and is tested
# against the trees and outputs stated in lessons/06-trees.md.

from collections import deque


# --- Lesson 16: the node -------------------------------------------------
class ListNode:                      # shown next to TreeNode for comparison
    def __init__(self, val):
        self.val = val
        self.next = None


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


# helper used on the page: build a tree from the LeetCode level-order list
def build_tree(values):
    """[2,1,3,None,None,None,4] -> root of that tree (LeetCode format)."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def to_list(root):
    """Inverse of build_tree, trailing Nones trimmed (LeetCode format)."""
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


# building the lesson-16 example tree by hand, the way the lesson does
root = TreeNode(2)
root.left = TreeNode(1)
root.right = TreeNode(3)
root.right.right = TreeNode(4)
assert to_list(root) == [2, 1, 3, None, None, None, 4]
assert build_tree([2, 1, 3, None, None, None, 4]).right.right.val == 4
assert to_list(build_tree([4, 3, 6, 2, None, 5, 7])) == [4, 3, 6, 2, None, 5, 7]
assert build_tree([]) is None


# terminology helpers: height counted in nodes vs edges, depth of a value
def height_nodes(root):
    if not root:
        return 0
    return 1 + max(height_nodes(root.left), height_nodes(root.right))


def height_edges(root):
    if not root:
        return -1                    # empty tree: no nodes, so "one less than 0"
    return 1 + max(height_edges(root.left), height_edges(root.right))


def depth_of(root, target, depth=1):
    """Depth counted in nodes, root = 1. Returns 0 if target is absent."""
    if not root:
        return 0
    if root.val == target:
        return depth
    return depth_of(root.left, target, depth + 1) or depth_of(root.right, target, depth + 1)


def count_nodes(root):
    if not root:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)


def count_edges(root):
    n = count_nodes(root)
    return n - 1 if n else 0


def is_leaf(node):
    return node is not None and node.left is None and node.right is None


t16 = build_tree([2, 1, 3, None, None, None, 4])
assert height_nodes(t16) == 3 and height_edges(t16) == 2       # lesson: 3 nodes, 2 edges
assert height_nodes(TreeNode(9)) == 1 and height_edges(TreeNode(9)) == 0
assert depth_of(t16, 2) == 1 and depth_of(t16, 3) == 2 and depth_of(t16, 4) == 3
assert count_nodes(t16) == 4 and count_edges(t16) == 3         # edges = n - 1
assert is_leaf(t16.left) and is_leaf(t16.right.right) and not is_leaf(t16.right)


# --- Lesson 17: BST search -----------------------------------------------
def search(root, target):
    if not root:
        return False

    if target > root.val:
        return search(root.right, target)
    elif target < root.val:
        return search(root.left, target)
    else:
        return True


bst = build_tree([2, 1, 3, None, None, None, 4])
assert search(bst, 3) is True
assert search(bst, 4) is True
assert search(bst, 1) is True
assert search(bst, 5) is False
assert search(bst, 0) is False
assert search(None, 3) is False


# iterative search (same steps, no call stack)
def search_iter(root, target):
    cur = root
    while cur:
        if target > cur.val:
            cur = cur.right
        elif target < cur.val:
            cur = cur.left
        else:
            return True
    return False


for v in range(0, 7):
    assert search_iter(bst, v) == search(bst, v)


# --- Lesson 18: insert and remove ----------------------------------------
# Insert a new node and return the root of the BST.
def insert(root, val):
    if not root:
        return TreeNode(val)

    if val > root.val:
        root.right = insert(root.right, val)
    elif val < root.val:
        root.left = insert(root.left, val)
    return root


r = TreeNode(4)
r = insert(r, 6)
assert to_list(r) == [4, None, 6]                # lesson: 6 becomes the right child
r = insert(r, 5)
assert to_list(r) == [4, None, 6, 5]             # lesson writes [4,null,6,5,null]
assert insert(None, 7).val == 7                  # inserting into an empty tree
r = insert(r, 5)                                 # duplicate: tree unchanged
assert to_list(r) == [4, None, 6, 5]


# Return the minimum value node of the BST.
def minValueNode(root):
    curr = root
    while curr and curr.left:
        curr = curr.left
    return curr


# Remove a node and return the root of the BST.
def remove(root, val):
    if not root:
        return None

    if val > root.val:
        root.right = remove(root.right, val)
    elif val < root.val:
        root.left = remove(root.left, val)
    else:
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        else:
            minNode = minValueNode(root.right)
            root.val = minNode.val
            root.right = remove(root.right, minNode.val)
    return root


# lesson-18 removal tree: 4 / 3 6 / 2 . 5 7   (same shape as the DFS tree)
t18 = build_tree([4, 3, 6, 2, None, 5, 7])
assert minValueNode(t18).val == 2
assert minValueNode(t18.right).val == 5
assert minValueNode(None) is None

# case 1a: 0 children - delete 2, 3.left becomes None
t = build_tree([4, 3, 6, 2, None, 5, 7])
t = remove(t, 2)
assert to_list(t) == [4, 3, 6, None, None, 5, 7]
# case 1b: 1 child - delete 3, root.left now points to 2
t = build_tree([4, 3, 6, 2, None, 5, 7])
t = remove(t, 3)
assert to_list(t) == [4, 2, 6, None, None, 5, 7]
# case 2: 2 children - delete 6, in-order successor 7 moves up
t = build_tree([4, 3, 6, 2, None, 5, 7])
t = remove(t, 6)
assert to_list(t) == [4, 3, 7, 2, None, 5]
# case 2 at the root - delete 4, successor is 5
t = build_tree([4, 3, 6, 2, None, 5, 7])
t = remove(t, 4)
assert to_list(t) == [5, 3, 6, 2, None, None, 7]
# removing a value that is not there leaves the tree alone
t = build_tree([4, 3, 6, 2, None, 5, 7])
assert to_list(remove(t, 99)) == [4, 3, 6, 2, None, 5, 7]
# removing the only node gives an empty tree
assert remove(TreeNode(1), 1) is None


# --- Lesson 19: DFS ------------------------------------------------------
# The lesson prints; here we collect into a list so we can assert on it.
def inorder(root, out):
    if not root:
        return
    inorder(root.left, out)
    out.append(root.val)
    inorder(root.right, out)


def preorder(root, out):
    if not root:
        return
    out.append(root.val)
    preorder(root.left, out)
    preorder(root.right, out)


def postorder(root, out):
    if not root:
        return
    postorder(root.left, out)
    postorder(root.right, out)
    out.append(root.val)


t19 = build_tree([4, 3, 6, 2, None, 5, 7])
o = []; inorder(t19, o);   assert o == [2, 3, 4, 5, 6, 7], o
o = []; preorder(t19, o);  assert o == [4, 3, 2, 6, 5, 7], o
o = []; postorder(t19, o); assert o == [2, 3, 5, 7, 6, 4], o
o = []; inorder(None, o);  assert o == []

# inorder is sorted only for a BST: same shape, values shuffled
not_bst = build_tree([1, 2, 3])
o = []; inorder(not_bst, o); assert o == [2, 1, 3]     # not sorted


# lesson-print versions, exactly as written (verified by capturing stdout)
def inorder_print(root):
    if not root:
        return
    inorder_print(root.left)
    print(root.val)
    inorder_print(root.right)


def preorder_print(root):
    if not root:
        return
    print(root.val)
    preorder_print(root.left)
    preorder_print(root.right)


def postorder_print(root):
    if not root:
        return
    postorder_print(root.left)
    postorder_print(root.right)
    print(root.val)


import io, contextlib


def captured(fn, *args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args)
    return [int(x) for x in buf.getvalue().split()]


assert captured(inorder_print, t19) == [2, 3, 4, 5, 6, 7]
assert captured(preorder_print, t19) == [4, 3, 2, 6, 5, 7]
assert captured(postorder_print, t19) == [2, 3, 5, 7, 6, 4]


# iterative DFS with an explicit stack (pattern section)
def preorder_iter(root):
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)
        if node.right:                 # push right first so left is popped first
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return out


def inorder_iter(root):
    out, stack, cur = [], [], root
    while cur or stack:
        while cur:                     # slide down-left, remembering the path
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()              # nothing further left: visit
        out.append(cur.val)
        cur = cur.right                # then go right
    return out


assert preorder_iter(t19) == [4, 3, 2, 6, 5, 7]
assert inorder_iter(t19) == [2, 3, 4, 5, 6, 7]
assert preorder_iter(None) == [] and inorder_iter(None) == []


# --- Lesson 20: BFS ------------------------------------------------------
def bfs(root):
    queue = deque()

    if root:
        queue.append(root)

    level = 0
    while len(queue) > 0:
        print("level: ", level)
        for i in range(len(queue)):
            curr = queue.popleft()
            print(curr.val)
            if curr.left:
                queue.append(curr.left)
            if curr.right:
                queue.append(curr.right)
        level += 1


buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    bfs(t19)
assert buf.getvalue() == "level:  0\n4\nlevel:  1\n3\n6\nlevel:  2\n2\n5\n7\n", buf.getvalue()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    bfs(None)
assert buf.getvalue() == ""


# level-size loop that returns the levels (LeetCode 102 shape)
def level_order(root):
    levels = []
    queue = deque([root] if root else [])
    while queue:
        size = len(queue)              # freeze the size: only this level
        level = []
        for _ in range(size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels


assert level_order(t19) == [[4], [3, 6], [2, 5, 7]]
assert level_order(None) == []
assert level_order(build_tree([2, 1, 3, None, None, None, 4])) == [[2], [1, 3], [4]]


# right side view: last value of each level (LeetCode 199)
def right_side_view(root):
    return [level[-1] for level in level_order(root)]


assert right_side_view(t19) == [4, 6, 7]
assert right_side_view(build_tree([1, 2, 3, None, 5, None, 4])) == [1, 3, 4]


# --- Patterns: the recursive template ------------------------------------
def max_depth(root):
    if not root:
        return 0
    left = max_depth(root.left)
    right = max_depth(root.right)
    return 1 + max(left, right)


def diameter(root):
    best = 0

    def height(node):
        nonlocal best
        if not node:
            return 0
        l = height(node.left)
        r = height(node.right)
        best = max(best, l + r)        # path through this node, counted in edges
        return 1 + max(l, r)

    height(root)
    return best


def is_balanced(root):
    def check(node):                   # returns height, or -1 if unbalanced below
        if not node:
            return 0
        l = check(node.left)
        if l == -1:
            return -1
        r = check(node.right)
        if r == -1:
            return -1
        if abs(l - r) > 1:
            return -1
        return 1 + max(l, r)

    return check(root) != -1


def invert(root):
    if not root:
        return None
    root.left, root.right = invert(root.right), invert(root.left)
    return root


def same_tree(p, q):
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return same_tree(p.left, q.left) and same_tree(p.right, q.right)


assert max_depth(t19) == 3 and max_depth(None) == 0
assert max_depth(build_tree([1, None, 2, None, 3])) == 3        # skewed
assert diameter(t19) == 4                                       # 2-3-4-6-5 or 2-3-4-6-7
assert diameter(build_tree([1, 2, 3, 4, 5])) == 3
assert is_balanced(t19) and not is_balanced(build_tree([1, None, 2, None, 3]))
assert is_balanced(None)
assert to_list(invert(build_tree([4, 2, 7, 1, 3, 6, 9]))) == [4, 7, 2, 9, 6, 3, 1]
assert same_tree(build_tree([1, 2, 3]), build_tree([1, 2, 3]))
assert not same_tree(build_tree([1, 2]), build_tree([1, None, 2]))


# validate a BST with min/max bounds
def is_valid_bst(root, low=float("-inf"), high=float("inf")):
    if not root:
        return True
    if not (low < root.val < high):
        return False
    return (is_valid_bst(root.left, low, root.val) and
            is_valid_bst(root.right, root.val, high))


assert is_valid_bst(t19)
assert is_valid_bst(build_tree([2, 1, 3, None, None, None, 4]))
assert not is_valid_bst(build_tree([5, 1, 4, None, None, 3, 6]))
# the trap: every node passes a local parent check but 6 sits in 5's left subtree
assert not is_valid_bst(build_tree([5, 4, 7, None, 6]))


# kth smallest via inorder (LeetCode 230)
def kth_smallest(root, k):
    stack, cur = [], root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right


assert kth_smallest(t19, 1) == 2 and kth_smallest(t19, 4) == 5


# lowest common ancestor in a BST (LeetCode 235)
def lca_bst(root, p, q):
    cur = root
    while cur:
        if p < cur.val and q < cur.val:
            cur = cur.left
        elif p > cur.val and q > cur.val:
            cur = cur.right
        else:
            return cur.val


assert lca_bst(t19, 2, 3) == 3 and lca_bst(t19, 5, 7) == 6 and lca_bst(t19, 2, 7) == 4


# --- Lesson 21: sets and maps on a BST -----------------------------------
class TreeMap:
    """A tiny map backed by the BST above: keys stay sorted."""
    class Node:
        def __init__(self, key, value):
            self.key, self.value = key, value
            self.left = self.right = None

    def __init__(self):
        self.root = None

    def put(self, key, value):
        def ins(node):
            if not node:
                return TreeMap.Node(key, value)
            if key < node.key:
                node.left = ins(node.left)
            elif key > node.key:
                node.right = ins(node.right)
            else:
                node.value = value          # same key: overwrite, keys stay unique
            return node
        self.root = ins(self.root)

    def get(self, key):
        cur = self.root
        while cur:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return cur.value
        return None

    def items(self):                        # inorder = sorted by key
        out = []
        def walk(node):
            if not node:
                return
            walk(node.left)
            out.append((node.key, node.value))
            walk(node.right)
        walk(self.root)
        return out


phone = TreeMap()
phone.put("Collin", 678)
phone.put("Alice", 123)
phone.put("Brad", 345)
assert phone.get("Brad") == 345 and phone.get("Zed") is None
assert phone.items() == [("Alice", 123), ("Brad", 345), ("Collin", 678)]
phone.put("Alice", 999)                     # a set/map keeps keys unique
assert phone.get("Alice") == 999 and len(phone.items()) == 3
assert [k for k, _ in phone.items()] == ["Alice", "Brad", "Collin"]   # TreeSet view

# the lesson's dict literal and its sorted order
book = {'Alice': 123, 'Brad': 345, 'Collin': 678}
assert sorted(book) == ["Alice", "Brad", "Collin"]

try:
    from sortedcontainers import SortedDict, SortedList
    treemap = SortedDict({'c': 3, 'a': 1, 'b': 2})
    assert list(treemap.keys()) == ['a', 'b', 'c']
    treemap['aa'] = 9
    assert list(treemap.keys()) == ['a', 'aa', 'b', 'c']
    sl = SortedList([5, 1, 3])
    sl.add(2)
    assert list(sl) == [1, 2, 3, 5]
    assert sl.bisect_left(3) == 2
    print("sortedcontainers present: SortedDict / SortedList checked")
except ImportError:
    print("sortedcontainers not installed: SortedDict lines shown as-is from the lesson")

print("all checks passed")
