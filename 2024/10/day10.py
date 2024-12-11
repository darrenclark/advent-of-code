INPUT = 'input.txt'

with open(INPUT) as f:
    grid = [list(map(int, list(l.strip()))) for l in f.readlines()]

w = len(grid[0])
h = len(grid)

def get_cell(x, y):
    if x < 0 or x >= w or y < 0 or y >= h:
        return None
    return grid[y][x]

def trailhead_score(x, y, i):
    def score(x, y, i, acc: set):
        if i == 9:
            acc.add((x, y))
            return 1
        else:
            if get_cell(x + 1, y) == i + 1:
                score(x + 1, y, i + 1, acc)
            if get_cell(x - 1, y) == i + 1:
                score(x - 1, y, i + 1, acc)
            if get_cell(x, y + 1) == i + 1:
                score(x, y + 1, i + 1, acc)
            if get_cell(x, y - 1) == i + 1:
                score(x, y - 1, i + 1, acc)

    acc = set()
    score(x, y, i, acc)
    return len(acc)

s = 0
for y in range(h):
    for x in range(w):
        if grid[y][x] == 0:
            sc = trailhead_score(x, y, 0)
            s += sc

print('Part 1:', s)

def trailhead_rating(x, y, i):
    if i == 9:
        return 1
    else:
        c = 0
        if get_cell(x + 1, y) == i + 1:
            c += trailhead_rating(x + 1, y, i + 1)
        if get_cell(x - 1, y) == i + 1:
            c += trailhead_rating(x - 1, y, i + 1)
        if get_cell(x, y + 1) == i + 1:
            c += trailhead_rating(x, y + 1, i + 1)
        if get_cell(x, y - 1) == i + 1:
            c += trailhead_rating(x, y - 1, i + 1)
        return c

s = 0
for y in range(h):
    for x in range(w):
        if grid[y][x] == 0:
            s += trailhead_rating(x, y, 0)

print('Part 2:', s)
