# Checks for site/topics/10-graphs.html
# Every function on the page lives here and is tested on the lesson's own examples.
from collections import deque, defaultdict

# ----------------------------------------------------------------------
# Lesson 28: formats
# ----------------------------------------------------------------------
grid = [[0, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 1, 0, 0]]

assert grid[1] == [1, 1, 0, 0]          # second row
assert grid[1][0] == 1                  # first column of the second row
ROWS, COLS = len(grid), len(grid[0])
assert (ROWS, COLS) == (4, 4)

# The same numbers read as an adjacency matrix: row = from, column = to
adjMatrix = [[0, 0, 0, 0],
             [1, 1, 0, 0],
             [0, 0, 0, 1],
             [0, 1, 0, 0]]
assert adjMatrix[1][2] == 0             # no edge 1 -> 2
assert adjMatrix[2][1] == 0             # no edge 2 -> 1
assert adjMatrix[2][3] == 1             # edge 2 -> 3 (the highlighted cell on the page)
assert adjMatrix[1][1] == 1             # self loop on 1

# list every directed edge the matrix encodes
edges_in_matrix = [(v1, v2) for v1 in range(4) for v2 in range(4) if adjMatrix[v1][v2] == 1]
assert edges_in_matrix == [(1, 0), (1, 1), (2, 3), (3, 1)], edges_in_matrix

# E <= V^2 : complete graph on 3 vertices, self loops allowed
V = ["A", "B", "C"]
complete = [(a, b) for a in V for b in V]
assert len(complete) == len(V) ** 2 == 9


class GraphNode:
    def __init__(self, val):
        self.val = val
        self.neighbors = []


a, b = GraphNode("A"), GraphNode("B")
a.neighbors.append(b)
assert a.neighbors[0].val == "B" and b.neighbors == []

# ----------------------------------------------------------------------
# Lesson 29: Matrix DFS - count unique paths (backtracking), NeetCode version
# ----------------------------------------------------------------------
def dfs(grid, r, c, visit):
    ROWS, COLS = len(grid), len(grid[0])
    if (min(r, c) < 0 or
        r == ROWS or c == COLS or
        (r, c) in visit or grid[r][c] == 1):
        return 0
    if r == ROWS - 1 and c == COLS - 1:
        return 1

    visit.add((r, c))

    count = 0
    count += dfs(grid, r + 1, c, visit)
    count += dfs(grid, r - 1, c, visit)
    count += dfs(grid, r, c + 1, visit)
    count += dfs(grid, r, c - 1, visit)

    visit.remove((r, c))
    return count


assert dfs(grid, 0, 0, set()) == 2
assert dfs(grid, 0, 0, set()) == 2      # visit set is clean after backtracking, so it repeats
assert dfs(grid, -1, 3, set()) == 0     # out of bounds
assert dfs(grid, 1, 0, set()) == 0      # standing on a 1

# The same DFS, but also record every path so the page can draw them.
def all_paths(grid, r, c, visit, path, out):
    ROWS, COLS = len(grid), len(grid[0])
    if (min(r, c) < 0 or r == ROWS or c == COLS or
            (r, c) in visit or grid[r][c] == 1):
        return
    path.append((r, c))
    if r == ROWS - 1 and c == COLS - 1:
        out.append(list(path))
        path.pop()
        return
    visit.add((r, c))
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        all_paths(grid, r + dr, c + dc, visit, path, out)
    visit.remove((r, c))
    path.pop()


paths = []
all_paths(grid, 0, 0, set(), [], paths)
assert len(paths) == 2, paths
short = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (3, 2), (3, 3)]
long_ = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 2), (2, 2), (3, 2), (3, 3)]
assert short in paths and long_ in paths, paths
assert len(short) - 1 == 6 and len(long_) - 1 == 8   # edge counts (BFS answer is 6)

# One dead end the page draws: (0,2) -> (1,2) -> (1,3) -> (0,3) has nowhere to go.
visit = {(0, 0), (0, 1), (0, 2), (1, 2), (1, 3)}
assert dfs(grid, 0, 3, visit) == 0

# Generic grid-DFS template with an explicit bounds helper (Patterns section)
def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])


assert in_bounds(grid, 0, 0) and in_bounds(grid, 3, 3)
assert not in_bounds(grid, -1, 3) and not in_bounds(grid, 4, 0) and not in_bounds(grid, 0, 4)

# ----------------------------------------------------------------------
# Lesson 30: Matrix BFS - shortest path top-left to bottom-right, NeetCode version
# ----------------------------------------------------------------------
def bfs(grid):
    ROWS, COLS = len(grid), len(grid[0])
    visit = set()
    queue = deque()
    queue.append((0, 0))
    visit.add((0, 0))

    length = 0
    while queue:
        for i in range(len(queue)):
            r, c = queue.popleft()
            if r == ROWS - 1 and c == COLS - 1:
                return length

            neighbors = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            for dr, dc in neighbors:
                if (min(r + dr, c + dc) < 0 or
                    r + dr == ROWS or c + dc == COLS or
                    (r + dr, c + dc) in visit or grid[r + dr][c + dc] == 1):
                    continue
                queue.append((r + dr, c + dc))
                visit.add((r + dr, c + dc))
        length += 1


assert bfs(grid) == 6
assert bfs([[0]]) == 0                  # start is the target
assert bfs([[0, 0], [0, 0]]) == 2

# Same BFS, but record the queue at the start of every level and the
# distance of every cell, so the page's trace table and ring diagram are exact.
def bfs_trace(grid):
    ROWS, COLS = len(grid), len(grid[0])
    visit = {(0, 0)}
    queue = deque([(0, 0)])
    dist = {(0, 0): 0}
    levels = []
    length = 0
    while queue:
        levels.append((length, list(queue)))
        for i in range(len(queue)):
            r, c = queue.popleft()
            if r == ROWS - 1 and c == COLS - 1:
                return length, levels, dist, list(queue)
            for dr, dc in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
                nr, nc = r + dr, c + dc
                if (min(nr, nc) < 0 or nr == ROWS or nc == COLS or
                        (nr, nc) in visit or grid[nr][nc] == 1):
                    continue
                queue.append((nr, nc))
                visit.add((nr, nc))
                dist[(nr, nc)] = length + 1
        length += 1
    return -1, levels, dist, []


length, levels, dist, leftover = bfs_trace(grid)
assert length == 6
expected_levels = [
    (0, [(0, 0)]),
    (1, [(0, 1)]),
    (2, [(0, 2)]),
    (3, [(0, 3), (1, 2)]),
    (4, [(1, 3), (2, 2)]),
    (5, [(2, 1), (3, 2)]),
    (6, [(2, 0), (3, 3)]),
]
assert levels == expected_levels, levels
assert leftover == [(3, 0)], leftover   # (3,0) was queued at distance 7 but never popped
expected_dist = {(0, 0): 0, (0, 1): 1, (0, 2): 2, (0, 3): 3, (1, 2): 3,
                 (1, 3): 4, (2, 2): 4, (2, 1): 5, (3, 2): 5, (2, 0): 6,
                 (3, 3): 6, (3, 0): 7}
assert dist == expected_dist, dist

# Directions array: the four moves from a cell
directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
r, c = 2, 2
assert [(r + dr, c + dc) for dr, dc in directions] == [(2, 3), (2, 1), (3, 2), (1, 2)]

# Patterns: generic BFS shortest path with the level loop, -1 when unreachable
def shortest_path(grid, start, target):
    ROWS, COLS = len(grid), len(grid[0])
    queue = deque([start])
    visit = {start}
    length = 0
    while queue:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            if (r, c) == target:
                return length
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 <= nr < ROWS and 0 <= nc < COLS and
                        grid[nr][nc] == 0 and (nr, nc) not in visit):
                    visit.add((nr, nc))
                    queue.append((nr, nc))
        length += 1
    return -1


assert shortest_path(grid, (0, 0), (3, 3)) == 6
assert shortest_path(grid, (0, 0), (3, 0)) == 7
assert shortest_path([[0, 1], [1, 0]], (0, 0), (1, 1)) == -1

# ----------------------------------------------------------------------
# Lesson 31: Adjacency list
# ----------------------------------------------------------------------
edges = [["A", "B"], ["B", "C"], ["B", "E"], ["C", "E"], ["E", "D"]]

adjList = {}
for src, dst in edges:
    if src not in adjList:
        adjList[src] = []
    if dst not in adjList:
        adjList[dst] = []
    adjList[src].append(dst)

assert adjList == {"A": ["B"], "B": ["C", "E"], "C": ["E"], "D": [], "E": ["D"]}, adjList


# DFS: count paths from node to target (backtracking)
def dfs_count(node, target, adjList, visit):
    if node in visit:
        return 0
    if node == target:
        return 1

    count = 0
    visit.add(node)
    for neighbor in adjList[node]:
        count += dfs_count(neighbor, target, adjList, visit)
    visit.remove(node)

    return count


assert dfs_count("A", "E", adjList, set()) == 2     # A-B-E and A-B-C-E
assert dfs_count("A", "D", adjList, set()) == 2     # both continue E -> D
assert dfs_count("D", "A", adjList, set()) == 0     # D has no outgoing edges
assert dfs_count("A", "A", adjList, set()) == 1     # already there


# BFS: shortest path from node to target (NeetCode version)
def bfs_list(node, target, adjList):
    length = 0
    visit = set()
    visit.add(node)
    queue = deque()
    queue.append(node)

    while queue:
        for i in range(len(queue)):
            curr = queue.popleft()
            if curr == target:
                return length

            for neighbor in adjList[curr]:
                if neighbor not in visit:
                    visit.add(neighbor)
                    queue.append(neighbor)
        length += 1
    return length


assert bfs_list("A", "E", adjList) == 2
assert bfs_list("A", "D", adjList) == 3
assert bfs_list("A", "A", adjList) == 0
# quirk of the lesson code: an unreachable target returns the level count, not -1
assert bfs_list("D", "A", adjList) == 1


def bfs_list_trace(node, target, adjList):
    visit = {node}
    queue = deque([node])
    levels, length = [], 0
    while queue:
        levels.append((length, list(queue)))
        for i in range(len(queue)):
            curr = queue.popleft()
            if curr == target:
                return length, levels
            for neighbor in adjList[curr]:
                if neighbor not in visit:
                    visit.add(neighbor)
                    queue.append(neighbor)
        length += 1
    return -1, levels


length, levels = bfs_list_trace("A", "E", adjList)
assert length == 2
assert levels == [(0, ["A"]), (1, ["B"]), (2, ["C", "E"])], levels

# Patterns: building adjacency lists with defaultdict, directed and undirected
def build_directed(edges):
    adj = defaultdict(list)
    for src, dst in edges:
        adj[src].append(dst)
        adj[dst]                      # touch it so isolated sinks get a key
    return adj


def build_undirected(edges):
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


assert dict(build_directed(edges)) == adjList
und = build_undirected(edges)
assert und["E"] == ["B", "C", "D"] and und["D"] == ["E"] and und["A"] == ["B"]
assert sum(len(v) for v in und.values()) == 2 * len(edges)   # every edge stored twice

# Numeric vertices 0..n-1 as a list of lists (LeetCode style)
def build_undirected_list(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


assert build_undirected_list(3, [[0, 1], [1, 2]]) == [[1], [0, 2], [1]]

# O(V + E): count vertices visited and edges relaxed in one BFS
def bfs_work(start, adj):
    visit = {start}
    queue = deque([start])
    vertices_popped = edges_checked = 0
    while queue:
        curr = queue.popleft()
        vertices_popped += 1
        for nb in adj[curr]:
            edges_checked += 1
            if nb not in visit:
                visit.add(nb)
                queue.append(nb)
    return vertices_popped, edges_checked


assert bfs_work("A", adjList) == (5, 5)   # 5 vertices, 5 edges, each touched once

# Reachability with DFS (LC 1971 shape): is there a path from src to dst?
def has_path(adj, src, dst, visit=None):
    if visit is None:
        visit = set()
    if src == dst:
        return True
    visit.add(src)
    for nb in adj[src]:
        if nb not in visit and has_path(adj, nb, dst, visit):
            return True
    return False


assert has_path(adjList, "A", "D") and not has_path(adjList, "D", "A")

# ----------------------------------------------------------------------
# Patterns: flood fill / number of islands
# ----------------------------------------------------------------------
def num_islands(grid):
    ROWS, COLS = len(grid), len(grid[0])
    visit = set()

    def dfs(r, c):
        if (r < 0 or c < 0 or r >= ROWS or c >= COLS or
                grid[r][c] != "1" or (r, c) in visit):
            return
        visit.add((r, c))
        for dr, dc in directions:
            dfs(r + dr, c + dc)

    count = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "1" and (r, c) not in visit:
                dfs(r, c)
                count += 1
    return count


islands = [["1", "1", "0", "0", "0"],
           ["1", "1", "0", "0", "0"],
           ["0", "0", "1", "0", "0"],
           ["0", "0", "0", "1", "1"]]
assert num_islands(islands) == 3
assert islands[0][0] == "1"             # grid untouched (visited set, not sinking)


def num_islands_in_place(grid):
    ROWS, COLS = len(grid), len(grid[0])

    def sink(r, c):
        if r < 0 or c < 0 or r >= ROWS or c >= COLS or grid[r][c] != "1":
            return
        grid[r][c] = "0"                  # mark by overwriting: the grid is the visit set
        for dr, dc in directions:
            sink(r + dr, c + dc)

    count = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == "1":
                sink(r, c)
                count += 1
    return count


copy_ = [row[:] for row in islands]
assert num_islands_in_place(copy_) == 3
assert all(cell == "0" for row in copy_ for cell in row)   # grid was destroyed


def max_area(grid):
    ROWS, COLS = len(grid), len(grid[0])
    visit = set()

    def dfs(r, c):
        if (r < 0 or c < 0 or r >= ROWS or c >= COLS or
                grid[r][c] == 0 or (r, c) in visit):
            return 0
        visit.add((r, c))
        return 1 + sum(dfs(r + dr, c + dc) for dr, dc in directions)

    return max((dfs(r, c) for r in range(ROWS) for c in range(COLS)), default=0)


assert max_area([[0, 1, 1, 0], [0, 1, 0, 0], [1, 0, 0, 1]]) == 3
assert max_area([[0, 0]]) == 0


def flood_fill(image, sr, sc, color):
    ROWS, COLS = len(image), len(image[0])
    old = image[sr][sc]
    if old == color:
        return image                      # nothing to do; avoids an infinite recolor loop

    def dfs(r, c):
        if r < 0 or c < 0 or r >= ROWS or c >= COLS or image[r][c] != old:
            return
        image[r][c] = color
        for dr, dc in directions:
            dfs(r + dr, c + dc)

    dfs(sr, sc)
    return image


assert flood_fill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2) == [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
assert flood_fill([[0, 0, 0], [0, 0, 0]], 0, 0, 0) == [[0, 0, 0], [0, 0, 0]]

# Multi-source BFS (Rotting Oranges shape): start with every source in the queue
def rotting_oranges(grid):
    ROWS, COLS = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1


assert rotting_oranges([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4
assert rotting_oranges([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1
assert rotting_oranges([[0, 2]]) == 0

# Connected components on an undirected adjacency list (NeetCode 323 shape)
def count_components(n, edges):
    adj = build_undirected_list(n, edges)
    visit = set()

    def dfs(node):
        visit.add(node)
        for nb in adj[node]:
            if nb not in visit:
                dfs(nb)

    count = 0
    for node in range(n):
        if node not in visit:
            dfs(node)
            count += 1
    return count


assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2
assert count_components(3, []) == 3

print("all checks passed")
