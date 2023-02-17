from pathlib import Path

p = Path(".")
n_lines = 0
for file in p.glob("**/*.py"):
    n_lines += len(open(file).readlines())

print(n_lines)
