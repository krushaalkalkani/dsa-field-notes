# Checks for site/topics/09-hashing.html (NeetCode lessons 26-27: Hash Usage, Hash Implementation)
# Every function / class that appears on the page is here, tested on the lesson's own examples.

from collections import Counter, defaultdict

# =====================================================================
# Lesson 26: Hash usage
# =====================================================================

# --- frequency count, NeetCode version ---
names = ["alice", "brad", "collin", "brad", "dylan", "kim"]

countMap = {}
for name in names:
    # If countMap does not contain name
    if name not in countMap:
        countMap[name] = 1
    else:
        countMap[name] += 1

assert countMap == {"alice": 1, "brad": 2, "collin": 1, "dylan": 1, "kim": 1}, countMap
# insertion order is kept (Python 3.7+), and it is NOT sorted
assert list(countMap) == ["alice", "brad", "collin", "dylan", "kim"]
assert sorted(countMap) == ["alice", "brad", "collin", "dylan", "kim"]  # happens to be alphabetical here

# --- idiomatic Python versions ---
c1 = {}
for name in names:
    c1[name] = c1.get(name, 0) + 1
assert c1 == countMap

c2 = defaultdict(int)
for name in names:
    c2[name] += 1
assert dict(c2) == countMap

c3 = Counter(names)
assert dict(c3) == countMap
assert c3["brad"] == 2
assert c3["nobody"] == 0          # missing key -> 0, no KeyError
assert c3.most_common(1) == [("brad", 2)]

# --- sets: keys only ---
seen = set(names)
assert len(seen) == 5             # 5 unique names
assert "brad" in seen and "zed" not in seen

# --- hashable keys ---
d = {}
d["alice"] = 1                    # str  ok
d[42] = 2                         # int  ok
d[(1, 2)] = 3                     # tuple ok
try:
    d[[1, 2]] = 4                 # list -> TypeError: unhashable type: 'list'
    raise AssertionError("list should not be hashable")
except TypeError as e:
    assert "unhashable" in str(e)
assert hash("Alice") == hash("Alice")   # same key -> same hash, always (inside one process)

# --- iterating in sorted order costs a sort ---
m = {"kim": 1, "alice": 1, "brad": 2}
assert list(m) == ["kim", "alice", "brad"]         # insertion order, not sorted
assert sorted(m) == ["alice", "brad", "kim"]       # O(n log n)

# =====================================================================
# Lesson 27: Hash implementation (open addressing), exactly as in the lesson
# =====================================================================

class Pair:
    def __init__(self, key, val):
        self.key = key
        self.val = val


class HashMap:
    def __init__(self):
        self.size = 0
        self.capacity = 2
        self.map = [None, None]

    def hash(self, key):
        index = 0
        for c in key:
            index += ord(c)
        return index % self.capacity

    def get(self, key):
        index = self.hash(key)

        while self.map[index] != None:
            if self.map[index].key == key:
                return self.map[index].val
            index += 1
            index = index % self.capacity
        return None

    def put(self, key, val):
        index = self.hash(key)

        while True:
            if self.map[index] == None:
                self.map[index] = Pair(key, val)
                self.size += 1
                if self.size >= self.capacity // 2:
                    self.rehash()
                return
            elif self.map[index].key == key:
                self.map[index].val = val
                return

            index += 1
            index = index % self.capacity

    def remove(self, key):
        if not self.get(key):
            return

        index = self.hash(key)
        while True:
            if self.map[index].key == key:
                # Removing an element using open-addressing actually causes a bug,
                # because we may create a hole in the list, and our get() may
                # stop searching early when it reaches this hole.
                self.map[index] = None
                self.size -= 1
                return
            index += 1
            index = index % self.capacity

    def rehash(self):
        self.capacity = 2 * self.capacity
        newMap = []
        for i in range(self.capacity):
            newMap.append(None)

        oldMap = self.map
        self.map = newMap
        self.size = 0
        for pair in oldMap:
            if pair:
                self.put(pair.key, pair.val)

    def print(self):
        for pair in self.map:
            if pair:
                print(pair.key, pair.val)


def slots(hm):
    """Helper for the trace tables: list of (index, key) for non-empty slots."""
    return [(i, p.key) for i, p in enumerate(hm.map) if p]


# --- the real ord() sums for the three names ---
assert sum(map(ord, "Alice")) == 478
assert sum(map(ord, "Brad")) == 377
assert sum(map(ord, "Collin")) == 609
assert [ord(c) for c in "Alice"] == [65, 108, 105, 99, 101]

# --- trace with the REAL sums, step by step ---
hm = HashMap()
assert (hm.capacity, hm.size, hm.map) == (2, 0, [None, None])

hm.put("Alice", "NYC")
# 478 % 2 = 0 -> slot 0, size 1 -> 1 >= 2//2 -> rehash to 4 -> 478 % 4 = 2
assert (hm.capacity, hm.size) == (4, 1)
assert slots(hm) == [(2, "Alice")]

hm.put("Brad", "Chicago")
# 377 % 4 = 1 -> slot 1, size 2 -> 2 >= 4//2 -> rehash to 8 -> Alice 478 % 8 = 6, Brad 377 % 8 = 1
assert (hm.capacity, hm.size) == (8, 2)
assert slots(hm) == [(1, "Brad"), (6, "Alice")]

hm.put("Collin", "Seattle")
# 609 % 8 = 1 -> occupied by Brad -> probe 2 -> empty -> slot 2, size 3 -> 3 >= 4? no
assert (hm.capacity, hm.size) == (8, 3)
assert slots(hm) == [(1, "Brad"), (2, "Collin"), (6, "Alice")]

# all three values retrievable, capacity doubled twice (2 -> 4 -> 8)
assert hm.get("Alice") == "NYC"
assert hm.get("Brad") == "Chicago"
assert hm.get("Collin") == "Seattle"
assert hm.get("Dylan") is None
assert hm.capacity == 8

# update an existing key does not change size
hm.put("Alice", "Boston")
assert hm.get("Alice") == "Boston" and hm.size == 3

# --- the same trace with the LESSON's made-up sums (25, 27, 33) ---
class LessonHashMap(HashMap):
    """Same code, but hash() uses the numbers from the NeetCode video instead of ord() sums."""
    FAKE = {"Alice": 25, "Brad": 27, "Collin": 33}

    def hash(self, key):
        return self.FAKE[key] % self.capacity


lm = LessonHashMap()
lm.put("Alice", "NYC")
# 25 % 2 = 1 -> slot 1, half full -> rehash to 4 -> 25 % 4 = 1 (same index, by luck)
assert (lm.capacity, lm.size) == (4, 1) and slots(lm) == [(1, "Alice")]
lm.put("Brad", "Chicago")
# 27 % 4 = 3 -> slot 3, size 2 = half -> rehash to 8 -> Alice 25 % 8 = 1, Brad 27 % 8 = 3
assert (lm.capacity, lm.size) == (8, 2) and slots(lm) == [(1, "Alice"), (3, "Brad")]
lm.put("Collin", "Seattle")
# 33 % 8 = 1 -> collision with Alice -> probe 2 -> empty -> slot 2
assert (lm.capacity, lm.size) == (8, 3) and slots(lm) == [(1, "Alice"), (2, "Collin"), (3, "Brad")]
assert lm.get("Collin") == "Seattle"

# --- the removal "hole" bug, concrete case ---
# Collin's home slot is 1 (33 % 8), but he sits at 2 because Alice was at 1.
lm.remove("Alice")                       # slot 1 becomes None: a hole
assert lm.map[1] is None
assert lm.map[2] is not None and lm.map[2].key == "Collin"   # Collin is STILL in the array...
assert lm.get("Collin") is None          # ...but get() hits the hole at slot 1 and stops early. BUG.

# same bug with the real sums: Collin (home 1) sits at 2 behind Brad (home 1)
hm2 = HashMap()
for k, v in [("Alice", "NYC"), ("Brad", "Chicago"), ("Collin", "Seattle")]:
    hm2.put(k, v)
hm2.remove("Brad")
assert hm2.map[2].key == "Collin" and hm2.get("Collin") is None   # lost

# a second bug in remove(): "if not self.get(key)" treats a falsy VALUE as "key absent"
z = HashMap()
z.put("zero", 0)
z.remove("zero")
assert z.get("zero") == 0                # never removed, because get returned 0 which is falsy


# --- fix: after clearing the slot, re-insert the rest of the cluster ---
class HashMapFixed(HashMap):
    def remove(self, key):
        index = self.hash(key)
        while self.map[index] is not None:            # search like get() does
            if self.map[index].key == key:
                self.map[index] = None
                self.size -= 1
                # re-put every pair that follows in the same cluster
                index = (index + 1) % self.capacity
                while self.map[index] is not None:
                    pair = self.map[index]
                    self.map[index] = None
                    self.size -= 1
                    self.put(pair.key, pair.val)
                    index = (index + 1) % self.capacity
                return
            index = (index + 1) % self.capacity


fm = HashMapFixed()
for k, v in [("Alice", "NYC"), ("Brad", "Chicago"), ("Collin", "Seattle")]:
    fm.put(k, v)
fm.remove("Brad")                        # Brad at 1, Collin at 2 (home 1) slides back into 1
assert fm.get("Brad") is None
assert fm.get("Collin") == "Seattle"
assert fm.get("Alice") == "NYC"
assert fm.size == 2
assert slots(fm) == [(1, "Collin"), (6, "Alice")]

# --- chaining version (added; the lesson describes it in words) ---
class ChainedHashMap:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]   # each slot holds a list of [key, val]

    def hash(self, key):
        return sum(ord(c) for c in key) % self.capacity

    def get(self, key):
        for k, v in self.buckets[self.hash(key)]:
            if k == key:
                return v
        return None

    def put(self, key, val):
        bucket = self.buckets[self.hash(key)]
        for item in bucket:
            if item[0] == key:
                item[1] = val
                return
        bucket.append([key, val])
        self.size += 1

    def remove(self, key):
        bucket = self.buckets[self.hash(key)]
        for i, item in enumerate(bucket):
            if item[0] == key:
                bucket.pop(i)
                self.size -= 1
                return


ch = ChainedHashMap(8)
ch.put("Brad", "Chicago")
ch.put("Collin", "Seattle")              # 609 % 8 = 1, same bucket as Brad
assert [k for k, _ in ch.buckets[1]] == ["Brad", "Collin"]
ch.remove("Brad")
assert ch.get("Collin") == "Seattle"     # no hole problem with chaining
assert ch.get("Brad") is None

# --- why a prime capacity spreads keys out ---
keys = [4, 8, 12, 16]
assert [k % 8 for k in keys] == [4, 0, 4, 0]      # capacity 8: two collisions
assert [k % 7 for k in keys] == [4, 1, 5, 2]      # capacity 7 (prime): all different

# =====================================================================
# Patterns
# =====================================================================

# Move 1: frequency map -> Valid Anagram (LC 242)
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    count = {}
    for ch_ in s:
        count[ch_] = count.get(ch_, 0) + 1
    for ch_ in t:
        if count.get(ch_, 0) == 0:
            return False
        count[ch_] -= 1
    return True

assert is_anagram("anagram", "nagaram") is True
assert is_anagram("rat", "car") is False
assert is_anagram("aab", "abb") is False
assert Counter("anagram") == Counter("nagaram")      # one-line version


# Move 2: seen-set -> Contains Duplicate (LC 217)
def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False

assert contains_duplicate([1, 2, 3, 1]) is True
assert contains_duplicate([1, 2, 3, 4]) is False
assert contains_duplicate([]) is False
assert (len(set([1, 2, 3, 1])) != 4) is True         # one-line version


# Move 2b: seen-set as "is this the start of a run?" -> Longest Consecutive Sequence (LC 128)
def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 not in s:                 # x starts a run
            length = 1
            while x + length in s:
                length += 1
            best = max(best, length)
    return best

assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
assert longest_consecutive([]) == 0


# Move 3: complement lookup -> Two Sum (LC 1)
def two_sum(nums, target):
    seen = {}                              # value -> index
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []

assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
assert two_sum([3, 3], 6) == [0, 1]
assert two_sum([1, 2], 10) == []


# Move 4: group by canonical key -> Group Anagrams (LC 49)
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = tuple(sorted(s))             # canonical form; tuple because a list cannot be a key
        groups[key].append(s)
    return list(groups.values())

def group_anagrams_count(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for ch_ in s:
            count[ord(ch_) - ord("a")] += 1
        groups[tuple(count)].append(s)     # O(k) key instead of O(k log k)
    return list(groups.values())

def norm(groups):
    return sorted(sorted(g) for g in groups)

expected = norm([["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])
assert norm(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])) == expected
assert norm(group_anagrams_count(["eat", "tea", "tan", "ate", "nat", "bat"])) == expected
assert group_anagrams([""]) == [[""]]


# Move 5: prefix sum + hashmap -> Subarray Sum Equals K (LC 560)
def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = {0: 1}                          # prefix sum -> how many times it appeared
    for x in nums:
        prefix += x
        count += seen.get(prefix - k, 0)   # earlier prefix that leaves exactly k
        seen[prefix] = seen.get(prefix, 0) + 1
    return count

assert subarray_sum([1, 1, 1], 2) == 2
assert subarray_sum([1, 2, 3], 3) == 2
assert subarray_sum([1, -1, 0], 0) == 3
assert subarray_sum([3, 4, 7, 2, -3, 1, 4, 2], 7) == 4


# Top K Frequent Elements (LC 347), via Counter
def top_k_frequent(nums, k):
    return [x for x, _ in Counter(nums).most_common(k)]

assert top_k_frequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
assert top_k_frequent([1], 1) == [1]


# First Unique Character in a String (LC 387)
def first_uniq_char(s):
    count = Counter(s)
    for i, ch_ in enumerate(s):
        if count[ch_] == 1:
            return i
    return -1

assert first_uniq_char("leetcode") == 0
assert first_uniq_char("loveleetcode") == 2
assert first_uniq_char("aabb") == -1

print("all checks passed")
