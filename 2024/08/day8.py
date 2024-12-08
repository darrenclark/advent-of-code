INPUT = 'input.txt'

with open(INPUT) as f:
    grid = [list(l.strip()) for l in f.readlines()]

w = len(grid[0])
h = len(grid)

antinodes = [[False] * w for _ in range(h)]

def put_antinode(x, y):
    if x < 0 or x >= w or y < 0 or y >= h:
        return False

    antinodes[y][x] = True
    return True

def get_same_frequence_coordinates(x, y):
    f = grid[y][x]

    for ix in range(w):
        for iy in range(h):
            if grid[iy][ix] == f and (ix, iy) != (x, y):
                yield (ix, iy)

for x in range(w):
    for y in range(h):
        f = grid[y][x]
        if f == '.':
            continue

        for (ox, oy) in get_same_frequence_coordinates(x, y):
            dx = ox - x
            dy = oy - y

            put_antinode(x - dx, y - dy)


def print_grid():
    for y in range(h):
        for x in range(w):
            print('#' if antinodes[y][x] else grid[y][x], end='')
        print()

# print_grid()

c = sum(1 for row in antinodes for a in row if a)
print('Part 1:', c)

antinodes = [[False] * w for _ in range(h)]

for x in range(w):
    for y in range(h):
        f = grid[y][x]
        if f == '.':
            continue

        for (ox, oy) in get_same_frequence_coordinates(x, y):
            dx = ox - x
            dy = oy - y

            i = 0
            while put_antinode(x - dx * i, y - dy * i):
                i += 1

# print_grid()

c = sum(1 for row in antinodes for a in row if a)
print('Part 2:', c)
