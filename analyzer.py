"""
AST-based analyzer to extract READ / WRITE sets from a cell.

Handles (from Dependency.md):
  Name        : LOAD -> READ, STORE -> WRITE
  Assignment  : analyze RHS then targets
  AugAssign   : READ target + RHS, WRITE target
  FunctionDef : WRITE function name (body skipped)
  Import      : WRITE imported name
"""

import ast
from Jupyter_parallel_run.cell import Cell


class DependencyAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.read = set()
        self.write = set()

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):
            self.read.add(node.id)
        elif isinstance(node.ctx, (ast.Store, ast.Del)):
            self.write.add(node.id)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        if isinstance(node.target, ast.Name):
            self.read.add(node.target.id)
            self.write.add(node.target.id)
        self.visit(node.value)

    def visit_FunctionDef(self, node):
        self.write.add(node.name)

    def visit_AsyncFunctionDef(self, node):
        self.write.add(node.name)

    def visit_ClassDef(self, node):
        self.write.add(node.name)

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.write.add(name.split(".")[0])

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.write.add(alias.asname or alias.name)


def analyze_cell(cell):
    """Parse cell source, populate cell.read and cell.write, return cell."""
    analyzer = DependencyAnalyzer()
    analyzer.visit(ast.parse(cell.source))
    cell.read = analyzer.read
    cell.write = analyzer.write
    return cell
