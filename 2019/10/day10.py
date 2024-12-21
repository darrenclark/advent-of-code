import math
INPUT = 'input.txt'
with open(INPUT) as f:
    input = f.read()

g = [list(l) for l in input.strip().split('\n')]
h = len(g)
w = len(g[0])

a = set()

for y in range(h):
    for x in range(w):
        if g[y][x] == '#':
            a.add((x,y))

def in_bounds(x, y):
    return x >= 0 and x < w and y >= 0 and y < h

def n_los(x, y):
    v = set(a)
    v.remove((x,y))

    for ax,ay in a:
        if (ax,ay) not in v:
            continue

        dx = ax - x
        dy = ay - y

        #dix = dx / abs(dx) if dx != 0 else 0
        #diy = dy / abs(dy) if dy != 0 else 0

        gcd = math.gcd(abs(dx), abs(dy))
        dx = dx//gcd
        dy = dy//gcd

        while in_bounds(ax, ay):
            ax += dx
            ay += dy
            if (ax, ay) in v:
                v.remove((ax, ay))

    return len(v)

los = {(x,y):n_los(x,y) for y in range(h) for x in range(w) if (x,y) in a}
ans = max(los, key=lambda xy: los[xy])
print('Part 1:', los[ans])
