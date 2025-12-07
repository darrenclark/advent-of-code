from functools import cache

INPUT = 'input.txt'

with open(INPUT) as f:
    input = f.read().splitlines()

def part1():
    pt1 = 0
    cols: set[int] = set()

    for i, c in enumerate(input[0]):
        if c == 'S':
            cols.add(i)

    for r in input[1:]:
        new_cols = cols.copy()
        for i, c in enumerate(r):
            if c == '^' and i in cols:
                new_cols.remove(i)
                if i - 1 >= 0:
                    new_cols.add(i - 1)
                if i + 1 < len(r):
                    new_cols.add(i + 1)
                pt1 += 1

        cols = new_cols


    print("part 1:", pt1)

part1()

def part2():

    @cache
    def f(y, x):
        if y == len(input):
            return 1
        if input[y][x] == '^':
            return f(y + 1, x - 1) + f(y + 1, x + 1)
        return f(y + 1, x)

    s = 0
    for i, c in enumerate(input[0]):
        if c == 'S':
            s = i
            break

    print('part 2:', f(0, s))

part2()
