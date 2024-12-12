from functools import cache

INPUT = 'input.txt'

with open(INPUT) as f:
    input = list(map(int, f.read().strip().split()))

@cache
def count(s, b):
    if b == 0:
        return 1
    if s == 0:
        return count(1, b-1)
    elif len(str(s)) % 2 == 0:
        s = str(s)
        return count(int(s[0:len(s)//2]), b-1) + count(int(s[len(s)//2:]), b-1)
    else:
        return count(s*2024, b-1)

PT1_COUNT = 25
PT2_COUNT = 75

for i in range(0, PT1_COUNT):
    sum([count(s, i) for s in input])

print('Part 1:', sum([count(s, PT1_COUNT) for s in input]))
print('Part 2:', sum([count(s, PT2_COUNT) for s in input]))
