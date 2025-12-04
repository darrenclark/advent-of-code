INPUT = 'input.txt'

with open(INPUT) as f:
    input = [list(map(int, l.strip())) for l in f.read().strip().splitlines()]

pt1 = 0
pt2 = 0

def max_in_line(line):
    max_i = 0
    max_x = line[0]

    for i, x in enumerate(line):
        if x > max_x:
            max_x = x
            max_i = i

    return max_i, max_x

def compute(line, acc, n):
    if n:
        max_i, max_x = max_in_line(line[:-n])
    else:
        max_i, max_x = max_in_line(line)

    acc = acc * 10 + max_x

    if n == 0:
        return acc

    return compute(line[max_i + 1:], acc, n - 1)

for line in input:
    pt1 += compute(line, 0, 1)
    pt2 += compute(line, 0, 11)

print('Part 1:', pt1)
print('Part 2:', pt2)
