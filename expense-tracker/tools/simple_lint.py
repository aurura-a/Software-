"""Minimal stand-in lint (ruff/flake8 were not installable offline): line length, trailing
whitespace, tabs, and unused imports. Run: python3 tools/simple_lint.py"""
import ast
import pathlib
import sys

problems = 0
for path in sorted(pathlib.Path(".").glob("expense_tracker/*.py")) + sorted(pathlib.Path(".").glob("tests/*.py")):
    text = path.read_text()
    for n, line in enumerate(text.splitlines(), 1):
        if len(line) > 100:
            print("%s:%d: line > 100 chars" % (path, n)); problems += 1
        if line != line.rstrip():
            print("%s:%d: trailing whitespace" % (path, n)); problems += 1
        if "\t" in line:
            print("%s:%d: tab character" % (path, n)); problems += 1
    tree = ast.parse(text)
    imported = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                imported[(a.asname or a.name).split(".")[0]] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                imported[a.asname or a.name] = node.lineno
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | {
        n.value.id for n in ast.walk(tree) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)}
    for name, lineno in imported.items():
        if name not in names:
            print("%s:%d: unused import %s" % (path, lineno, name)); problems += 1
print("simple_lint: %d problem(s)" % problems)
sys.exit(1 if problems else 0)
