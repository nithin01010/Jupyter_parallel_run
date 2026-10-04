"""Demo — dependency analysis on a sample notebook."""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Jupyter_parallel_run import Cell, analyze_cell, DependencyGraph

sources = [
    "import pandas as pd",
    "x = 10",
    "y = 20",
    "z = x + y",
    "x += 1",
    "c = z + x + y",
    'df = pd.read_csv("data.csv")',
    "print(z, df.shape)",
]

cells = [analyze_cell(Cell(id=i, source=s)) for i, s in enumerate(sources)]
graph = DependencyGraph(cells)

print("Cells:")
for c in cells:
    print(f"  [{c.id}] {c.source:36s}  R={sorted(c.read)}  W={sorted(c.write)}")

print("\nEdges:")
for src, dst, kind, vs in graph.edges:
    print(f"  Cell {src} -> Cell {dst}  [{kind}] {sorted(vs)}")

print("\nParallel levels:")
for i, group in enumerate(graph.parallel_groups()):
    print(f"  Level {i}: {group}")

print("\nDSU checks:")
for a, b in [(0, 1), (1, 3), (3, 4)]:
    print(f"  Cell {a} & Cell {b}: {'dependent' if graph.are_dependent(a, b) else 'independent'}")
