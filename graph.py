"""
Dependency graph — edges + parallel groups + DSU.

Edge rules (from Dependency.md):
  WRITE(A) ^ READ(B)  -> edge A -> B
  READ(A)  ^ WRITE(B) -> edge B -> A
  WRITE(A) ^ WRITE(B) -> lower id first

DSU (from Solutions.md):
  "create a graph and do a dsu to find root parent,,
   now we can know if any 2 are dependent."
"""

from collections import defaultdict, deque


class DSU:
    """Disjoint Set Union to check if two cells are connected."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return
        if self.rank[a] < self.rank[b]:
            a, b = b, a
        self.parent[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1

    def connected(self, a, b):
        return self.find(a) == self.find(b)


class DependencyGraph:

    def __init__(self, cells):
        self.cells = cells
        self.edges = []
        self.adj = defaultdict(set)
        self.dsu = DSU(len(cells))
        self._build()

    def _build(self):
        n = len(self.cells)
        for i in range(n):
            for j in range(i + 1, n):
                A, B = self.cells[i], self.cells[j]

                flow = A.write & B.read
                if flow:
                    self._add_edge(A.id, B.id, "flow", flow)

                anti = A.read & B.write
                if anti:
                    self._add_edge(A.id, B.id, "anti", anti)

                output = A.write & B.write
                if output:
                    src, dst = (A.id, B.id) if A.id < B.id else (B.id, A.id)
                    self._add_edge(src, dst, "output", output)

    def _add_edge(self, src, dst, kind, variables):
        if dst not in self.adj[src]:
            self.edges.append((src, dst, kind, variables))
            self.adj[src].add(dst)
        self.dsu.union(src, dst)

    def are_dependent(self, a, b):
        return self.dsu.connected(a, b)

    def parallel_groups(self):
        """Topological sort into levels — each level runs in parallel."""
        in_deg = {c.id: 0 for c in self.cells}
        for src, dst, _, _ in self.edges:
            in_deg[dst] += 1

        queue = deque(cid for cid, d in sorted(in_deg.items()) if d == 0)
        levels = []

        while queue:
            level = sorted(queue)
            levels.append(level)
            queue = deque()
            for node in level:
                for nb in sorted(self.adj[node]):
                    in_deg[nb] -= 1
                    if in_deg[nb] == 0:
                        queue.append(nb)

        return levels
