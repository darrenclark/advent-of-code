INPUT = 'input.txt'

with open(INPUT) as f:
    def parse_line(l):
        [test_value, numbers] = l.strip().split(':')
        return (int(test_value), list(map(int, numbers.split())))

    rows = [parse_line(l) for l in f.readlines()]

def check(tv, acc, numbers):
    if len(numbers) == 0:
        return acc == tv

    next = numbers[0]
    return check(tv, acc * next, numbers[1:]) or check(tv, acc + next, numbers[1:])

s = 0

for (tv, numbers) in rows:
    if check(tv, numbers[0], numbers[1:]):
        s += tv

print('Part 1:', s)

def concat(a, b):
    return int(str(a) + str(b))

def check_pt2(tv, acc, numbers):
    if len(numbers) == 0:
        return acc == tv

    next = numbers[0]
    return check_pt2(tv, acc * next, numbers[1:]) or check_pt2(tv, acc + next, numbers[1:]) or check_pt2(tv, concat(acc, next), numbers[1:])

s = 0

for (tv, numbers) in rows:
    if check_pt2(tv, numbers[0], numbers[1:]):
        s += tv

print('Part 2:', s)
