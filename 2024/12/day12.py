INPUT = 'input.txt'

with open(INPUT) as f:
    grid = [list(l.strip()) for l in f.readlines()]

w = len(grid[0])
h = len(grid)

def new_mask():
    return [
        [False for _ in range(w)] for _ in range(h)
    ]

def area(mask):
    return sum(sum(1 for x in row if x) for row in mask)

def get(mask, x, y):
    if x < 0 or x >= w or y < 0 or y >= h:
        return False
    return mask[y][x]

def perimeter(mask):
    c = 0
    for x in range(w):
        for y in range(h):
            if not mask[y][x]: continue

            c += 1 if not get(mask, x-1, y) else 0
            c += 1 if not get(mask, x+1, y) else 0
            c += 1 if not get(mask, x, y-1) else 0
            c += 1 if not get(mask, x, y+1) else 0

    return c

def corners(mask):
    c = 0

    def is_corner(x, y, dx, dy):
        # in terms of bottom right corner
        r = get(mask, x + dx, y)
        b = get(mask, x, y + dy)
        rb = get(mask, x + dx, y + dy)

        return (r == False and b == False) or (r == True and b == True and rb == False)


    for x in range(w):
        for y in range(h):
            if not mask[y][x]: continue

            lt = is_corner(x, y, -1, -1)
            rt = is_corner(x, y, 1, -1)
            lb = is_corner(x, y, -1, 1)
            rb = is_corner(x, y, 1, 1)

            c += 1 if lt else 0
            c += 1 if rt else 0
            c += 1 if lb else 0
            c += 1 if rb else 0

    return c


filled = new_mask()

def fill(grid, filled, x, y):
    mask = new_mask()

    l = grid[y][x]

    def do_fill(x, y):
        if x < 0 or x >= w or y < 0 or y >= h:
            return
        if filled[y][x] or grid[y][x] != l:
            return
        filled[y][x] = True
        mask[y][x] = True
        do_fill(x-1, y)
        do_fill(x+1, y)
        do_fill(x, y-1)
        do_fill(x, y+1)

    do_fill(x, y)

    return mask

pt1 = 0
pt2 = 0
for x in range(w):
    for y in range(h):
        if filled[y][x]: continue


        l = grid[y][x]
        m = fill(grid, filled, x, y)
        pt1 += area(m) * perimeter(m)
        pt2 += area(m) * corners(m)

print('Part 1:', pt1)
print('Part 2:', pt2)
