from pathlib import Path

p = Path.cwd()
p = list(p.glob('*'))
print(p)