import re
import itertools

INPUT = 'input.txt'

machines_pt1 = []
machines_pt2 = []

with open(INPUT) as f:
    for g in f.read().split('\n\n'):
        [a, b, p] = g.split('\n')

        [ax, ay] = re.findall(r'\d+', a)
        [bx, by] = re.findall(r'\d+', b)
        [px, py] = re.findall(r'\d+', p)

        machines_pt1.append({'a': (int(ax), int(ay)), 'b': (int(bx), int(by)), 'p': (int(px), int(py))})
        machines_pt2.append({'a': (int(ax), int(ay)), 'b': (int(bx), int(by)), 'p': (int(px) + 10000000000000, int(py) + 10000000000000)})

def cost(m):
    print(m)
    # px = ax * an + bx * bn
    # py = ay * an + by * bn
    # cost = an * 3 + bn
    (ax, ay) = m['a']
    (bx, by) = m['b']
    (px, py) = m['p']

    c = None

    for an in itertools.count(start=0):
        rx = px - ax * an
        ry = py - ay * an

        if ry < 0 or rx < 0: break

        bn = rx // bx
        if rx % bx == 0 and by * bn == ry:
            c2 = an * 3 + bn
            c = c2 if c is None or c2 < c else c

    return c

pt1 = sum(cost(m) or 0 for m in machines_pt1)
print('Part 1:', pt1)

pt2 = sum(cost(m) or 0 for m in machines_pt2)
print('Part 2:', pt2)
