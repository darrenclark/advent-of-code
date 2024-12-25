import numpy as np
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
    # px = ax * an + bx * bn
    # py = ay * an + by * bn
    # cost = an * 3 + bn
    (ax, ay) = m['a']
    (bx, by) = m['b']
    (px, py) = m['p']

    a = np.array([[ax, bx], [ay, by]])
    b = np.array([px, py])
    an,bn = np.linalg.solve(a, b)

    if abs(an - round(an)) < 0.001 and abs(bn - round(bn)) < 0.001:
        return round(an) * 3 + round(bn)
    else:
        return None

pt1 = sum(cost(m) or 0 for m in machines_pt1)
print('Part 1:', pt1)

pt2 = sum(cost(m) or 0 for m in machines_pt2)
print('Part 2:', pt2)
