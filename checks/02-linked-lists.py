# --- Singly linked list ---
class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None


a = ListNode("red")
b = ListNode("blue")
c = ListNode("green")
a.next = b
b.next = c
c.next = None

head = a
tail = c

# traversal
cur = head
out = []
while cur:
    out.append(cur.val)
    cur = cur.next
assert out == ["red", "blue", "green"], out

# append at tail
d = ListNode("yellow")
tail.next = d
tail = d
cur = head
out = []
while cur:
    out.append(cur.val)
    cur = cur.next
assert out == ["red", "blue", "green", "yellow"], out

# delete the node after head
head.next = head.next.next
cur = head
out = []
while cur:
    out.append(cur.val)
    cur = cur.next
assert out == ["red", "green", "yellow"], out


# --- Singly linked list class with head/tail ---
class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, val):
        node = ListNode(val)
        if self.tail:
            self.tail.next = node
            self.tail = node
        else:
            self.head = self.tail = node

    def delete_after(self, node):
        # deletes node.next, if it exists
        if node is None or node.next is None:
            return
        removed = node.next
        node.next = removed.next
        if removed is self.tail:
            self.tail = node

    def to_list(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.val)
            cur = cur.next
        return out


s = SinglyLinkedList()
for v in [1, 2, 3]:
    s.append(v)
assert s.to_list() == [1, 2, 3]
s.delete_after(s.head)
assert s.to_list() == [1, 3]
s.delete_after(s.head)          # deletes tail
assert s.to_list() == [1] and s.tail is s.head
s.append(9)
assert s.to_list() == [1, 9]


# --- Doubly linked list ---
class DNode:
    def __init__(self, val):
        self.val = val
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_end(self, val):
        node = DNode(val)
        if self.tail:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        else:
            self.head = self.tail = node

    def insert_front(self, val):
        node = DNode(val)
        if self.head:
            node.next = self.head
            self.head.prev = node
            self.head = node
        else:
            self.head = self.tail = node

    def delete_end(self):
        if not self.tail:
            return None
        val = self.tail.val
        if self.tail is self.head:
            self.head = self.tail = None
        else:
            before = self.tail.prev
            before.next = None
            self.tail = before
        return val

    def delete_front(self):
        if not self.head:
            return None
        val = self.head.val
        if self.head is self.tail:
            self.head = self.tail = None
        else:
            after = self.head.next
            after.prev = None
            self.head = after
        return val

    def forward(self):
        out, cur = [], self.head
        while cur:
            out.append(cur.val)
            cur = cur.next
        return out

    def backward(self):
        out, cur = [], self.tail
        while cur:
            out.append(cur.val)
            cur = cur.prev
        return out


d = DoublyLinkedList()
d.insert_end(2)
d.insert_end(3)
d.insert_front(1)
assert d.forward() == [1, 2, 3]
assert d.backward() == [3, 2, 1]
assert d.delete_end() == 3
assert d.delete_front() == 1
assert d.forward() == [2]
assert d.delete_end() == 2
assert d.head is None and d.tail is None
assert d.delete_end() is None


# --- Queue with linked list ---
class Queue:
    def __init__(self):
        self.left = None    # front: dequeue here
        self.right = None   # back: enqueue here

    def enqueue(self, val):
        newNode = ListNode(val)
        if self.right:                   # queue is non-empty
            self.right.next = newNode
            self.right = self.right.next
        else:                            # queue is empty
            self.left = self.right = newNode

    def dequeue(self):
        if not self.left:                # queue is empty
            return None
        val = self.left.val
        self.left = self.left.next
        if not self.left:                # queue became empty
            self.right = None
        return val

    def is_empty(self):
        return self.left is None


q = Queue()
assert q.dequeue() is None
q.enqueue("A")
q.enqueue("B")
q.enqueue("C")
assert q.dequeue() == "A"
assert q.dequeue() == "B"
assert q.dequeue() == "C"
assert q.is_empty() and q.right is None
q.enqueue("D")
assert q.dequeue() == "D"

from collections import deque
dq = deque()
dq.append(1); dq.append(2); dq.appendleft(0)
assert dq.popleft() == 0 and dq.pop() == 2 and list(dq) == [1]


# --- Patterns ---
def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next      # 1. save next
        cur.next = prev     # 2. flip pointer
        prev = cur          # 3. move prev
        cur = nxt           # 4. move cur
    return prev


def build(vals):
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


assert to_list(reverse_list(build([1, 2, 3, 4]))) == [4, 3, 2, 1]
assert reverse_list(None) is None


def remove_value(head, target):
    dummy = ListNode(0)
    dummy.next = head
    cur = dummy
    while cur.next:
        if cur.next.val == target:
            cur.next = cur.next.next   # skip it
        else:
            cur = cur.next
    return dummy.next


assert to_list(remove_value(build([7, 1, 7, 2, 7]), 7)) == [1, 2]
assert to_list(remove_value(build([7]), 7)) == []


def middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


assert middle(build([1, 2, 3, 4, 5])).val == 3
assert middle(build([1, 2, 3, 4])).val == 3


def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


h = build([1, 2, 3])
assert has_cycle(h) is False
h.next.next.next = h.next   # 3 -> 2 makes a cycle
assert has_cycle(h) is True

print("all checks passed")
