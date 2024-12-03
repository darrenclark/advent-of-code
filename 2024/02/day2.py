INPUT = 'input.txt'

with open(INPUT) as f:
    rows = [list(map(int, l.split())) for l in f.readlines()]

def is_valid(row):
    if row[0] == row[1]:
        return False
    if row[0] - row[1] > 0:
        for (a, b) in zip(row, row[1:]):
            if not (1 <= a - b <= 3):
                return False
    else:
        for (a, b) in zip(row, row[1:]):
            if not (1 <= b - a <= 3):
                return False
    return True

count = sum(1 for row in rows if is_valid(row))
print('Part 1:', count)

def is_valid_part2(row):
    if is_valid(row):
        return True
    else:
        for i in range(len(row)):
            r = list(row)
            r.pop(i)
            if is_valid(r):
                return True
    return False

count = 0
for row in rows:
    if is_valid_part2(row):
        count += 1

count = sum(1 for row in rows if is_valid_part2(row))
print('Part 2:', count)
