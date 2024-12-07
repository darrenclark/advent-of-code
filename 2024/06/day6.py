INPUT = 'input.txt'

with open(INPUT) as f:
    grid = [list(l.strip()) for l in f.readlines()]

w = len(grid[0])
h = len(grid)

sx = -1
sy = -1

gdx = 0
gdy = -1

for x in range(h):
    for y in range(w):
        if grid[y][x] == '^':
            sx = x
            sy = y
            break


def in_bounds(x, y):
    return 0 <= x < w and 0 <= y < h

def is_obstruction(g, x, y):
    return in_bounds(x,y) and g[y][x] == '#'

class StuckInLoop(Exception):
    pass

def walk(g):
    gx = sx
    gy = sy

    gdx = 0
    gdy = -1

    positions = set()
    positions_with_direction = set()

    positions.add((gx, gy))

    while in_bounds(gx, gy):

        if is_obstruction(g, gx + gdx, gy + gdy):
            # turn 90 right
            if gdy == -1:
                gdy = 0
                gdx = 1
            elif gdx == 1:
                gdy = 1
                gdx = 0
            elif gdy == 1:
                gdx = -1
                gdy = 0
            elif gdx == -1:
                gdx = 0
                gdy = -1
        else:
            gx = gx + gdx
            gy = gy + gdy
            if in_bounds(gx, gy):
                positions.add((gx, gy))
                if (gx, gy, gdx, gdy) in positions_with_direction:
                    raise StuckInLoop()
                positions_with_direction.add((gx, gy, gdx, gdy))

    return len(positions)

print('Part 1:', walk(grid))

c = 0

for y in range(h):
    for x in range(w):
        if grid[y][x] == '.':
            grid[y][x] = '#'
            try:
                walk(grid)
            except StuckInLoop:
                c += 1
            grid[y][x] = '.'

print('Part 2:', c)
