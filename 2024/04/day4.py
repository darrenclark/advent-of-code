INPUT = 'input.txt'

with open(INPUT) as f:
    rows = [list(l.strip()) for l in f.readlines()]

w = len(rows[0])
h = len(rows)

def is_xmas(a, b, c, d):
    if a[0] < 0 or a[1] < 0 or b[0] < 0 or b[1] < 0 or c[0] < 0 or c[1] < 0 or d[0] < 0 or d[1] < 0:
        return False

    try:
        if rows[a[1]][a[0]] == 'X' and rows[b[1]][b[0]] == 'M' and rows[c[1]][c[0]] == 'A' and rows[d[1]][d[0]] == 'S':
            return True
    except IndexError:
        pass
    return False

count = 0

for x in range(w):
    for y in range(h):
        # right
        if is_xmas((x, y), (x+1, y), (x+2, y), (x+3, y)):
            count += 1
        # down right
        if is_xmas((x, y), (x+1, y+1), (x+2, y+2), (x+3, y+3)):
            count += 1
        # down
        if is_xmas((x, y), (x, y+1), (x, y+2), (x, y+3)):
            count += 1
        # down left
        if is_xmas((x, y), (x-1, y+1), (x-2, y+2), (x-3, y+3)):
            count += 1
        # left
        if is_xmas((x, y), (x-1, y), (x-2, y), (x-3, y)):
            count += 1
        # up left
        if is_xmas((x, y), (x-1, y-1), (x-2, y-2), (x-3, y-3)):
            count += 1
        # up
        if is_xmas((x, y), (x, y-1), (x, y-2), (x, y-3)):
            count += 1
        # up right
        if is_xmas((x, y), (x+1, y-1), (x+2, y-2), (x+3, y-3)):
            count += 1

print('Part 1:', count)

def is_x_mas(x, y):
    if rows[y][x] != 'A':
        return False

    if x - 1 < 0 or y - 1 < 0 or x + 1 >= w or y + 1 >= h:
        return False

    ul = rows[y-1][x-1]
    ur = rows[y-1][x+1]
    dr = rows[y+1][x+1]
    dl = rows[y+1][x-1]

    if not ((ul == 'M' and dr == 'S') or (ul == 'S' and dr == 'M')):
        return False

    if not ((ur == 'M' and dl == 'S') or (ur == 'S' and dl == 'M')):
        return False

    return True

count = 0

for x in range(w):
    for y in range(h):
        if is_x_mas(x, y):
            count += 1

print('Part 2:', count)
