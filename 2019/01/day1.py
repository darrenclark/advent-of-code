INPUT = 'input.txt'

with open(INPUT, 'r') as infile:
    data = [int(l.strip()) for l in infile.readlines()]

r = sum(x // 3 - 2 for x in data)
print('Part 1:', r)

def fuel(x):
    f = x // 3 - 2
    if f <= 0:
        return 0
    return f + fuel(f)

r = sum(fuel(x) for x in data)
print('Part 2:', r)
